from django import forms
from .models import Pedido,Home

class PedidoModelForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude = ["horario_pedidos"]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Digite seu nome',
            }),
            'musica': forms.TextInput(attrs={
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Ex: Nome da música ou estilo musical',
            }),
            'artista': forms.TextInput(attrs={
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Ex: Artista,banda ou cantor',
            }),
            'horario_desejado': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Digite o horário do dia que deseja ouvir',
            }),
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'mensagem': forms.TextInput(attrs={
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Digite alguma observação',
            }),
        }

class HomeModelForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ["nome","comentario"]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control campo-estilizado',
                'placeholder': 'Digite seu nome',
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control campo-estilizado',
                'placeholder': 'Conte-nos suas ideias de programas que você gostaria de ouvir...',
                'rows': 4,
            }),
               }
