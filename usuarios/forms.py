from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove todos os help_text padrões
        for field in self.fields.values():
            field.help_text = None

        # Adiciona apenas os help_text desejados
        self.fields['password1'].help_text = (
        "Sua senha precisa conter pelo menos 8 caracteres.<br>"
        "Sua senha não pode ser inteiramente numérica."
        )  
        self.fields['password2'].help_text = "Informe a mesma senha informada anteriormente, para verificação."

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']