class ProductionModel:
    def __init__(self, suppliers, production_facilities):
        self.suppliers = suppliers
        self.production_facilities = production_facilities

    def delieve(self):
        for supplier in self.suppliers:
            for i,facility in enumerate(self.production_facilities):
                order = supplier.production_facilities[facility]
                self.production_facilities[i].UpdateStorage(order)

    def produce(self):
        for facility in self.production_facilities:
            facility.Produce()