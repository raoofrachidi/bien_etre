import requests

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, IntegrityError
from .models import Product


class Command(BaseCommand):
    help = 'Initializes the database'

    CATEGORIES = ['Viandes', 'Poissons', 'Epicerie', 'Chocolats', 'Pates-a-tartiner', 'Biscuits', 'Vins',
                  'Boissons-gazeuses', 'Yaourts', 'Pains', 'Glace', 'Fromages-de-france', 'Pizzas', 'Snacks sucrés']

    def create_db(self):

        for category in self.CATEGORIES:

            params = {
                'action': 'process',
                'json': 1,
                'page_size': 500,
                'page': 1,
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': category,
            }

            response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl',
                                    params=params)

            data = response.json()
            products = data['products']

            for product in products:
                try:
                    name = product["product_name"]
                    brand = product["brands"]
                    nutriscore = product["nutrition_grades"]
                    url = product["url"]
                    picture = product['image_front_url']
                    picture_nutrition = product["image_nutrition_small_url"]

                    Product.objects.create(name=name, category=category,
                                           nutriscore=nutriscore,
                                           url=url, picture=picture, picture_nutrition=picture_nutrition)

                except KeyError:
                    pass

                except DataError:
                    pass

                except IntegrityError:
                    pass

    def handle(self, *args, **options):
        self.create_db()
