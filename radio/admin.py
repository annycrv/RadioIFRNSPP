from django.contrib import admin

from .models import Home, Programa,Programacao, Sobre,Pedido,Episodio,Sugestao

admin.site.register(Home)
admin.site.register(Sugestao)
admin.site.register(Programa)
admin.site.register(Programacao)
admin.site.register(Sobre)
admin.site.register(Pedido)
admin.site.register(Episodio)

