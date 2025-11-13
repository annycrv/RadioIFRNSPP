from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.usuarios, name='usuarios'),
    path('novo/', views.usuarios_novo, name='usuarios_novo'),
    path('<int:id_post>/editar/', views.usuarios_editar, name='usuarios_editar'),
    path('<int:id_post>/remover/', views.usuarios_remover, name='usuarios_remover'),
]
