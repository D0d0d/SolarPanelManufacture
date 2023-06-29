from Production import ProductionFacility


class Storage:
    def __init__(self,max=1, resources=[], workers=1):
        self.max=max
        self.resources = resources
        self.workers=workers
        self.production_facilities = []

    def Update(self, resources):
        for res in resources:
            if res["name"] in [i["name"] for i in self.resources]:
                next(i for i in self.resources if i["name"]==res["name"])["amount"] += res["amount"]
            else:
                self.storage.append(res)

    def add_production_facility(self, facility):
        self.production_facilities.append(facility)

    def remove_production_facility(self, facility : ProductionFacility):
        if facility in self.production_facilities:
            del self.production_facilities[facility]

    def remove_production_facility(self, facility : int):
     self.production_facilities.pop(facility)