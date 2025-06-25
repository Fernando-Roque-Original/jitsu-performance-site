# Ficheiro: core/migrations/XXXX_popular_dados_iniciais.py (VERSÃO FINAL E SEGURA)

from django.db import migrations

def popular_faixas_e_graus(apps, schema_editor):
    Faixa = apps.get_model('core', 'Faixa')
    Grau = apps.get_model('core', 'Grau')

    # Apaga dados existentes para garantir um começo limpo
    Grau.objects.all().delete()
    Faixa.objects.all().delete()

    faixas_data = [
        {'ordem': 1, 'nome': 'Branca', 'cor_hex': '#FFFFFF', 'idade_minima': 0},
        {'ordem': 2, 'nome': 'Cinza', 'cor_hex': '#808080', 'idade_minima': 4},
        {'ordem': 3, 'nome': 'Amarela', 'cor_hex': '#FFD700', 'idade_minima': 7},
        {'ordem': 4, 'nome': 'Laranja', 'cor_hex': '#FFA500', 'idade_minima': 10},
        {'ordem': 5, 'nome': 'Verde', 'cor_hex': '#008000', 'idade_minima': 13},
        {'ordem': 6, 'nome': 'Azul', 'cor_hex': '#007BFF', 'idade_minima': 16},
        {'ordem': 7, 'nome': 'Roxa', 'cor_hex': '#8A2BE2', 'idade_minima': 16},
        {'ordem': 8, 'nome': 'Marrom', 'cor_hex': '#A0522D', 'idade_minima': 18},
        {'ordem': 9, 'nome': 'Preta', 'cor_hex': '#000000', 'idade_minima': 19},
    ]

    # MUDANÇA AQUI: Criamos cada faixa individualmente, em vez de em massa
    for data in faixas_data:
        Faixa.objects.create(**data)
    print("\nFaixas criadas com sucesso.")

    faixas_com_graus = ['Branca', 'Cinza', 'Amarela', 'Laranja', 'Verde', 'Azul', 'Roxa', 'Marrom']
    
    graus_criados_count = 0
    for nome_faixa in faixas_com_graus:
        faixa_obj = Faixa.objects.get(nome=nome_faixa)
        
        titulos_base = {
            'Branca': 'Fundamentos', 'Cinza': 'Controle', 'Amarela': 'Passagens',
            'Laranja': 'Combinações', 'Verde': 'Transições', 'Azul': 'Desenvolvimento',
            'Roxa': 'Ataques', 'Marrom': 'Refinamento',
        }
        
        for i in range(5):
            titulo_grau = f"{i}º Grau - {titulos_base[nome_faixa]}"
            if i == 0:
                titulo_grau = f"Fundamentos da Faixa {nome_faixa}"

            if nome_faixa == 'Branca':
                Grau.objects.create(faixa=faixa_obj, numero=i, titulo=f"{titulo_grau} (Adulto)", publico_alvo='ADULTO')
                Grau.objects.create(faixa=faixa_obj, numero=i, titulo=f"{titulo_grau} (Infantil)", publico_alvo='INFANTIL')
                graus_criados_count += 2
            elif faixa_obj.idade_minima < 16:
                Grau.objects.create(faixa=faixa_obj, numero=i, titulo=titulo_grau, publico_alvo='INFANTIL')
                graus_criados_count += 1
            else:
                Grau.objects.create(faixa=faixa_obj, numero=i, titulo=titulo_grau, publico_alvo='ADULTO')
                graus_criados_count += 1
    
    print(f"{graus_criados_count} graus criados com sucesso.")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_grau_unique_together_grau_publico_alvo_and_more'),
    ]

    operations = [
        migrations.RunPython(popular_faixas_e_graus),
    ]