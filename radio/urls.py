from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('programacao/<str:dia>/', views.programacao, name='programacao'),
    path('quadros/', views.quadros, name='quadros'),
    path('podcasts/', views.podcasts, name='podcasts'),
    path('sobre/', views.sobre, name='sobre'),
]