import requests

from .models import Product, Favorite
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

URL = 'https://world.openfoodfacts.org/language/french/'

def update_product(product_origin, product_updated):
	"""Replace all attributes of the object in the database by the attributes of the object build from OPC"""
	for key in product_origin.__dict__:
		if key == 'id':
			continue
		else:
			product_origin.__dict__[key] = product_updated.__dict__[key]
	return product_origin

def update_db():
	"""Function use to get all french products in the openfoodfacts database"""
	last_page = False
	i = 1
	while not last_page:
		url = URL + str(i) +'.json'
		data = requests.get(url)
		data = data.json()
		if data['products'] == []:
			last_page = True
		else:
			for product in data['products']:
				try:
					name = product['product_name']
					nutriscore = product['nutrition_grades']
					picture = product['image_url']
					category = product['categories']
					url = product['url']
					picture_nutrition = product['image_nutrition_url']

					if category == "" or name == "" or nutriscore == "" or picture == "" or url == "" or picture_nutrition == "":
						continue
					else:
						product_to_save = Product(name=name, picture=picture, category=category, nutriscore=nutriscore, url=url, picture_nutrition=picture_nutrition)

						try:
							product_to_update = Product.objects.get(id=product_to_save.id)
							product_to_update = update_product(product_to_update, product_to_save)
							product_to_update.save()


						except ObjectDoesNotExist:
							product_to_save.save()

						except MultipleObjectsReturned:
							continue

				except KeyError:
					continue
			i = i+1
	print('Mise à jour de la base terminée !')


if __name__ == "__main__":
	update_db()
