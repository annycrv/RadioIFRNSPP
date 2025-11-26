from django import forms
from .models import Pedido,Home, Programa, Programacao,Episodio

class PedidoModelForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
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
            'horario_desejado': forms.Select(attrs={'class': 'form-select'}),


            'mensagem': forms.Textarea(attrs={
                'class': 'form-control campo-estilizado2',
                'placeholder': 'Digite alguma observação',
                'rows': 4,
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
        
class ProgramaModelForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = '__all__'


class ProgramacaoModelForm(forms.ModelForm):
    class Meta:
        model = Programacao
        fields = '__all__'

class EpisodioModelForm(forms.ModelForm):
    class Meta:
        model = Episodio
        exclude = ['programa']

