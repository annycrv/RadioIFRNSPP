from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to="usuarios/perfil/", blank=True)

