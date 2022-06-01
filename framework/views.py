from datetime import date

from simba_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug


site = Engine()
logger = Logger('main')
routes = {}


# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список продуктов
@AppRoute(routes=routes, url='/products-list/')
class ProductsList:
    @Debug(name='ProductList')
    def __call__(self, request):
        logger.log('Список продуктов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            logger.log(category)
            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No products have been added yet'


# контроллер - создать продукт
@AppRoute(routes=routes, url='/create-product/')
class CreateProduct:
    category_id = -1

    @Debug(name='CreateProduct')
    def __call__(self, request):
        logger.log('Создание продукта')
        if request['method'] == 'POST':
            logger.log(request['method'])
            # метод POST
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                product = site.create_product('in_stock', name, category)
                site.products.append(product)

            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_product.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        logger.log('Создание категории')
        if request['method'] == 'POST':
            # метод POST
            data = request['data']
            logger.log(f"{data}")

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# контроллер - копировать продукт
@AppRoute(routes=routes, url='/copy-product/')
class CopyProduct:
    @Debug(name='CopyProduct')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_product = site.get_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render('product_list.html',
                                    objects_list=site.products,
                                    name=new_product.category.name)
        except KeyError:
            return '200 OK', 'No products have been added yet'