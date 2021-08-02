from django.conf.urls import url
from . import views

app_name = 'store'

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^substitute/$', views.substitute, name='substitute'),
    url(r'^favorite/', views.favorite, name='favorite'),
    url(r'^myfavorites/', views.myfavorites, name='myfavorites'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^myaccount/', views.myaccount, name='myaccount'),
]