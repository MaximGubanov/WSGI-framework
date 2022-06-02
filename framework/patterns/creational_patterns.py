from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject


# абстрактный пользователь
class AbstractUser:
    def __init__(self, name):
        self.name = name


# администратор
class Admin(AbstractUser):
    pass


# персонал
class Staff(AbstractUser):
    pass


# все остальные пользователи
class Buyer(AbstractUser):

    def __init__(self, name):
        self.products = []
        super().__init__(name)


class UserFactory:
    types = {
        'admin': Admin,
        'staff': Staff,
        'buyer': Buyer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип
class ProductPrototype:
    # прототип продуктов

    def clone(self):
        return deepcopy(self)


#  продукт/товар
class Product(ProductPrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.products.append(self)
        self.buyers = []
        super().__init__()

    def __getitem__(self, item):
        return self.buyers[item]

    def add_buyer(self, buyer: Buyer):
        self.buyers.append(buyer)
        buyer.products.append(self)
        self.notify()


# продукт/товар в наличии
class InStockProduct(Product):
    pass


# продукт/товар не в наличии
class OutOfStockProduct(Product):
    pass


class ProductFactory:
    types = {
        'in_stock': InStockProduct,
        'out_of_stock': OutOfStockProduct
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def product_count(self):
        result = len(self.products)
        if self.category:
            result += self.category.products_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.administrators = []
        self.staff = []
        self.buyers = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_product(type_, name, category):
        return ProductFactory.create(type_, name, category)

    def get_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        return None

    def get_buyer(self, name) -> Buyer:
        for item in self.buyers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    # @staticmethod
    def log(self, text):
        print('log--->', text)
        self.writer.write(text)
