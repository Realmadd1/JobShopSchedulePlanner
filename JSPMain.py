from JobShopSchedulePlanner import JobShopSchedulePlanner

# 定义全局变量
schPlanner = None


def set_global_variable(value):
    global schPlanner
    schPlanner = value


def get_global_variable():
    return schPlanner


if __name__ == '__main__':
    path = "instance.json"

    # 求解类型
    # 1 MIPModel求解
    # 2 启发式规则求解

    planner = JobShopSchedulePlanner()
    planner.run(path=path, solveType=2)





