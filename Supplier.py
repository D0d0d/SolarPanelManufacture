class Supplier:
    def __init__(self, name,time,price, products):
        '''
        :param name: наименование поставщика
        :param time: время доставкки
        :param price: стоимость доставки
        :param products: имеющийся товар
        '''
        self.name = name
        self.time = time
        self.price = price
        self.products = products
        self.production_facilities = {}  # Список производственных установок, связанных с поставщиком

    def add_production_facility(self, facility,order:{}):
        if (key in self.products for key in order.keys()):
            if facility in self.production_facilities.keys():
                self.production_facilities[facility]+=order
            else:
                self.production_facilities.update({facility:order})
        else:
            raise RuntimeError(f'Заказ неверен! {self.name}\n')

    def remove_production_facility(self, facility):
        if facility in self.production_facilities:
            del self.production_facilities[facility]
