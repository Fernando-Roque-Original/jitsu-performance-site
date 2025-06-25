# ficheiro: core/models.py (Versão Final RPG)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Faixa(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    cor_hex = models.CharField(max_length=7, default="#FFFFFF")
    ordem = models.PositiveIntegerField(unique=True)
    idade_minima = models.PositiveIntegerField(default=0)
    def __str__(self): return self.nome

# Em core/models.py

# Substitua a sua class Grau por esta em core/models.py

class Grau(models.Model):
    PUBLICO_CHOICES = [
        ('INFANTIL', 'Infantil (até 15 anos)'),
        ('ADULTO', 'Adulto (16 anos ou mais)'),
    ]

    faixa = models.ForeignKey(Faixa, related_name="graus", on_delete=models.CASCADE, verbose_name="Faixa")
    numero = models.PositiveIntegerField(verbose_name="Grau")
    titulo = models.CharField(max_length=200, help_text="Ex: Fundamentos da Postura e Mobilidade")
    publico_alvo = models.CharField(max_length=10, choices=PUBLICO_CHOICES, default='ADULTO')
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('faixa', 'numero', 'publico_alvo')

    def __str__(self):
        return f"{self.faixa.nome} ({self.get_publico_alvo_display()}) - {self.numero}º Grau"

# NOVO MODELO: Topico
class Topico(models.Model):
    """Representa um sub-módulo dentro de um Grau. Ex: 'A Escolinha'."""
    grau = models.ForeignKey(Grau, related_name="topicos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.grau} | {self.titulo}"

# MODELO ATUALIZADO: Tecnica
class Tecnica(models.Model):
    """Agora, uma técnica pertence a um Tópico, não mais a um Grau diretamente."""
    topico = models.ForeignKey(Topico, related_name="tecnicas", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    url_video = models.URLField(max_length=300) # URL para o vídeo da técnica
    ordem = models.PositiveIntegerField(default=0)
    def __str__(self): return self.titulo

# Em core/models.py

class Perfil(models.Model):
    """Perfil do usuário, agora com mais características de RPG."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    faixa_atual = models.ForeignKey(Faixa, on_delete=models.SET_NULL, null=True, blank=True)
    grau_atual = models.ForeignKey(Grau, on_delete=models.SET_NULL, null=True, blank=True, help_text="Grau atual do aluno")
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.jpg', null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    CARGO_CHOICES = [
        ('ALUNO', 'Aluno'),
        ('PENDENTE', 'Professor Pendente'),
        ('PROFESSOR', 'Professor Aprovado'),
    ]
    cargo = models.CharField(max_length=10, choices=CARGO_CHOICES, default='ALUNO')

    # ---- A FUNÇÃO QUE FALTAVA ----
    def idade(self):
        # Se não houver data de nascimento, não há como calcular a idade
        if not self.data_nascimento:
            return None
        
        # Pega na data de hoje
        hoje = timezone.now().date()
        
        # Calcula a idade de forma precisa
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
    # -----------------------------

    def __str__(self):
        return f"{self.user.username} ({self.get_cargo_display()})"

# NOVO MODELO: ProgressoTecnica
class ProgressoTecnica(models.Model):
    """Regista se um aluno concluiu uma técnica específica."""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    class Meta: unique_together = ('perfil', 'tecnica')
    def __str__(self): return f"{self.perfil.user.username} concluiu {self.tecnica.titulo}"

@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created: Perfil.objects.create(user=instance)
    instance.perfil.save()