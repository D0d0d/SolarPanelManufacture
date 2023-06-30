import re
from copy import copy, deepcopy

from Production import ProductionStage, ProductionFacility
from Supplier import Supplier
from Model import ProductionModel
from Storage import Storage

repeat = 5
components = [
                {"name":"chip",     "price":[40,100],       "amount":300},   #кремниевые чипы
                {"name":"glass",    "price":[400,600],      "amount":10},    #стекло
                {"name":"contacts", "price":[30,60],        "amount":250},   #контакты
                {"name":"wires",    "price":[10,80],        "amount":125},   #провода
                {"name":"mounting", "price":[200,400],      "amount":5},    #монтажные элементы: клей/винты/зажимы
                {"name":"frame",    "price":[400,1000],     "amount":5},    #рамки
                {"name": "film",    "price": [40, 100],     "amount": 1},   #упаковочная пленка
                {"name": "box",     "price": [400, 4000],   "amount": 1},   #коробка
             ]

pat =["chip","glass","contacts","wires","mounting","frame"]
#region Инициализация этапов
Assembly1 = ProductionStage(name="Assembly1", time=15, energy=10, production=[{"name":"pannel","amount": 5, "quality":1}],
                            components=[i for i in components if i['name'] in pat],
                            workers=4,
                            quality=True)

Test1 = ProductionStage(name="Test1", time=10, energy=5, production=[{"name":"tested_pannel","amount":5, "quality":1}], components=[{"name":"pannel","amount": 5}], workers=2)

pat =["film","box"]
Package1 = ProductionStage(name="Package1", time=5, energy=1, production=[{"name":"packaged_product","amount": 1, "quality":1}],
                           components=[{"name":"tested_pannel","amount": 5}]
                           +[i for i in components if i['name'] in pat],
                           workers=1,
                            quality=True)

Marking1 = ProductionStage(name="Marking1", time=5, energy=1, production=[{"name":"product","amount": 1, "quality":1}], components=[{"name":"packaged_product","amount": 1}],
                           workers=1)
#endregion
#region Инициализация производственной линии
Line1 = ProductionFacility(name="Line1", stage="first", workers=20)                                                            ############################
Line1.AddStage([Assembly1])
Line1.BakeLine()
Line2 = ProductionFacility(name="Line2", stage="second", workers=20)
Line2.AddStage([Test1])
Line2.BakeLine()
Line3 = ProductionFacility(name="Line3", stage="third", workers=20)                                                            ############################
Line3.AddStage([Package1])
Line3.BakeLine()
Line4 = ProductionFacility(name="Line4", stage="fourth", workers=20)
Line4.AddStage([Marking1])
Line4.BakeLine()
#endregion

needed = [{'name': 'chip', 'price': [40, 100], 'amount': 300},
          {'name': 'glass', 'price': [400, 600], 'amount': 10},
          {'name': 'contacts', 'price': [30, 60], 'amount': 250},
          {'name': 'wires', 'price': [10, 80], 'amount': 125},
          {'name': 'mounting', 'price': [200, 400], 'amount': 5},
          {'name': 'frame', 'price': [400, 1000], 'amount': 5},
          {'name': 'film', 'price': [40, 100], 'amount': 1},
          {'name': 'box', 'price': [400, 4000], 'amount': 1}]

for i in needed:
    i["amount"]*=repeat
    i["quality"]=0.9
#region Инициализация поставщика
supplier1 = Supplier(name="Supplier1", time=5, price=5, products=needed)
#endregion
#region Инициализация склада
Storage = Storage(max=50, workers=1)
Storage.add_production_facility(Line1)
Storage.add_production_facility(Line2)


Storage.add_production_facility(Line3)
Storage.add_production_facility(Line4)



#endregion

model = ProductionModel([supplier1],Storage,
                        [Line1,Line2,
                         Line3,Line4])


model.order()
model.delieve()
model.produce()

model.order()
model.delieve()
model.produce()
