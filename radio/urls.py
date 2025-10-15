from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('programacao/', views.programacao, name='programacao'),
    path('programas/', views.programas, name='programas'),
    path('podcasts/', views.podcasts, name='podcasts'),
    path('sobre/', views.sobre, name='sobre'),
]