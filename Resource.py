import datetime

from Util import *


class Resource:
    def __init__(self, **kwargs):
        self.resourceId = kwargs["resourceId"]  # 机器id
        self.resourceName = kwargs["resourceName"]  # 机器名称
        self.operationType = kwargs["operationType"]  # 可操作工序类型
        self.operationTypeName = kwargs["operationTypeName"]  # 可操作工序类名称
        self.earlyStartTime = kwargs["earlyStartTime"]  # 最早开始时间
        self.earlyAvailableTime = datetime.datetime(2000, 1, 1, 0, 0, 0)  # 最早可使用时间
        self.assignmentList = []  # 分配的任务

    def calcEarlyAvailableTime(self):
        """
        计算最早可获得时间
        :return:
        """
        if self.assignmentList:
            self.earlyAvailableTime = timestamp_to_minutes(self.assignmentList[-1].endTime)

    def calcPrefixDuration(self, productStep, products):
        """
        计算换型时间
        :param productStep:
        :param products:
        :return:
        """
        if self.assignmentList:
            if products[productStep.productId].productType == products[self.assignmentList[-1].productId].productType:
                return 0
            else:
                return productStep.processTime * 0.05
        else:
            return 0

    def calcProcessDuration(self, productStep, products):
        """
        计算处理时间

        如果机器上暂未安排工序，则为本身工序的处理时间
        如果机器上安排了工序：
            如果本身为产品的第一个工序，则只需要序与所在机器的上一个工序类型相同，则可以合并处理
            否则：
                需要当前产品的上一个工序的完成时间t1和所在机器的上一个工序的完成时间t2做对比
                    如果t1<=t2,且工序与所在机器的上一个工序类型相同，则可以合并处理，取当前工序处理时间的0.75倍
                    否则，为本身工序的处理时间
        :param productStep:
        :param products:
        :return:
        """
        if self.assignmentList:
            if not productStep.previewStep:
                if products[self.assignmentList[-1].productId].productType == \
                        products[productStep.productId].productType:
                    return productStep.processTime * 0.75
                else:
                    return productStep.processTime
            else:
                if productStep.previewStep.isSchedule:
                    previewAssignment = productStep.previewStep.isSchedule
                    t1 = timestamp_to_minutes(previewAssignment.endTime)
                    t2 = timestamp_to_minutes(self.assignmentList[-1].endTime)
                    if t1 <= t2 and products[self.assignmentList[-1].productId].productType == \
                            products[productStep.productId].productType:
                        return productStep.processTime * 0.75
                    else:
                        return productStep.processTime
        else:
            return productStep.processTime

    def adjustAssignmentTime(self, products, productSteps):
        """
        如果考虑第一道工序时间降低25%

        由于在前面计算加工时间时，如果出现第一个产品类型不同的assignment，则它的加工时间默认为产品加工时间
        但在后面可能分配了相同产品类型的assignment，该assignment存在合并加工的可能，因此需要重新检查判断调整产品的加工时间
        由于每加入一个assignment都会进行一次时间的调整检查，因此只需要检查当前加入的resource中最后的两个assignment
            left [-2] 和 right [-1]

            当前资源设备resource的已分配任务assignment的数量 >= 2,需要检查加工时间是否需要重新调整：
                如果left的加工时间已经为0.75processTime，则表明它已经被考虑为合并加工的状态，则不需要再做进一步调整
                如果left的加工时间为processTime，则表明它还未被考虑为合并加工状态，则需要进一步判断：
                    当前right的产品类型与left的产品类型相同时：
                        left的0.75processTime的结束时间点 t1 和 right的产品的上一工序的结束加工时间 t2 的对比
                        如果t1 >= t2:
                            则可以合并加工，对left的加工时间进行调整
                            如果left的同一产品存在后续已经安排的工序，还需要做进一步调整和检查
                        否则，不能合并加工，不需要做进一步调整
                    否则，不能合并加工，不需要做进一步调整

        :param products:
        :param productSteps:
        :return:
        """
        if len(self.assignmentList) <= 1:
            return
        else:
            left_assignment = self.assignmentList[-2]
            right_assignment = self.assignmentList[-1]
            if hhmmss_to_minutes(left_assignment.processDuration) == \
                    0.75 * productSteps[left_assignment.productStepId].processTime:
                return
            else:
                if products[left_assignment.productId].productType == products[right_assignment.productId].productType:
                    t1 = hhmmss_to_minutes(left_assignment.prefixEndTime) + \
                         0.75 * productSteps[left_assignment.productStepId].processTime
                    t2 = hhmmss_to_minutes(productSteps[right_assignment.productStepId].previewStep.isSchedule.endTime)
                    if t1 >= t2:
                        # 则可以合并，需要调整left的加工时间
                        pass
                    else:
                        return

                else:
                    return
