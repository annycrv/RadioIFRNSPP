from django import forms
from .models import Pedido, Programa, Programacao,Episodio,Sugestao

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

class SugestaoModelForm(forms.ModelForm):
    class Meta:
        model = Sugestao
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
        exclude = ['curtidas']
        fields = '__all__'


class ProgramacaoModelForm(forms.ModelForm):
    
    dias = forms.MultipleChoiceField(
        choices=Programacao.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label="Dias"
    )
    horarios = forms.MultipleChoiceField(
        choices=Programacao.HORARIO,
        widget=forms.CheckboxSelectMultiple,
        label="Horários"
    )

    class Meta:
        model = Programacao
        fields = ['programa']

    def save(self, commit=True):
        programa = self.cleaned_data['programa']
        dias = self.cleaned_data['dias']
        horarios = self.cleaned_data['horarios']

        instances = []
        for dia in dias:
            for horario in horarios:
                instance = Programacao(programa=programa, dia=dia, horario=horario)
                if commit:
                    instance.save()
                instances.append(instance)
        return instances

class EpisodioModelForm(forms.ModelForm):
    class Meta:
        model = Episodio
        exclude = ['programa']

        widgets = {
            'audio': forms.URLInput(attrs={
                'placeholder': 'Ex: http://instagram.com/',
                'class': 'form-control',  # opcional, para estilizar com Bootstrap
            }),
        }
