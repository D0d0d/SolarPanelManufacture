class Storage:
    def __init__(self,max=1, resources={}, workers=1):
        self.max=max
        self.resources = resources
        self.workers=workers

    def Update(self, resources):
        for key in resources.keys():
            if key in self.resources.keys():
                self.resources[key]+=resources[key]
            else:
                self.resources.update({key:resources[key]})
