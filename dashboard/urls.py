from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path('', views.index, name='index'),
    path('quadros/', views.quadros, name='quadros'),
    path('quadros/novo/', views.quadro_novo, name='quadro_novo'),
    # path('quadro/<int:id_quadro>/detalhar/', views.quadro_detalhar, name='quadro_detalhar'),
    path('quadros/<int:id_quadro>/editar/', views.quadro_editar, name='quadro_editar'),
    path('quadros/<int:id_quadro>/remover/', views.quadro_remover, name='quadro_remover'),
    path('programacao/', views.index, name='programacao'),
    path('conteudo/', views.index, name='conteudo'),
    path('sobre/', views.index, name='sobre'),
    path('usuarios/', views.index, name='usuarios'),
]