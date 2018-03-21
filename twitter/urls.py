from django.urls import path
from . import views

urlpatterns = [
    path('adduser/',views.adduser),
    path('verify/',views.verify),
    path('login/',views.login),
    path('logout/',views.logout),
    path('additem/',views.additem),
    path('item/',views.item),
    path('search/',views.search),

    path('adduser',views.adduser),
    path('verify',views.verify),
    path('login',views.login),
    path('logout',views.logout),
    path('additem',views.additem),
    path('item',views.item),
    path('search',views.search),

]