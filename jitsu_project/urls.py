# ficheiro: jitsu_project/urls.py (versão final para a estrutura RPG)

from django.contrib import admin
from django.urls import path
# Imports para servir ficheiros de mídia em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

# Importamos TODAS as views que vamos usar da nossa app 'core'
from core.views import (
    homepage_view,
    dashboard_view,
    registo_aluno_view,
    registo_professor_view,
    escolha_inicial_view,
    editar_perfil_view,
    logout_view,
    carregar_graus_view,
    # A view 'completar_grau_view' que planejamos, será adicionada aqui no futuro
    carregar_conteudo_faixa_view
)

urlpatterns = [
    # URLs do App
    path('admin/', admin.site.urls),
    path('', homepage_view, name='homepage'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # URLs de Registo
    path('registo/aluno/', registo_aluno_view, name='registo_aluno'),
    path('registo/professor/', registo_professor_view, name='registo_professor'),
    
    # URLs de Fluxo do Usuário
    path('bem-vindo/', escolha_inicial_view, name='escolha_inicial'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),

    path('ajax/carregar-graus/<int:faixa_id>/', carregar_graus_view, name='carregar_graus'),
    path('ajax/carregar-faixa/<int:faixa_id>/', carregar_conteudo_faixa_view, name='carregar_faixa'),
]

# Adiciona o caminho para os ficheiros de mídia (fotos de perfil) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)