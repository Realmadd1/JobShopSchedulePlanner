import datetime


class ProductStep:
    def __init__(self, **kwargs):
        self.productStepId: str = kwargs["productStepId"]            # 产品步骤id  产品id-步骤工序类型-步骤编号
        self.productId = kwargs["productId"]                    # 产品id
        self.productType = kwargs["productType"]                # 产品类型
        self.operationType = kwargs["operationType"]            # 工序类型
        self.sequenceNr: int = kwargs["sequenceNr"]                  # 加工顺序
        self.processTime: datetime.timedelta = kwargs["processTime"]                # 处理时间
        self.processTimeUnit = kwargs["timeUnit"]               # 处理时间的时间单位
        self.resourcesList = []                                 # 允许加工的机器资源
        self.isSchedule = None                                  # 是否被分配
        self.previousStep = kwargs["previewStep"]                # 前一个产品步骤
        self.routingEarlyStart = 0.0                            # 产品路线中最早可开始加工时间
        self.availableResourceList = []                         # 可获得的机器资源

    # 设置允许加工的机器资源
    def setResourceList(self, resources: dict):
        for resource in resources.values():
            if resource.operationType == self.operationType:
                self.resourcesList.append(resource)

