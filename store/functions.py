import requests
import re
from .models import *


def keeping_data(products):
    """This function keeps the data we need"""
    products = products[:9]
    list = []
    for i in range(len(products)):
        product = {
            "name": products[i]['product_name'],
            "nutriscore": products[i].get('nutrition_grades', 'NC'),
            "picture": products[i]['image_front_url'],
            "category": products[i]['categories'].split(',')[-1],
            "url": products[i]['url'],
            "picture_nutrition": products[i].get('image_nutrition_url', 'Non renseigné'),
        }
        list.append(product)
    return list


def request_api(query):
    """This function imports variants of the user's choice"""
    api = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(query)
    response = requests.get(api)
    result = response.json()
    products = result['products'][:20]
    return keeping_data(products)


def request_off(category, nutriscore):
    """This function searches a substitute for the user's choice"""
    off = "https://fr.openfoodfacts.org/cgi/search.pl?"
    params = {
        'action' : 'process',
         'tagtype_0' : 'categories',
         'tag_contains_0' : 'contains',
         'tag_0' : category,
         'tagtype_1' : 'nutrition_grades',
         'tag_contains_1' : 'contains',
         'tag_1' : nutriscore,
         'sort_by' : 'unique_scans_n',
         'page_size' : '20',
         'axis_x' : 'energy',
         'axis_y' : 'product_n',
         'json' : '1',
     }
    response = requests.get(off, params=params)
    result = response.json()
    return result['products']


def get_substitute(category):
    """This function lists the substitutes"""
    nutriscore_list = ["a", "b", "c", "d", "e"]
    list = []
    for nutriscore in nutriscore_list:
        if len(list) < 6:
            substitute_list = request_off(category, nutriscore)
            for substitute in substitute_list:
                list.append(substitute)
    return keeping_data(list)