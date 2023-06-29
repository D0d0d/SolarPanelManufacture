import re
from copy import copy

from Production import ProductionStage, ProductionFacility
from Supplier import Supplier
from Model import ProductionModel
from Storage import Storage

components = [
                {"name":"chip",     "price":[40,100],       "amount":60},   #кремниевые чипы
                {"name":"glass",    "price":[400,600],      "amount":2},    #стекло
                {"name":"contacts", "price":[30,60],        "amount":50},   #контакты
                {"name":"wires",    "price":[10,80],        "amount":25},   #провода
                {"name":"mounting", "price":[200,400],      "amount":1},    #монтажные элементы: клей/винты/зажимы
                {"name":"frame",    "price":[400,1000],     "amount":1},    #рамки
                {"name": "film",    "price": [40, 100],     "amount": 1},   #упаковочная пленка
                {"name": "box",     "price": [400, 4000],   "amount": 1},   #коробка
             ]

pat =["chip","glass","contacts","wires","mounting","frame"]
#region Инициализация этапов
Assembly1 = ProductionStage(name="Assembly1", time=15, energy=10, production=[{"name":"pannel","amount": 1}],
                            components=[i for i in components if i['name'] in pat],
                            workers=4,
                            quality=True)

Test1 = ProductionStage(name="Test1", time=10, energy=5, production=[{"name":"tested_pannel","amount":1}], components=[{"name":"pannel","amount": 1}], workers=2)

pat =["film","box"]
Package1 = ProductionStage(name="Package1", time=5, energy=1, production=[{"name":"packaged_product","amount": 1}],
                           components=[{"name":"tested_pannel","amount": 5}]
                           +[i for i in components if i['name'] in pat],
                           workers=1,
                            quality=True)

Marking1 = ProductionStage(name="Marking1", time=5, energy=1, production=[{"name":"product","amount": 1}], components=[{"name":"packaged_product","amount": 1}],
                           workers=1)
#endregion
#region Инициализация производственной линии
Line1 = ProductionFacility(name="Line1", stage="first", workers=32)                                                            ############################
Line1.AddStage([Assembly1,Assembly1,Assembly1,Assembly1,Assembly1, Test1,Test1,Test1,Test1,Test1, Package1, Marking1])
Line1.BakeLine()

#endregion
needed = [{'name': 'chip', 'price': [40, 100], 'amount': 960},
          {'name': 'glass', 'price': [400, 600], 'amount': 32},
          {'name': 'contacts', 'price': [30, 60], 'amount': 800},
          {'name': 'wires', 'price': [10, 80], 'amount': 400},
          {'name': 'mounting', 'price': [200, 400], 'amount': 16},
          {'name': 'frame', 'price': [400, 1000], 'amount': 16},
          {'name': 'film', 'price': [40, 100], 'amount': 1},
          {'name': 'box', 'price': [400, 4000], 'amount': 1}]

for i in needed:
    i["amount"]*=2
    i["quality"]=0.9
#region Инициализация поставщика
supplier1 = Supplier(name="Supplier1", time=5, price=5, products=needed)
#endregion
#region Инициализация склада
Storage = Storage(max=50, workers=1)
Storage.add_production_facility(Line1)
#endregion

model = ProductionModel([supplier1],Storage, [Line1])

model.order()
model.delieve()


model.order()
model.delieve()
model.produce()

