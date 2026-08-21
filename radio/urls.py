from django.urls import path
from . import views

app_name = "radio"

urlpatterns = [
    path('', views.index, name='index'),
    path('sugestao_ajax/', views.sugestao_ajax, name='sugestao_ajax'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedido_ajax/', views.pedido_ajax, name='pedido_ajax'),
    path('programacao/<str:dia>/', views.programacao, name='programacao'),
    path('programacao_ajax/<str:dia>/', views.programacao_ajax, name='programacao_ajax'),
    path('programas/', views.programas, name='programas'),
    path("programas_ajax/", views.programas_ajax, name="programas_ajax"),
    path('sobre/', views.sobre, name='sobre'),
    path('registrar_curtida/', views.registrar_curtida, name='registrar_curtida'),
    path("curtida_ajax/", views.curtida_ajax, name="curtida_ajax",),
    path('episodios/<int:id_programa>/',views.episodios, name='episodios'),
]