from typing import List
from ProductStep import ProductStep
import datetime


class Product:
    def __init__(self, **kwarg):
        self.productId = kwarg["productId"]             # 产品id
        self.productType = kwarg["productType"]         # 产品类型
        self.productSteps: List[ProductStep] = []       # 产品工序
        self.planStartTime = datetime.datetime.min      #
        self.planEndTime = datetime.datetime.max        # 产品完工时间

    def add_product_step(self, productStep):
        self.productSteps.append(productStep)






