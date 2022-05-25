from datetime import date
from views import Index, About, Contact, ProductsList, CreateProduct, CreateCategory, CategoryList, CopyProduct


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/products-list/': ProductsList(),
    '/create-product/': CreateProduct(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-product/': CopyProduct(),
}