import string
class ProductionStage:
    def __init__(self,name, time, energy,production,components, workers):
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


class ProductionFacility:


    def __init__(self, name:string, stage, production_time=0.0, workers=0):
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
        self.storage = {}
        self.production = {}
        self.available_workers = 0
        self.energy=0
        self.energy_used=0
        self.time_used=0
        self.name = name
        self.production_time = production_time
        self.available_workers = workers
        self.stage = stage
        self.isStart = 0
        print(f"Создана линия производства: {self.name}\n")

    def SetDependencies(self,end):
        self.isStart = 1
        self.end = end

    def SetDependencies(self, start, end):
        self.isStart = 2
        self.start = start
        self.end = end

    def AddStage(self,stage):
        self.stages+=stage

    def BakeLine(self):
        self.workers=0
        self.componetns = {}
        for stage in self.stages:
            for key in stage.components.keys():
                if key in self.storage.keys():
                    if  self.storage[key]-stage.components[key]<0:
                        self.componetns.update({key:-1*self.storage[key]-stage.components[key]})
                        self.storage[key]=0
                    else:
                        self.storage[key]-=stage.components[key]
                else:
                    self.componetns.update({key:stage.components[key]})

            for key in stage.production.keys():
                if key in self.storage.keys():
                    self.storage[key]+=stage.production[key]
                else:
                    self.storage.update({key:stage.production[key]})

            self.available_workers-=stage.workers
            self.workers+=stage.workers
            self.production_time+=stage.time
            self.energy+=stage.energy

        if all(val>=0 for val in self.storage.values()):
            self.Working=True
            self.production.update(self.storage)
            self.storage.clear()

            print(f"Линия <<{self.name}>> собрана! \n")
        else:
            self.Working=False
            print(f"Линия <<{self.name}>> сломана! \n")
        print(
              f"Время производства: {self.production_time} \n"
              f"Необходимые компоненты: {self.componetns}\n"
              f"Энергопотребление: {self.energy}\n"
              f"Выход продукции: {self.production} \n"
              f"Работающие сотрудники: {self.workers} \n"
              f"Незанятые сотрудники: {self.available_workers} \n\n")

    def UpdateStorage(self, resources):
        for key in resources.keys():
            if key in self.storage.keys():
                self.storage[key]+=resources[key]
            else:
                self.storage.update({key:resources[key]})


    def Produce(self):
        while all(self.storage[key]-self.componetns[key]>=0 for key in self.componetns.keys()):
            for key in self.componetns.keys():
                self.storage[key]-=self.componetns[key]
                for prod in self.production.keys():
                    if prod in self.storage.keys():
                        self.storage[prod]+=self.production[prod]
                    else:
                        self.storage.update({prod:self.production[prod]})
            self.energy_used+=self.energy
            self.time_used+=self.production_time
        print(f"Ресурсы закончились! Выход производства: {self.storage}\n"
              f"Затрачено {self.energy_used} энергии и {self.time_used} времени ")
        self.production_time=0
        self.time_used=0
