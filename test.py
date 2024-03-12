import gurobipy as gp
from gurobipy import GRB

# 创建一个模型
m = gp.Model("callback_example")

# 创建变量
x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

# 设置变量的目标系数
m.setObjective(x + y + 2*z, GRB.MAXIMIZE)

# 添加约束
m.addConstr(x + 2*y + 3*z <= 4, "c0")
m.addConstr(x + y >= 1, "c1")

# 定义回调函数
def mycallback(model, where):
    if where == GRB.Callback.MIPSOL:
        # 在每次发现一个新的整数可行解时被调用
        sol = model.cbGetSolution([x, y, z])
        print('=================================================================================')
        print(f'Found new integer solution: x={int(sol[0])}, y={int(sol[1])}, z={int(sol[2])}')

# 将回调函数添加到模型中
m.optimize(mycallback)

# 打印最优解
print('Optimal solution:')
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Objective value: {m.objVal}')