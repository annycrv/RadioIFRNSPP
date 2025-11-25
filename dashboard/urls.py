from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path('', views.index, name='index'),
    path('programas/', views.programas, name='programas'),
    path('programas/novo/', views.programa_novo, name='programa_novo'),
    path('programas/<int:id_programa>/', views.programas, name='programa'),
    path('programas/<int:id_programa>/editar/', views.programa_editar, name='programa_editar'),
    path('programas/<int:id_programa>/remover/', views.programa_remover, name='programa_remover'),
    path('programacao/', views.programacao, name='programacao'),
    path('programacao/<int:id_programacao>/', views.programacao, name='programacao'),
    path('programacao/novo/', views.programacao_novo, name='programacao_novo'),
    path('programacao/<int:id_item>/editar/', views.programacao_editar, name='programacao_editar'),
    path('programacao/<int:id_item>/remover/', views.programacao_remover, name='programacao_remover'),
    path('conteudo/', views.index, name='conteudo'),
    path('sobre/', views.index, name='sobre'),
    path('usuarios/', views.index, name='usuarios'),
    path('episodios/', views.episodios, name='episodios'),
    path('episodios/novo/<int:id_programa>/', views.episodio_novo, name='episodio_novo'),
    path('episodios/detalhar/<int:id_episodio>/', views.episodio_detalhar, name='episodio_detalhar'),
    path('episodios/<int:id_item>/editar/', views.episodio_editar, name='episodio_editar'),
    path('episodios/<int:id_item>/remover/', views.episodio_remover, name='episodio_remover'),
    path('programas/<int:id_programa>/episodios/', views.episodios_programa,name='episodios_programa'),
]