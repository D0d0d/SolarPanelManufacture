class ProductionModel:
    def __init__(self, suppliers, storage, production_facilities={}):
        self.suppliers = suppliers
        self.production_facilities = production_facilities
        self.storage = storage
        self.total_delievery = {'cost':0, 'time':0}
        self.total_time = 0
        self.total_cost = 0

    def order(self):
        sups = []
        received = {}
        for fac in self.storage.production_facilities:
            order = self.storage.production_facilities[fac]
            for comp in order:
                    for s in [i for i in self.suppliers if comp in i.products.keys()]:
                        if comp not in received.keys():
                            received.update({comp:0})

                        if order[comp]>s.products[comp]['available']:
                            received[comp]+= s.products[comp]['available']
                            s.products[comp]['available']=0
                        else:
                            received[comp]+=order[comp]
                            s.products[comp]['available']-=order[comp]

                        self.total_delievery['cost']+= s.products[comp]['price']*order[comp]
                        if s not in sups:
                            sups.append(s)
                            self.total_delievery['time']+=s.time
                        if (received[comp] == order[comp]): break
        self.storage.Update(received)

    def delieve(self):
        for fac in self.storage.production_facilities:
            order = self.storage.production_facilities[fac]
            for comp in order:
                if (comp in self.storage.resources.keys()) and (self.storage.resources[comp]>=order[comp]) :
                    fac.UpdateStorage({comp:order[comp]})
                    self.storage.Update({comp:-order[comp]})
                else:
                    print('Недостаточно ресурсов для линии '+fac.name)


    def produce(self):
        for facility in self.production_facilities:
            facility.Produce()