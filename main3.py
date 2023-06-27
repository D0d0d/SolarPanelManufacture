from Production import ProductionStage, ProductionFacility
from Supplier import Supplier
from Model import ProductionModel
from Storage import Storage
#region Инициализация этапов
Assembly1 = ProductionStage(name="Assembly1", time=15, energy=10, production={"raw": 6}, components={"comp1": 6},
                            workers=4)

Test1 = ProductionStage(name="Test1", time=10, energy=5, production={"tested": 5}, components={"raw": 5}, workers=2)

Package1 = ProductionStage(name="Package1", time=5, energy=1, production={"packaged": 5}, components={"tested": 5},
                           workers=1)

Marking1 = ProductionStage(name="Marking1", time=5, energy=1, production={"product": 5}, components={"packaged": 5},
                           workers=1)
#endregion
#region Инициализация производственной линии
Line1 = ProductionFacility(name="Line1", stage="first", workers=10)
Line1.AddStage([Assembly1, Test1, Package1, Marking1])
Line1.BakeLine()
#endregion
#region Инициализация поставщика
supplier1 = Supplier(name="Supplier1", time=5, price=5, products={"comp1": {'price':5, 'available':60}})
#endregion
#region Инициализация склада
Storage = Storage(max=50, workers=1)
Storage.add_production_facility(Line1, {"comp1": 25})
#endregion

model = ProductionModel({supplier1},Storage, [Line1])
model.order()
model.delieve()
model.produce()

