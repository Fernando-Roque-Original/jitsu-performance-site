# ficheiro: core/admin.py (Versão com filtros)

from django.contrib import admin
from .models import Faixa, Grau, Topico, Tecnica, Perfil, ProgressoTecnica

# --- Personalização para o modelo Grau ---
@admin.register(Grau)
class GrauAdmin(admin.ModelAdmin):
    # As colunas que queremos ver na lista de graus
    list_display = ('titulo', 'faixa', 'numero', 'publico_alvo')
    
    # OS FILTROS QUE VOCÊ PEDIU! Eles aparecerão na barra lateral direita.
    list_filter = ('publico_alvo', 'faixa', 'numero')
    
    # Uma barra de pesquisa para procurar por título do grau ou nome da faixa
    search_fields = ('titulo', 'faixa__nome')


# --- Personalizações para os outros modelos (para manter a organização) ---

@admin.register(Faixa)
class FaixaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'idade_minima')
    ordering = ('ordem',)

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'grau', 'ordem')
    list_filter = ('grau__faixa',)

@admin.register(Tecnica)
class TecnicaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'topico')
    list_filter = ('topico__grau__faixa', 'topico')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'faixa_atual', 'grau_atual')
    list_filter = ('cargo', 'faixa_atual')

# Registamos o ProgressoTecnica de forma simples, pois não precisa de personalização por agora
admin.site.register(ProgressoTecnica)