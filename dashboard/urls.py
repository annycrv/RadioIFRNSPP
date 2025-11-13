from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path('', views.index, name='index'),
    path('quadros/', views.quadros, name='quadros'),
    path('quadros/novo/', views.quadro_novo, name='quadro_novo'),
    path('quadros/<int:id_quadro>/editar/', views.quadro_editar, name='quadro_editar'),
    path('quadros/<int:id_quadro>/remover/', views.quadro_remover, name='quadro_remover'),
    path('programacao/', views.programacao, name='programacao'),
    path('programacao/novo/', views.programacao_novo, name='programacao_novo'),
    path('programacao/<int:id_item>/editar/', views.programacao_editar, name='programacao_editar'),
    path('programacao/<int:id_item>/remover/', views.programacao_remover, name='programacao_remover'),
    path('conteudo/', views.index, name='conteudo'),
    path('sobre/', views.index, name='sobre'),
    path('usuarios/', views.index, name='usuarios'),
]