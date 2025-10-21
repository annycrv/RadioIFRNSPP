from django.contrib import admin

from .models import Home, Programacao,Programa, Podcast, Sobre

admin.site.register(Home)
admin.site.register(Programacao)
admin.site.register(Programa)
admin.site.register(Podcast)
admin.site.register(Sobre)

