import string
from copy import copy, deepcopy


class ProductionStage:
    def __init__(self, name, time, energy, production, components, workers, quality=False):
        '''
        :param name: Название этапа
        :param time: Время необходимое на выполнение работы
        :param energy: Объем затрачиваемой энергии
        :param production: Объем производимой продукции
        :param workers: минимальное число работников
        :param components: необходимые компоненты
        '''
        self.name = name
        self.time = time
        self.energy = energy
        self.production = production
        self.workers = workers
        self.components = components
        self.quality = quality


class ProductionFacility:
    iter = 0

    def __init__(self, name: string, stage, production_time=0.0, workers=0, delievery_time=0.0, delievery_cost=0.0):
        '''
        :name name: название
        :param stage: этап производства
        :param production_time: время производства
        :param production_volume: объем производства
        :param workers: выделенное количество работников
        :param components: необходимые компоненты
        :param production: ожидамый результат {dict}
        '''
        self.stages = []
        self.storage = []
        self.production = []
        self.available_workers = 0
        self.energy = 0
        self.energy_used = 0
        self.time_used = 0
        self.name = name
        self.production_time = production_time
        self.available_workers = workers
        self.stage = stage
        self.isStart = 0
        print(f"Создана линия производства: {self.name}\n")

    def SetDependencies(self, end):
        self.isStart = 1
        self.end = end

    def SetDependencies(self, start, end):
        self.isStart = 2
        self.start = start
        self.end = end

    def AddStage(self, stage):
        self.stages += stage

    def BakeLine(self):
        self.workers = 0
        self.components = []
        s=0
        stages_count = len(self.stages)
        while s<stages_count:
            buf = True
            stage = self.stages[s]
            for comp in stage.components:
                if comp['name'] in [i['name'] for i in self.production]:
                    stored_production = next(i for i in self.production if i['name'] == comp['name'])
                    if stored_production['amount'] > 0:
                        stored_production['amount'] -= comp['amount']
                        if stored_production['amount'] < 0:
                            stored_production['amount'] += comp['amount']
                            s -= 1
                            buf=False
                            break
                    else:
                        s -= 1
                        buf = False
                        break
                else:
                    if comp['name'] in [i['name'] for i in self.components]:
                        stored_comp = next(i for i in self.components if i['name'] == comp['name'])
                        stored_comp['amount']+=comp['amount']
                    else:
                        self.components.append(copy(comp))
            if buf:
                for prod in stage.production:
                    if prod['name'] in [i['name'] for i in self.production]:
                        next(i for i in self.production if i['name']==prod['name'])['amount']+=prod['amount']
                    else:
                        self.production.append(copy(prod))
                self.available_workers -= stage.workers
                self.workers += stage.workers
                self.production_time += stage.time
                self.energy += stage.energy
                s+=1


        if all(prod['amount']>=0 for prod in self.production):
            self.Working = True
            self.storage.clear()
            self.production = [i for i in self.production if i["amount"] > 0]
            print(f"Линия <<{self.name}>> собрана! \n")
        else:
            self.Working = False
            print(f"Линия <<{self.name}>> сломана! \n")

        print(
            f"Время производства: {self.production_time} \n"
            f"Необходимые компоненты: {self.components}\n"
            f"Энергопотребление: {self.energy}\n"
            f"Выход продукции: {self.production} \n"
            f"Работающие сотрудники: {self.workers} \n"
            f"Незанятые сотрудники: {self.available_workers} \n\n")

    def UpdateStorage(self, resources):
        for res in resources:
            if res["name"] in [i["name"] for i in self.storage]:
                next(i for i in self.storage if i["name"] == res["name"])["amount"] += res["amount"]
            else:
                self.storage.append(res)

    def Produce(self):
        names = [i["name"] for i in self.components]
        quality = 1
        while any([stored["amount"] - need["amount"] >= 0 for stored, need in
                   zip([j for j in self.storage if j["name"] in names],
                       [k for k in self.components if k["name"] in names])]):
            for need in self.components:
                stored = next(i for i in self.storage if i["name"] == need["name"])
                stored["amount"] -= need["amount"]
                quality=min(quality,stored["quality"])
            for prod in self.production:
                produced = copy(prod)
                produced['quality']=min(quality, produced["quality"])
                print(produced['quality'])
                if produced["name"] in [i["name"] for i in self.storage]:
                    stored_prod = next(i for i in self.storage if i["name"] == produced["name"])
                    if (produced['quality']==stored_prod['quality']):
                        stored_prod["amount"] += produced["amount"]
                    else:
                        self.storage.append(produced)
                else:
                    self.storage.append(copy(produced))
            self.energy_used += self.energy
            self.time_used += self.production_time
            self.storage = [i for i in self.storage if i["amount"] > 0]

        print(f"Ресурсы закончились! Выход производства: {self.storage}\n"
              f"Затрачено {self.energy_used} энергии и {self.time_used} времени ")
