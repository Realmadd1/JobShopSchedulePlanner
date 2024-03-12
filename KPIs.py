

class KPIs:
    def __init__(self):
        self.kpiId = 0
        self.weight = 0.0
        self.value = 0.0
        self.name = ""
        self.unitName = ""
        self.init_value = 1.0

    def set_weight(self, w):
        self.weight = w

    def set_value(self, v):
        self.value = v


class KPI_equipmentUtilization(KPIs):
    def __init__(self, weight):
        super().__init__()
        self.oid = 0
        self.name = "设备利用率"
        self.unitName = "%"
        self.weight = weight

    def calc_value(self):
        self.value = 0.0


class KPI_completionTime(KPIs):
    def __init__(self, weight):
        super().__init__()
        self.oid = 1
        self.name = "完工时间"
        self.unitName = "s"
        self.weight = weight

    def calc_value(self):
        self.value = 0.0

