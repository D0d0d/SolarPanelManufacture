from copy import copy


class ProductionModel:
    def __init__(self, suppliers, storage, production_facilities=[]):
        self.suppliers = suppliers
        self.production_facilities = production_facilities
        self.storage = storage
        self.total_delievery = {'cost':0, 'time':0}
        self.total_time = 0
        self.total_cost = 0
        self.produced =[]

    def order(self):
        try:
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
                            received.append(copy(receive))
                        recieve = next(i for i in received if i["name"]==comp["name"])

                        take = 0
                        if comp["amount"]>=(available['amount']+recieve["amount"]):
                            receive['quality']=(receive['quality']*recieve["amount"]+available['quality']*available["amount"])/(recieve["amount"]+available["amount"])
                            take = copy(available['amount'])
                            recieve["amount"]+= take
                            available['amount']=0
                        else:
                            take = comp["amount"]#-recieve["amount"]
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
        except:
            print("У продавца нет нужного ресурса!")

    def delieve(self):
        for i,fac in enumerate(self.storage.production_facilities):
            order = fac.components
            for comp in order:
                #print(next(i for i in self.storage.resources if i['name']==comp['name']))
                if (comp["name"] in [i["name"] for i in self.storage.resources]) and \
                        (next(i for i in self.storage.resources if i["name"]==comp["name"])["amount"]>=comp["amount"]):
                        have = next(i for i in self.storage.resources if i["name"]==comp["name"])
                        send = copy(comp)
                        send['quality']=have['quality']
                        fac.UpdateStorage([send])

                        have["amount"]-=send['amount']

                else:
                    try:
                        if  comp['name'] in [i['name'] for i in self.storage.production_facilities[i-1].production]:
                            pass
                        else:
                            print('Недостаточно ресурсов для линии 1 ',fac.name, comp['name'] )
                            break
                    except:
                        print('Недостаточно ресурсов для линии 2 ', fac.name)
                        break

    def produce(self):
        amount_facilities = len(self.production_facilities)
        cur=0
        while cur<amount_facilities-1:
            result = self.production_facilities[cur].Produce()
            for res in result['products']:
                if res['name'] in [i['name'] for i in self.production_facilities[cur+1].storage]:
                    next(i for i in self.production_facilities[cur+1].storage if i['name']==res['name'])['amount']+=res['amount']
                else:
                    self.production_facilities[cur+1].storage.append(res)
            cur+=1
        final_stage = self.production_facilities[amount_facilities-1]
        result = final_stage.Produce()
        final_stage.storage=[]
        for prod in result["products"]:
            if prod['name'] in [i['name'] for i in self.produced]:
                next(i for i in self.produced if i['name']==prod['name'])['amount']+=prod['amount']
            else:
                self.produced.append(copy(prod))
        print(self.produced)
