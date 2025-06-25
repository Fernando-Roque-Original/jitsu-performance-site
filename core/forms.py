# ficheiro: core/forms.py (Versão Correta e Completa)

from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class PerfilForm(forms.ModelForm):
    # Definimos os campos que não estão no modelo Perfil, mas que queremos editar
    first_name = forms.CharField(max_length=150, required=False, label="Primeiro Nome")
    last_name = forms.CharField(max_length=150, required=False, label="Apelido")
    
    # Garantimos que o campo de data use o widget de calendário
    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Perfil
        # O formulário baseia-se no Perfil e só precisa de saber sobre a foto aqui
        fields = ['foto_perfil']

    def __init__(self, *args, **kwargs):
        # O 'user' é passado da nossa view para o formulário
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Preenchemos os campos com os dados existentes do User e do Perfil
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
        if self.instance and self.instance.data_nascimento:
            # Formata a data para o padrão que o input[type=date] espera (YYYY-MM-DD)
            self.fields['data_nascimento'].initial = self.instance.data_nascimento.strftime('%Y-%m-%d') if self.instance.data_nascimento else ''

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = self.user
        
        # Atualiza os dados do User com os dados validados ("cleaned") do formulário
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Atualiza o perfil com a data validada
        perfil.data_nascimento = self.cleaned_data['data_nascimento']

        if commit:
            user.save()
            perfil.save()
        return perfil