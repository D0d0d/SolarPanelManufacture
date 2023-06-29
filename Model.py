from copy import copy


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
        received = []
        for fac in self.storage.production_facilities:
            order = self.storage.production_facilities[fac]
            for comp in order:
                for supplier in [i for i in self.suppliers if comp["name"] in [j["name"] for j in i.products]]:
                    supply = next(i for i in supplier.products if i["name"]==comp["name"])
                    if comp["name"] not in [i["name"] for i in received]:
                        receive = copy(supply)
                        receive['amount']=0
                        received.append(receive)
                    available = next(i for i in supplier.products if i["name"]==comp["name"])
                    recieve = next(i for i in received if i["name"]==comp["name"])
                    take = 0
                    if comp["amount"]>(available['amount']+recieve["amount"]):
                        receive['quality']=(receive['quality']*recieve["amount"]+available['quality']*available["amount"])/(recieve["amount"]+available["amount"])
                        take = copy(available['amount'])
                        recieve["amount"]+= take
                        available['amount']=0

                    else:
                        take = comp["amount"]-recieve["amount"]
                        receive['quality'] = (receive['amount']*recieve['quality']+take*available['quality'])/(take+receive["amount"])
                        recieve["amount"]+=take
                        available['amount']-=take
                    self.total_delievery['cost']+= available['price'][0]*take ######################
                    if supplier not in sups:
                        sups.append(supplier)
                        self.total_delievery['time']+=supplier.time
                    if (receive["amount"] == comp["amount"]): break
        self.storage.resources+=received

    def delieve(self):
        for fac in self.storage.production_facilities:
            order = self.storage.production_facilities[fac]
            for comp in order:
                if (comp["name"] in [i["name"] for i in self.storage.resources]) and \
                        (next(i for i in self.storage.resources if i["name"]==comp["name"])["amount"]>=comp["amount"]):
                        have = next(i for i in self.storage.resources if i["name"]==comp["name"])
                        fac.UpdateStorage([have])
                        self.storage.Update([have])
                else:
                    print('Недостаточно ресурсов для линии '+fac.name)


    def produce(self):
        for facility in self.production_facilities:
            facility.Produce()