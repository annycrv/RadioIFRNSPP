from django.contrib import admin

from .models import Home, Programacao,Quadro, Podcast, Sobre,Pedido

admin.site.register(Home)
admin.site.register(Programacao)
admin.site.register(Quadro)
admin.site.register(Podcast)
admin.site.register(Sobre)
admin.site.register(Pedido)

