import time

from Product import *
from ProductStep import *
from Resource import *
from KPIs import *
from Plot import draw
from Model import MIPModel
from ASAP import ASAPMethod

import json


class JobShopSchedulePlanner:
    def __init__(self):
        self.input_data = None          # 输入数据
        self.optimized_parameter = {}   # 优化参数
        self.resources = {}             # 机器集合
        self.products = {}              # 产品集合
        self.productSteps = {}          # 产品步骤集合
        self.assignments = {}           # 任务集合
        self.sol = None                 # 输出结果

    # 读取数据
    def read_data(self, PATH):
        with open(PATH, 'r', encoding='utf-8-sig') as fp:
            self.input_data = json.loads(fp.read())  # 转化为字典格式

    def sync_data(self):
        # 优化参数
        self.optimized_parameter["equipmentUtilization"] = KPI_equipmentUtilization(
            self.input_data["parameters"]["equipmentUtilizationWeight"])  # 优化参数：设备利用率
        self.optimized_parameter["completionTime"] = KPI_completionTime(
            self.input_data["parameters"]["completionTimeWeight"])          # 优化参数：整体完成时间
        # 产品
        productsDetail = self.input_data["products"]
        productStepId = 1
        for productDetail in productsDetail:
            product = Product(productId=productDetail["productId"], productType=productDetail["productType"])
            self.products[product.productId] = product
            previewStep = None
            for productStepDetail in productDetail["sequences"]:
                productStep = ProductStep(
                    productStepId=productStepId, operationType=productStepDetail["operationType"],
                    productId=productDetail["productId"], productType=productDetail["productType"],
                    sequenceNr=productStepDetail["sequenceNr"], processTime=productStepDetail["processTime"],
                    timeUnit=productStepDetail["timeUnit"], previewStep=previewStep
                )
                self.productSteps[productStep.productStepId] = productStep
                product.add_product_step(productStep)  # 将产品步骤对象加入产品对象中
                productStepId += 1
                previewStep = productStep

        # 设备资源
        resourcesDetail = self.input_data["resources"]
        for resourceDetail in resourcesDetail:
            resource = Resource(
                resourceId=resourceDetail["resourceId"], resourceName=resourceDetail["resourceName"],
                operationType=resourceDetail["operationType"], operationTypeName=resourceDetail["operationTypeName"],
                earlyStartTime=resourceDetail["startTime"]
            )
            self.resources[resource.resourceId] = resource

        # 为每个productStep设置resource资源
        for productStep in self.productSteps.values():
            productStep.setResourceList(self.resources)

    def MIPModelSolve(self):
        globalModel = MIPModel(self)
        self.assignments = globalModel.solve()
        print(self.assignments)

    def ASAPMethodSolve(self):
        asapMethod = ASAPMethod(self)
        self.assignments = asapMethod.run()
        print(self.assignments)

    def plot(self):
        draw(self, self.assignments)

    def run(self, path, solveType):
        print("=================================开始读取数据======================================================")
        start = time.time()
        self.read_data(path)
        self.sync_data()
        print("=================================完成数据读取======================================================")
        print("数据读取耗时：", time.time() - start)
        print("=================================尝试使用方法", solveType, "进行求解================================")
        start = time.time()
        if solveType == 1:
            self.MIPModelSolve()
        elif solveType == 2:
            self.ASAPMethodSolve()
        print("=================================获得任务分配======================================================")
        print("任务分配耗时：", time.time() - start)
        print("===================================开始画图========================================================")
        self.plot()

