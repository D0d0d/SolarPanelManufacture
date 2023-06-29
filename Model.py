from copy import copy


class ProductionModel:
    def __init__(self, suppliers, storage, production_facilities=[]):
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
                order = fac.components
                for comp in order:
                    for supplier in [i for i in self.suppliers if comp["name"] in [j["name"] for j in i.products]]:

                        available = next(i for i in supplier.products if i["name"]==comp["name"])

                        if available["name"] not in [i["name"] for i in received]:
                            receive = copy(available)
                            receive['amount']=0
                            received.append(receive)
                        recieve = next(i for i in received if i["name"]==comp["name"])

                        take = 0
                        if comp["amount"]>=(available['amount']+recieve["amount"]):
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
            for rec in received:
                if rec["name"] in [i['name'] for i in self.storage.resources]:
                    stored = next(i for i in self.storage.resources if i['name']==rec['name'])
                    stored['quality']=(stored['quality']*stored['amount']+rec['quality']*rec['amount'])/(stored['amount']+rec['amount'])
                    stored['amount']+=rec['amount']
                else:
                    self.storage.resources.append(rec)

    def delieve(self):
        for fac in self.storage.production_facilities:
            order = fac.components

            for comp in order:
                if (comp["name"] in [i["name"] for i in self.storage.resources]) and \
                        (next(i for i in self.storage.resources if i["name"]==comp["name"])["amount"]>=comp["amount"]):
                        have = copy(next(i for i in self.storage.resources if i["name"]==comp["name"]))
                        fac.UpdateStorage([have])

                        have=copy(have)
                        have["amount"]*=-1

                        self.storage.Update(copy([have]))
                else:
                    print('Недостаточно ресурсов для линии '+fac.name)
                    break


    def produce(self):
        for facility in self.production_facilities:
            facility.Produce()