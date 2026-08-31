from django import forms
from .models import Pedido, Apresentador,Programa, Programacao,Episodio,Sugestao
from django.forms import BaseFormSet, formset_factory

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
        
class ApresentadorModelForm(forms.ModelForm):
    class Meta:
        model = Apresentador
        fields = '__all__'


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
        fields = ["programa"]

    def save(self, commit=True):

        programa = self.cleaned_data["programa"]
        dias = self.cleaned_data["dias"]
        horarios = self.cleaned_data["horarios"]

        programacoes = []

        for dia in dias:

            for horario in horarios:

                programacao = Programacao(
                    programa=programa,
                    dia=dia,
                    horario=horario
                )

                if commit:
                    programacao.save()

                programacoes.append(programacao)

        return programacoes
          
class BaseProgramacaoFormSet(BaseFormSet):

    def clean(self):

        super().clean()

        combinacoes = {}
        conflitos = []

        for form in self.forms:

            if not hasattr(form, "cleaned_data"):
                continue

            if not form.cleaned_data:
                continue

            programa = form.cleaned_data.get("programa")
            dias = form.cleaned_data.get("dias")
            horarios = form.cleaned_data.get("horarios")

            if not programa or not dias or not horarios:
                continue

            for dia in dias:

                for horario in horarios:

                    combinacao = (dia, horario)

                    if combinacao in combinacoes:

                        programa_anterior = combinacoes[
                            combinacao
                        ]

                        if programa_anterior != programa:

                            dia_nome = dict(
                                Programacao.DIAS_SEMANA
                            ).get(dia)

                            horario_nome = dict(
                                Programacao.HORARIO
                            ).get(horario)

                            conflitos.append(
                                f"{dia_nome} - {horario_nome} "
                                f"já foi selecionado para "
                                f"'{programa_anterior}' e também "
                                f"para '{programa}'."
                            )

                    else:

                        combinacoes[combinacao] = programa

        if conflitos:

            raise forms.ValidationError(conflitos)
        
ProgramacaoFormSet = formset_factory(
    ProgramacaoModelForm,
    formset=BaseProgramacaoFormSet,
    extra=1
)

ProgramacaoEditFormSet = formset_factory(
    ProgramacaoModelForm,
    formset=BaseProgramacaoFormSet,
    extra=0
)

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
