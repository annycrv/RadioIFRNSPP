from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to="radio/usuarios/perfil/", blank=True)
    email = models.EmailField(max_length=255, unique=True)
    
    # Define qual o campo é o nome de usuário
    USERNAME_FIELD = "email"
    # Necessário para createsuperuser continuar funcionando
    REQUIRED_FIELDS = ["username"]

