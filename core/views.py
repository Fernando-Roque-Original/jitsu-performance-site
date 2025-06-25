# ficheiro: core/views.py (VERSÃO FINAL E CORRIGIDA)

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Importamos todos os nossos modelos e o formulário
from .models import Perfil, Faixa, Grau, Tecnica
from .forms import PerfilForm


def homepage_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username_do_form = request.POST.get('username')
        password_do_form = request.POST.get('password')
        user = authenticate(request, username=username_do_form, password=password_do_form)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            contexto = {'error_message': 'Nome de usuário ou senha inválidos.'}
            return render(request, 'core/login.html', contexto)
    return render(request, 'core/login.html')


@login_required
def dashboard_view(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return redirect('escolha_inicial')

    if perfil.cargo == 'ALUNO' and not perfil.faixa_atual:
        return redirect('escolha_inicial')

    contexto = {'perfil': perfil}

    if perfil.cargo == 'PROFESSOR':
        contexto['faixas'] = Faixa.objects.all().order_by('ordem')
    
    # ---- LÓGICA CORRIGIDA E REINTRODUZIDA PARA O ALUNO ----
    elif perfil.cargo == 'ALUNO':
        if perfil.faixa_atual:
            # 1. Calcula a idade do aluno a partir da data de nascimento
            idade_aluno = perfil.idade()

            # 2. Define o público alvo com base na idade
            publico_alvo_do_aluno = 'ADULTO'
            if idade_aluno is not None and idade_aluno <= 15:
                publico_alvo_do_aluno = 'INFANTIL'

            # 3. Busca os graus que correspondem à faixa E AO PÚBLICO ALVO do aluno
            graus_da_faixa = Grau.objects.filter(
                faixa=perfil.faixa_atual,
                publico_alvo=publico_alvo_do_aluno # ESTE FILTRO É A CHAVE!
            ).order_by('numero')
            
            contexto['graus'] = graus_da_faixa
    # --------------------------------------------------------

    return render(request, 'core/dashboard.html', contexto)


@login_required
def escolha_inicial_view(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    if perfil.faixa_atual:
        return redirect('dashboard')

    if request.method == 'POST':
        escolha = request.POST.get('escolha')
        if escolha == 'iniciante':
            faixa_branca = Faixa.objects.get(ordem=1)
            
            idade_aluno = perfil.idade()
            publico_alvo_do_aluno = 'ADULTO'
            if idade_aluno is not None and idade_aluno <= 15:
                publico_alvo_do_aluno = 'INFANTIL'

            grau_zero = Grau.objects.get(
                faixa=faixa_branca, 
                numero=0, 
                publico_alvo=publico_alvo_do_aluno
            )
            
            perfil.faixa_atual = faixa_branca
            perfil.grau_atual = grau_zero
            perfil.save()
            return redirect('dashboard')
        elif escolha == 'questionario':
            return redirect('dashboard')
    return render(request, 'core/escolha_inicial.html')


def registo_aluno_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('escolha_inicial')
    else:
        form = UserCreationForm()
    return render(request, 'core/registo.html', {'form': form, 'tipo_registo': 'Aluno'})


def registo_professor_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.perfil.cargo = 'PENDENTE'
            user.perfil.save()
            return render(request, 'core/registo_sucesso.html')
    else:
        form = UserCreationForm()
    return render(request, 'core/registo.html', {'form': form, 'tipo_registo': 'Professor'})


@login_required
def editar_perfil_view(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        if 'remover_foto' in request.POST:
            perfil.foto_perfil.delete(save=False)
            perfil.foto_perfil = 'fotos_perfil/default.jpg'
            perfil.save()
            return redirect('editar_perfil')
        else:
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            data_nascimento_str = request.POST.get('data_nascimento')
            perfil.data_nascimento = data_nascimento_str if data_nascimento_str else None
            if 'nova_foto_perfil' in request.FILES:
                perfil.foto_perfil = request.FILES['nova_foto_perfil']
            perfil.save()
            return redirect('dashboard')
    contexto = {'perfil': perfil}
    return render(request, 'core/editar_perfil.html', contexto)


def logout_view(request):
    logout(request)
    return redirect('homepage')

# Views para o conteúdo interativo
def carregar_graus_view(request, faixa_id):
    faixa = Faixa.objects.get(id=faixa_id)
    perfil = request.user.perfil
    
    idade_aluno = perfil.idade()
    publico_alvo_do_aluno = 'ADULTO'
    if idade_aluno is not None and idade_aluno <= 15:
        publico_alvo_do_aluno = 'INFANTIL'
        
    graus = Grau.objects.filter(faixa=faixa, publico_alvo=publico_alvo_do_aluno).order_by('numero')
    
    return render(request, 'partials/cards_graus.html', {'graus': graus, 'perfil': perfil})

def carregar_conteudo_faixa_view(request, faixa_id):
    faixa = Faixa.objects.get(id=faixa_id)
    return render(request, 'partials/card_faixa_professor.html', {'faixa': faixa})