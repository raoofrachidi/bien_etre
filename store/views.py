from django.shortcuts import render, redirect, get_object_or_404
import requests
from .forms import UserSignUpForm, ParagraphErrorList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout as djangologout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import bcrypt
from .functions import *


def index(request):
    """This view returns the home page"""
    return render(request, 'store/index.html')


def signup(request):
    """This view manages the registration of a user"""
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email, username=username)
            if not user.exists():
                user = User(
                    email=email,
                    username=username,
                )
                user.set_password(password)
                user.save()
                users=User.objects.all()
                for u in users:
                    print(u.username)
            messages.success(request, 'Votre compte a bien été créé, vous pouvez vous connecter !')
            return redirect('store:signin')
    else:
        form = UserSignUpForm()
    return render(request, 'store/signup.html', {'form': form})


def signin(request):
    """This view manages the connection of a user"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Vous êtes connecté !')
            return render(request, 'store/myaccount.html')
        else:
            messages.warning(request, "Votre nom d'utilisateur ou votre mot de passe est incorrect.")
            return render(request, 'store/signin.html')
    else:
        return render(request, 'store/signin.html')


def logout(request):
    """This view manages the logout of a user"""
    djangologout(request)
    messages.success(request, 'Vous êtes déconnecté !')
    return redirect('store:signin')


@login_required
def myaccount(request):
    """This view displays a user account page"""
    return render(request, 'store/myaccount.html')


@login_required
def myfavorites(request):
    """This view displays the user's favorites"""
    user = request.user
    favorite_list = Substitute.objects.filter(user_id=user.id).order_by('id')
    paginator = Paginator(favorite_list, 6)
    page = request.GET.get('page', 1)
    try:
        alternatives = paginator.page(page)
    except PageNotAnInteger:
        alternatives = paginator.page(1)
    except EmptyPage:
        alternatives = paginator.page(paginator.num_pages)
    context = {
        'alternatives': alternatives
    }
    return render(request, 'store/myfavorites.html', context)


def search(request):
    """This view searches the product asked by the user"""
    query = request.GET.get('query')
    if not query:
        messages.info(request, 'Veuillez saisir un produit.')
        return render(request, 'store/index.html')
    else:
        products = request_api(query)
        if not products:
            messages.info(request, "Votre recherche n'a donné aucun résultat.")
            return render(request , 'store/index.html')
        else:
            context = {
                'products': products
            }
        return render(request, 'store/search.html', context)


def substitute(request):
    """This view displays the substitutes of the user's choice"""
    user_choices = request.GET.get('chosen_product').split(', ')
    selected_product = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
    for value, user_choice in zip(selected_product, user_choices):
        request.session[value] = user_choice
    category = request.session['selected_category']
    alternatives = get_substitute(category)
    context = {
        'alternatives': alternatives
    }
    return render(request, 'store/substitute.html', context)

@login_required
def favorite(request):
    """This view records the substitute and the product in the database. It also records the favorite with th"""
    choices = request.GET.get('favorite').split(', ')
    print(choices)
    product = Product.objects.create(
        name = request.session['selected_name'],
        url = request.session['selected_url'],
        picture = request.session['selected_img'],
        nutriscore = request.session['selected_nutriscore'],
        category = request.session['selected_category'])

    favorite = Favorite.objects.create(
        user_id = request.user,
        product_id = product
    )

    substitute_product = Substitute.objects.create(
        name = choices[0],
        category = choices[1],
        picture = choices[2],
        nutriscore = choices[3],
        url = choices[4],
        picture_nutrition = choices[5],

        favorite_id = favorite,
        user_id = request.user
    )
    messages.success(request, 'Votre produit a bien été enregistré.')
    return redirect('store:myfavorites')


def detail(request):
    """This view displays the details of the product"""
    substitutes = request.GET.get('substitute').split(', ')
    session = ['substitut_name', 'substitut_category', 'substitut_img', 'substitut_nutriscore', 'substitut_url', 'substitut_img_nutrition']
    for value , substitute_product in zip(session, substitutes):
        request.session[value] = substitute_product
    return render(request, 'store/detail.html')