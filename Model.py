from gurobipy import *
from Assignment import Assignment


class MIPModel:
    def __init__(self, schPlanner):
        self.model = Model('MIPModel')
        self.data = schPlanner
        # 集合
        self.productLocs = [(j, l) for j in self.data.products for l in range(len(self.data.products[j].productSteps))]
        self.resourceLocs = [(i, k) for i in self.data.resources for k in range(len(self.data.products))]
        self.area = [(j, l, i, k) for j, l in self.productLocs for i, k in self.resourceLocs]
        self.M = 1e05
        self.a = {}
        for j, l in self.productLocs:
            for i in self.data.resources:
                if self.data.products[j].productSteps[l].operationType == self.data.resources[i].operationType:
                    self.a[j, l, i] = 1
                else:
                    self.a[j, l, i] = 0

        # 决策变量
        self.cMax = None  # 连续变量，完成加工时间
        self.x = {}  # x_j,l,i,k 表示任务j的第l道工序是否在机器i的第k个slot加工
        self.y = {}  # y_j,l_i   表示任务j的第l道工序是否在机器i上加工
        self.r = {}  # r_j,l     表示任务j的第l道工序的换型时间
        self.p = {}  # p_j,l     表示任务j的第l道工序的实际加工时间
        self.s = {}  # s_i,k     表示机器i的第k个slot换型开始时间
        self.e = {}  # e_i,k     表示机器i的第k个slot加工结束时间

    # 建立决策变量
    def add_variables(self):
        self.cMax = self.model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1e6, name="cMax")
        for j, l in self.productLocs:
            self.r[j, l] = self.model.addVar(
                vtype=GRB.CONTINUOUS, lb=0,
                ub=self.data.products[j].productSteps[l].processTime * 0.05,
                name="r_{}_{}".format(j, l)
            )

            self.p[j, l] = self.model.addVar(
                vtype=GRB.CONTINUOUS, lb=self.data.products[j].productSteps[l].processTime * 0.75,
                ub=self.data.products[j].productSteps[l].processTime,
                name='p_{}_{}'.format(j, l)
            )

            for i in self.data.resources:
                self.y[j, l, i] = self.model.addVar(vtype=GRB.BINARY, name="y_{}_{}_{}".format(j, l, i))

                for k in range(len(self.data.products)):
                    self.x[j, l, i, k] = self.model.addVar(vtype=GRB.BINARY, name="x_{}_{}_{}_{}".format(j, l, i, k))

        for i in self.data.resources:
            for k in range(len(self.data.products)):
                self.s[i, k] = self.model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=10e6, name="s_{}_{}".format(i, k))
                self.e[i, k] = self.model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=10e6, name="e_{}_{}".format(i, k))

    # 设立目标函数
    def set_objective(self):
        self.model.setObjective(self.cMax, GRB.MINIMIZE)

    # 建立约束
    def add_constraints(self):
        n = len(self.data.products) - 1  # 最后一个机器slot数
        for i in self.data.resources:
            # 完成加工时间约束
            # s_i,n + sum(∀j,l  x_j,l,i,n * (r_j,l + p_j,l)) <= cMax
            self.model.addConstr(
                (self.s[i, n] + quicksum(self.x[j, l, i, n] * (self.r[j, l] + self.p[j, l])
                                         for j, l in self.productLocs) <= self.cMax),
                name="Makespan_Limit_{}".format(i)
            )

        for j, l in self.productLocs:
            # 每个operation都要放入一台机器中
            # sum(∀i y_j,l,i) == 1, ∀j,l
            self.model.addLConstr(quicksum((self.y[j, l, i] for i in self.data.resources)), sense=GRB.EQUAL,
                                  rhs=1, name="slot_operation_Limit_{}_{}".format(j, l)
                                  )

            for i in self.data.resources:
                # 可放入的机器限制
                # y_j, l, i <= a_j, l, i, ∀j,l,i
                self.model.addLConstr(self.y[j, l, i], sense=GRB.LESS_EQUAL, rhs=self.a[j, l, i],
                                      name="resource_Limit_{}_{}_{}".format(j, l, i)
                                      )

                # 当operation放入一台机器操作时，需要在该机器上给它分配一个slot
                # sum(∀k x_j,l,i,k) == y_j, l, i, ∀j,l,i
                self.model.addLConstr(quicksum(self.x[j, l, i, k] for k in range(len(self.data.products))),
                                      sense=GRB.EQUAL, rhs=self.y[j, l, i],
                                      name="operation_slot_Limit_{}_{}".format(j, l)
                                      )

                # 每台机器的第一个slot的operation没有换型时间
                # r_j,l <= (1 - x_j,l,i,1) * M, ∀i,j,l
                self.model.addLConstr(
                    self.r[j, l], sense=GRB.LESS_EQUAL, rhs=(1 - self.x[j, l, i, 0]) * self.M,
                    name="first_fix_typeTime_limit_{}_{}_{}".format(j, l, i)
                )

                # 每台机器的第一个slot的operation的加工时间为1个processTime
                self.model.addLConstr(
                    self.p[j, l], sense=GRB.GREATER_EQUAL,
                    rhs=self.x[j, l, i, 0] * self.data.products[j].productSteps[l].processTime,
                    name="first_processTime_limit_{}_{}_{}".format(j, l, i)
                )

            # 对每个任务的每个工序开始加工时间限制
            # sum(∀i, k x_j,l,i,k * s_i,k) + r_j,l + p_j,l <= sum(∀i, k x_j,l+1,i,k * s_i,k) ,∀j,l (l != m)
            if l != len(self.data.products[j].productSteps) - 1:
                self.model.addConstr(
                    quicksum(self.x[j, l, i, k] * self.s[i, k] for i, k in self.resourceLocs) + self.r[j, l] +
                    self.p[j, l] <= quicksum(self.x[j, l + 1, i, k] * self.s[i, k] for i, k in self.resourceLocs),
                    name="product_operation_start_time_limit_{}_{}".format(j, l)
                )



        for i, k in self.resourceLocs:
            if k != len(self.data.products) - 1:
                # 每台机器的slot的对称性破坏
                # sum(∀j,l x_j,l,i,k) >= sum(∀j,l x_j,l,i,k+1) ∀i, k, (k != n)
                self.model.addLConstr(
                    quicksum(self.x[j, l, i, k] for j, l in self.productLocs), sense=GRB.GREATER_EQUAL,
                    rhs=quicksum(self.x[j, l, i, k + 1] for j, l in self.productLocs),
                    name="slot_broken_limit_{}_{}".format(i, k)
                )

                # 每台机器的每个slot的开始加工时间限制
                # s_i,k + sum(∀j,l x_j,l,i,k *(r_j,l + p_j,l))<= s_i,k+1 , ∀i, k, (k != n)
                self.model.addConstr(
                    (self.s[i, k] + quicksum(self.x[j, l, i, k] * (self.r[j, l] + self.p[j, l])
                                             for j, l in self.productLocs) <= self.s[i, k + 1]),
                    name="slot_start_time_limit_{}_{}".format(i, k)
                )

            # 每台机器的每个slot至多放入一个operation
            # sum(∀j,l x_j,l,i,k) <= 1, ∀i,k
            self.model.addLConstr(
                quicksum(self.x[j, l, i, k] for j, l in self.productLocs), sense=GRB.LESS_EQUAL,
                rhs=1, name="slot_operation_Limit_{}_{}".format(i, k)
            )
            # 中间变量表示，每台机器的每个slot上完成加工的时间点
            # s_i,k + sum(∀j,l x_j,l,i,k * (r_j,l+p_j,l) = e_i,k, ∀i, k
            self.model.addConstr(self.s[i, k] + quicksum(self.x[j, l, i, k] * (self.r[j, l] + self.p[j, l])
                                                         for j, l in self.productLocs) == self.e[i, k],
                                 name="resource_slot_endTime_limit_{}_{}".format(i, k)
                                 )

        for j, l in self.productLocs:
            for f, q in self.productLocs:
                for i, k in self.resourceLocs:
                    if k != 0:
                        if self.data.products[j].productType != self.data.products[f].productType:
                            self.model.addLConstr(
                                self.r[j, l], sense=GRB.GREATER_EQUAL,
                                rhs=(self.x[j, l, i, k] + self.x[f, q, i, k-1] - 2) * self.M +
                                    0.05 * self.data.products[j].productSteps[l].processTime,
                                name="Prefix_Time_Limit_{}_{}_{}_{}_{}_{}".format(j, l, f, q, i, k)
                            )

                        else:
                            self.model.addLConstr(
                                self.p[j, l], sense=GRB.GREATER_EQUAL,
                                rhs=self.data.products[j].productSteps[l].processTime -
                                    (2 - self.x[j, l, i, k] - self.x[f, q, i, k-1]) * self.M -
                                    (self.s[i, k] - self.e[i, k-1]) * self.M,
                                name="Process_Time_Limit_{}_{}_{}_{}_{}_{}".format(j, l, f, q, i, k)
                            )

        self.model.update()

    def outPutSol(self):
        assignments = {}
        assignmentId = 0
        for j, l in self.productLocs:
            productStep = self.data.products[j].productSteps[l]
            for i in self.data.resources:
                if self.y[j, l, i].x > 0.9:
                    for k in range(len(self.data.products)):
                        if self.x[j, l, i, k].x > 0.9:
                            assignment = Assignment()
                            assignment.assignmentId = assignmentId
                            assignment.resourceId = i
                            assignment.productId = j
                            assignment.productStepId = productStep.productStepId
                            assignment.operationType = productStep.operationType
                            assignment.calcTime(self.s[i, k].x, self.r[j, l].x, self.p[j, l].x)
                            productStep.isSchedule = assignment
                            assignments[assignmentId] = assignment
                            assignmentId += 1
        return assignments

    def solve(self):
        self.add_variables()
        self.set_objective()
        self.add_constraints()
        self.model.Params.OutputFlag = 1
        self.model.setParam('TimeLimit', 10)
        self.model.optimize()
        assignments = self.outPutSol()
        # self.model.computeIIS()
        # self.model.write("model.ilp")
        # self.model.write('model.lp')
        return assignments



