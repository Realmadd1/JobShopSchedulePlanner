from Util import *
from typing import Optional
import datetime


class Assignment:
    def __init__(self):
        self.assignmentId: str                                                          # 任务id
        self.resourceId: str                                                            # 机器id
        self.productId: str                                                             # 产品id
        self.productStepId: str                                                         # 对应的productStepId
        self.operationType: Optional[str] = None                                        # 工序类型
        self.startTime: datetime = datetime.datetime(2000, 1, 1, 0, 0, 0)               # 开始加工时间
        self.endTime: datetime = datetime.datetime(3000, 1, 1, 0, 0, 0)                 # 结束加工时间
        self.prefixStartTime: datetime = datetime.datetime(2000, 1, 1, 0, 0, 0)         # 换型开始时间
        self.prefixDuration: datetime.timedelta = datetime.timedelta(0)                 # 换型时间 (默认为0)
        self.prefixEndTime: datetime = datetime.datetime(3000, 1, 1, 0, 0, 0)           # 换型结束时间
        self.processStartTime: datetime = datetime.datetime(2000, 1, 1, 0, 0, 0)        # 开始生产时间
        self.processDuration: datetime.timedelta = datetime.timedelta(0)                # 生产时间
        self.processEndTime: datetime = datetime.datetime(3000, 1, 1, 0, 0, 0)          # 结束生产时间
        self.previousAssignment: Optional["Assignment"] = None                          # 这个任务在该设备上的前一个任务

    def calcStartTime(self):
        self.startTime = self.prefixStartTime

    def calcEndTime(self):
        self.endTime = self.processEndTime

    def calcPrefixEndTime(self):
        self.prefixEndTime = self.prefixStartTime + self.prefixDuration

    def calcProcessStartTime(self):
        self.processStartTime = self.prefixEndTime

    def calcProcessEndTime(self):
        self.processEndTime = self.processStartTime + self.processDuration

    def setTime(self, prefixStartTime: datetime, prefixDuration: datetime.timedelta, processDuration: datetime.timedelta):
        self.prefixStartTime = prefixStartTime
        self.prefixDuration = prefixDuration
        self.processDuration = processDuration
        self.calcStartTime()
        self.calcPrefixEndTime()
        self.calcProcessStartTime()
        self.calcProcessEndTime()
        self.calcEndTime()


