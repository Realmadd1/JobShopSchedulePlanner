from Util import *


class Assignment:
    def __init__(self):
        self.assignmentId = int()                   # 任务id
        self.resourceId = int()                     # 机器id
        self.productId = int()                      # 产品id
        self.productStepId = int()                  # 对应的productStepId
        self.operationType = None                   # 工序类型
        self.startTime = ""                         # 开始加工时间
        self.endTime = ""                           # 结束加工时间
        self.prefixStartTime = ""                   # 换型开始时间
        self.prefixDuration = ""                    # 换型时间 (默认为0)
        self.prefixEndTime = ""                     # 换型结束时间

        self.processStartTime = ""                      # 开始生产时间
        self.processEndTime = ""                        # 结束生产时间
        self.processDuration = ""                   # 生产时间
        self.previous = None                        # 这个任务在该设备上的前一个任务

    def calcStartTime(self):
        self.startTime = self.prefixStartTime

    def calcEndTime(self):
        self.endTime = self.processEndTime

    def calcPrefixEndTime(self):
        self.prefixEndTime = self.prefixStartTime + self.prefixDuration


    def calcTime(self, startTime, prefixDuration, processDuration):
        self.startTime = minutes_to_timestamp(startTime)
        self.prefixStartTime = self.startTime
        self.prefixDuration = minutes_to_hhmmss(prefixDuration)
        self.prefixEndTime = minutes_to_timestamp(startTime + prefixDuration)
        self.processStart = self.prefixEndTime
        self.processDuration = minutes_to_hhmmss(processDuration)
        self.processEnd = minutes_to_timestamp(startTime + prefixDuration + processDuration)
        self.endTime = self.processEnd


