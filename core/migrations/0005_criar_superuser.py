# Ficheiro: core/migrations/0004_criar_superuser.py

from django.db import migrations
from django.contrib.auth import get_user_model

def criar_superuser(apps, schema_editor):
    User = get_user_model()

    # ---- CONFIGURE OS SEUS DADOS DE ADMIN AQUI ----
    username = "admin"  # Escolha um nome para o seu admin
    password = "F741852963!" # Escolha uma senha forte
    email = "naruto1.uzumaqui1@gmail.com"
    # ---------------------------------------------

    # Verifica se um superusuário com este nome já não existe
    if not User.objects.filter(username=username).exists():
        print(f"\nCriando superusuário: {username}")
        User.objects.create_superuser(username=username, password=password, email=email)
    else:
        print(f"\nSuperusuário '{username}' já existe, não foi criado novamente.")


class Migration(migrations.Migration):

    dependencies = [
        # Apontando para a última migração que temos (a que populou os dados)
        ('core', '0003_popular_dados_iniciais'),
    ]

    operations = [
        migrations.RunPython(criar_superuser),
    ]