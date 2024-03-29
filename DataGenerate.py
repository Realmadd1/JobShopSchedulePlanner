import json
import random
from datetime import datetime


def generate_products():
    products = []
    # 操作工序名称列表
    operation_list = ["Cutting", "Milling", "Drilling", "Grinding", "Welding"]
    typeANum = 3
    typeBNum = 4
    typeCNum = 3
    product_type_list = []
    product_type_list.extend(["A"] * typeANum + ["B"] * typeBNum + ["C"] * typeCNum)
    for i in range(1, productNum + 1):
        product_type = product_type_list.pop(random.randint(0, len(product_type_list) - 1))
        # 使用相同的随机种子确保相同产品类型的操作顺序一致
        random.seed(product_type)
        operation_sequence = operation_list.copy()
        # 每种产品对应一种操作顺序
        random.shuffle(operation_sequence)
        # 加入对应的操作顺序和名称等信息
        sequences = []
        for j, operationType in enumerate(operation_sequence):  # 每个产品有固定的工序数量
            sequences.append({
                "sequenceNr": j + 1,
                "operationType": operationType,
                "operationTypeName": operationType,
                "processTime": random.randint(10, 30),  # 随机生成10到30之间的加工时间
                "timeUnit": "minute"
            })
        products.append({
            "productId": 'P' + str(i).zfill(3),
            "productType": product_type,
            "sequences": sequences
        })

    return products


def generate_random_time():
    # 生成小时、分钟和秒
    hour = 0    # 0
    minute = 0  # 0
    second = 0  # 0

    # 格式化为两位数字符串
    time_str = f"2024-03-10T{hour:02d}:{minute:02d}:{second:02d}"

    return time_str


def generate_resources():
    resources = []
    # 定义工序类型及其对应的工序名称
    operation_types = [
        ("Cutting", "cuttingMachine", "Cutting"),
        ("Milling", "millingMachine", "Milling"),
        ("Drilling", "drillingMachine", "Drilling"),
        ("Grinding", "grindingMachine", "Grinding"),
        ("Welding", "weldingMachine", "Welding")
    ]

    # 确保每个工序2个机器
    for i in range(max(resourceNum, operationNum)):
        operationType, resourceName, operationTypeName = operation_types[i % len(operation_types)]

        # 为每个资源生成唯一的随机startTime
        startTime = generate_random_time()
        resources.append({
            "resourceId": 'R' + str(i+1).zfill(3),  # 资源ID从1开始
            "resourceName": resourceName,
            "operationTypeName": operationTypeName,
            "operationType": operationType,
            "earlyStartTime": startTime
        })

    return resources


# 生成数据
productNum = 10  # 产品数量
resourceNum = 10  # 机器数量
operationNum = 5  # 工序数量

data = {
    "products": generate_products(),
    "resources": generate_resources()
}

# 转换为JSON格式
json_data = json.dumps(data, indent=4)

# 保存到文件
with open('instance.json', 'w') as f:
    json.dump(data, f, indent=4)


