from django.contrib import admin

from .models import Apresentador,Programa,Programacao,Pedido,Episodio,Sugestao

admin.site.register(Sugestao)
admin.site.register(Apresentador)
admin.site.register(Programa)
admin.site.register(Programacao)
admin.site.register(Pedido)
admin.site.register(Episodio)

