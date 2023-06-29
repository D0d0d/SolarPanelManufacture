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


