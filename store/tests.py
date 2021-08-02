from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import *
from django.test import Client
from .views import *
from unittest.mock import patch
from django.contrib.sessions.middleware import SessionMiddleware


class PageTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_legalnotice_page(self):
        response = self.client.get(reverse('store:legalnotice'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        """test the search page"""
        response = self.client.get(reverse('store:search'), {
            'query': 'Chocapic',
            })
        self.assertEqual(response.status_code, 200)


class UserTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='Jean', email='jean@gmail.com')
        user.set_password('Test123')
        user.save()

    def test_signup(self):
        response = self.client.post(reverse('store:signup'), {'username': 'Jean', 'email': 'testuser@email.com', 'password': 'Test123'})
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        response = self.client.post(reverse('store:signin'), {'username': 'Jean', 'password': 'Test123'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        logged_user = self.client.login(username='Jean', password='Test123')
        response = self.client.get('/store/logout/')
        self.assertEqual(response.status_code , 302)

    def test_myaccount(self):
        logged_user = self.client.login(username='Jean', password='Test123')
        response = self.client.get(reverse('store:myaccount'))
        self.assertEqual(response.status_code , 200)

    def test_myfavorites(self):
        logged_user = self.client.login(username='Jean', password='Test123')
        response = self.client.get(reverse('store:myfavorites'))
        self.assertEqual(response.status_code, 200)


class ProductTestCase(TestCase):
    def test_detail(self):
        response = self.client.get(reverse('store:detail'), {
            'substitute': ['Céréal double delight', 'fr:Biscuits cacaotés fourrés goût vanille',
                           'https://static.openfoodfacts.org/images/products/541/006/303/3092/front_fr.18.400.jpg', 'b',
                           'https://fr.openfoodfacts.org/produit/5410063033092/cereal-double-delight',
                           'https://static.openfoodfacts.org/images/products/541/006/303/3092/nutrition_fr.15.400.jpg'],})
        self.assertEqual(response.status_code, 200)


class SubstituteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Jean', email='jean@gmail.com', password='Test123')
        self.factory = RequestFactory()
        self.selected_product = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']

    @patch('store.functions.get_substitute')
    def test_substitute(self, mock_get_substitute):
        mock_get_substitute.return_value = [{'name': 'Prince', 'nutriscore': 'b', 'picture': 'https://static.openfoodfacts.org/images/products/021/038/807/3996/front_fr.4.400.jpg',
                 'category': ' Biscuits fourrés', 'url': 'https://fr.openfoodfacts.org/produit/0210388073996/prince', 'picture_nutrition': 'Non renseigné'},
                 {'name': 'Céréal double delight', 'nutriscore': 'b', 'picture': 'https://static.openfoodfacts.org/images/products/541/006/303/3092/front_fr.18.400.jpg',
                 'category': 'fr:Biscuits cacaotés fourrés goût vanille', 'url': 'https://fr.openfoodfacts.org/produit/5410063033092/cereal-double-delight',
                 'picture_nutrition': 'https://static.openfoodfacts.org/images/products/541/006/303/3092/nutrition_fr.15.400.jpg'}, {'name': 'Fourré Cacao sans sucres',
                 'nutriscore': 'c', 'picture': 'https://static.openfoodfacts.org/images/products/317/568/112/3014/front_fr.33.400.jpg', 'category': ' Biscuits édulcorés',
                 'url': 'https://fr.openfoodfacts.org/produit/3175681123014/fourre-cacao-sans-sucres-gerble', 'picture_nutrition':
                 'https://static.openfoodfacts.org/images/products/317/568/112/3014/nutrition_fr.49.400.jpg'}, {'name': 'Biscuit Cacaoté Fourré Saveur Vanille', 'nutriscore':
                 'c', 'picture': 'https://static.openfoodfacts.org/images/products/317/568/120/3303/front_fr.6.400.jpg', 'category': ' en:chocolate-biscuits', 'url':
                 'https://fr.openfoodfacts.org/produit/3175681203303/biscuit-cacaote-fourre-saveur-vanille-gerble', 'picture_nutrition':
                'https://static.openfoodfacts.org/images/products/317/568/120/3303/nutrition_fr.18.400.jpg'}, {'name': 'Goûters fourrés aux fruits rouges', 'nutriscore':
                'c', 'picture': 'https://static.openfoodfacts.org/images/products/325/622/505/4756/front_fr.41.400.jpg', 'category': ' Biscuits fourrés', 'url':
                'https://fr.openfoodfacts.org/produit/3256225054756/gouters-fourres-aux-fruits-rouges-u-bio', 'picture_nutrition':
                'https://static.openfoodfacts.org/images/products/325/622/505/4756/nutrition_fr.45.400.jpg'}, {'name': 'Fourré Pruneau Figue',
                'nutriscore': 'c', 'picture': 'https://static.openfoodfacts.org/images/products/325/149/034/1051/front_fr.11.400.jpg', 'category': ' Biscuits fourrés',
                'url': 'https://fr.openfoodfacts.org/produit/3251490341051/fourre-pruneau-figue-gerble', 'picture_nutrition':
                'https://static.openfoodfacts.org/images/products/325/149/034/1051/nutrition_fr.8.400.jpg'},
                {'name': 'Galletas sandwich de cacao rellenas de crema', 'nutriscore': 'c', 'picture': 'https://static.openfoodfacts.org/images/products/841/037/604/4393/front_es.17.400.jpg',
                'category': 'Chocolate sandwich cookies', 'url': 'https://fr.openfoodfacts.org/produit/8410376044393/galletas-sandwich-de-cacao-rellenas-de-crema-gullon', 'picture_nutrition':
                'https://static.openfoodfacts.org/images/products/841/037/604/4393/nutrition_fr.9.400.jpg'}, {'name': 'mini génoises orange', 'nutriscore': 'c', 'picture':
                'https://static.openfoodfacts.org/images/products/20996239/front_fr.4.400.jpg', 'category': ' Biscuits fourrés', 'url':
                'https://fr.openfoodfacts.org/produit/20996239/mini-genoises-orange-sondey', 'picture_nutrition': 'https://static.openfoodfacts.org/images/products/20996239/nutrition_fr.15.400.jpg'},
                {'name': 'Mini biscuits fourrés ronds parfum fraise', 'nutriscore': 'c', 'picture': 'https://static.openfoodfacts.org/images/products/325/622/504/1398/front_fr.35.400.jpg',
                'category': ' Goûters fourrés', 'url': 'https://fr.openfoodfacts.org/produit/3256225041398/mini-biscuits-fourres-ronds-parfum-fraise-u-mat-lou', 'picture_nutrition':
                'https://static.openfoodfacts.org/images/products/325/622/504/1398/nutrition_fr.31.400.jpg'}]
        request = self.factory.get('/store/substitute/',
                                   {'chosen_product': ['Prince goût chocolat au blé complet', 'Biscuits fourrés',
                                   'https://static.openfoodfacts.org/images/products/762/221/044/9283/front_fr.286.400.jpg',
                                   'd', 'https://fr.openfoodfacts.org/produit/7622210449283/prince-gout-chocolat-au-ble-complet-lu'],})
        request.user = self.user
        SessionMiddleware().process_request(request)
        request.session.save()
        record_session = self.selected_product
        for values in record_session:
            request.session[values] = values
        response = substitute(request)
        self.assertEqual(response.status_code, 200)

    def test_favorite(self):
        response = self.client.get(reverse('store:favorite'),
           {'favorite': ['Céréal double delight', 'fr:Biscuits cacaotés fourrés goût vanille',
             'https://static.openfoodfacts.org/images/products/541/006/303/3092/front_fr.18.400.jpg', 'b',
             'https://fr.openfoodfacts.org/produit/5410063033092/cereal-double-delight',
             'https://static.openfoodfacts.org/images/products/541/006/303/3092/nutrition_fr.15.400.jpg'],})
        self.assertEqual(response.status_code, 302)