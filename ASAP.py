from datetime import datetime, timedelta

from Assignment import Assignment
from Util import *


class ASAPMethod:
    def __init__(self, schPlanner):
        self.data = schPlanner
        self.assignments = {}

    def run(self):
        while True:
            # 找当前productRoutine中的第一个需要完成的productStep
            waitAssign = self.productRoutineOfFirstProductStep()
            if not waitAssign:
                # 如果没有，则分配结束
                break
            # waitAssign中的productStep可以分配给哪些Resource
            waitResources = self.productStepToResource(waitAssign)
            # 找到waitResources中最早空闲的机器
            resource = self.getEarlyResource(waitResources)
            # 找到resource中处理时间最短的productStep
            productStep = self.getShortestProductStep(waitResources[resource])
            # 将productStep分配给resource
            self.createAssignment(resource, productStep)
        return self.assignments

    def productRoutineOfFirstProductStep(self):
        # 找当前productRoutine中的第一个需要完成的productStep
        waitAssign = []
        for product in self.data.products.values():
            for productStep in product.productSteps:
                if not productStep.isSchedule:
                    waitAssign.append(productStep)
                    break
        return waitAssign

    def productStepToResource(self, waitAssign):
        # waitAssign中的productStep可以分配给哪些Resource
        waitResources = {resource: [] for resource in self.data.resources.values()}
        for productStep in waitAssign:
            for resource in productStep.resourcesList:
                waitResources[resource].append(productStep)
        # 将Resource按照可以分配的productStep的数量升序排序
        waitResources = {key: value for key, value in waitResources.items() if value}
        sortedWaitResources = dict(sorted(waitResources.items(), key=lambda x: len(x[1])))
        return sortedWaitResources

    @staticmethod
    def getEarlyResource(waitResources):
        earlyResource = None
        for resource in waitResources:
            resource.calcEarlyAvailableTime()
            if not earlyResource:
                earlyResource = resource
                continue
            if resource.earlyAvailableTime < earlyResource.earlyAvailableTime:
                earlyResource = resource
        return earlyResource

    @staticmethod
    def getShortestProductStep(productStepList):
        shortestProductStep = None
        for productStep in productStepList:
            if not shortestProductStep:
                shortestProductStep = productStep
                continue
            if productStep.processTime < shortestProductStep.processTime:
                shortestProductStep = productStep
        return shortestProductStep

    def createAssignment(self, resource, productStep):
        # 将处理时间最短的productStep分配给最早空闲的Resource
        assignment = Assignment()
        assignment.assignmentId = len(self.assignments)
        assignment.resourceId = resource.resourceId
        assignment.productId = productStep.productId
        assignment.productStepId = productStep.productStepId
        assignment.operationType = resource.operationType
        if productStep.previousStep:
            preTime = productStep.previousStep.isSchedule.endTime
        else:
            preTime = datetime(2000, 1, 1, 0, 0, 0)
        startTime = max(resource.earlyAvailableTime, preTime)
        prefixDuration = resource.calcPrefixDuration(productStep, self.data.products)
        processDuration = resource.calcProcessDuration(productStep, self.data.products)
        assignment.setTime(startTime, prefixDuration, processDuration)
        # 更新相关变量
        self.assignments[assignment.assignmentId] = assignment
        resource.assignmentList.append(assignment)
        productStep.isSchedule = assignment















