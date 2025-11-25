from django.urls import path
from . import views

app_name = "radio"

urlpatterns = [
    path("redirecionar/", views.redirecionar, name="redirecionar"),
    path('', views.index, name='index'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('programacao/<str:dia>/', views.programacao, name='programacao'),
    path('programas/', views.programas, name='programas'),
    path('sobre/', views.sobre, name='sobre'),
    path('registrar_curtida/', views.registrar_curtida, name='registrar_curtida'),
    path('episodios/<int:id_programa>/',views.episodios, name='episodios'),
]