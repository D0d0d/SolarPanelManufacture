class Storage:
    def __init__(self,max=1, resources={}, workers=1):
        self.max=max
        self.resources = resources
        self.workers=workers
        self.production_facilities = {}

    def Update(self, resources):
        for key in resources.keys():
            if key in self.resources.keys():
                self.resources[key]+=resources[key]
            else:
                self.resources.update({key:resources[key]})

    def add_production_facility(self, facility,components:{}):
        if facility in self.production_facilities.keys():
            self.production_facilities[facility]+=components
        else:
            self.production_facilities.update({facility:components})

    def remove_production_facility(self, facility):
        if facility in self.production_facilities:
            del self.production_facilities[facility]
