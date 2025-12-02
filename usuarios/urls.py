from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.usuarios, name='usuarios'),
    path('novo/', views.usuarios_novo, name='usuarios_novo'),
    path('usuarios/<int:id_usuario>/', views.usuarios, name='usuario'),
    path('<int:id_usuario>/editar/', views.usuarios_editar, name='usuarios_editar'),
    path('usuarios/<int:id_usuario>/remover/', views.usuarios_remover, name='usuario_remover'),
    path('perfil/', views.perfil, name='perfil'),
    path('editando_perfil/', views.editar_perfil, name='editando_perfil') 
]
