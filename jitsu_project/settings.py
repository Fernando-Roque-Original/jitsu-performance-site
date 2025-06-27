"""
Django settings for jitsu_project project.
"""

from pathlib import Path
import os # Importamos o 'os' para ler as variáveis de ambiente
import dj_database_url # Importamos o 'dj_database_url'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÃO DE SEGURANÇA E AMBIENTE ---

# A SECRET_KEY nunca deve ser visível no código em produção.
# Usamos os.environ.get() para ler a variável de ambiente que configurámos no Render.
# O segundo valor é um default para o ambiente local.
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-jt#-c3m%6)s*zm3-_*p-w88dn#rj07lkytqo3rykz7es8+uq&p'
)

# O DEBUG deve ser False em produção para segurança.
# A variável 'RENDER' é automaticamente definida como 'true' pelo Render.
IS_RENDER = os.environ.get('RENDER') == 'true'

if IS_RENDER:
    DEBUG = False
else:
    DEBUG = True

# --- HOSTS PERMITIDOS ---
# Esta configuração agora é mais segura e flexível.
ALLOWED_HOSTS = []

# O Render define esta variável com o endereço público do nosso site.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Adicionamos os hosts locais para desenvolvimento
ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])


# --- APLICAÇÕES E MIDDLEWARE ---

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic', # Para o WhiteNoise
    'core', # A nossa app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Middleware do WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jitsu_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jitsu_project.wsgi.application'


# --- BANCO DE DADOS ---
# Esta é a configuração mais importante.
# Ela tenta ler a DATABASE_URL que configurámos no Render.
# Se não encontrar (porque estamos no nosso computador), ela usa o db.sqlite3.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600 # Opcional, melhora a performance das conexões
    )
}


# --- VALIDAÇÃO DE SENHAS ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (a sua secção de validadores continua igual) ...
]


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- FICHEIROS ESTÁTICOS (CSS, JS) E DE MÍDIA (UPLOADS) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- OUTRAS CONFIGURAÇÕES ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'homepage'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# As configurações do JAZZMIN continuam aqui...
JAZZMIN_SETTINGS = {
    # ... (a sua secção JAZZMIN_SETTINGS continua igual) ...
}