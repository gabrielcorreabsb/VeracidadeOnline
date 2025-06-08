"""
Django settings for IFAKE_WebApp project.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3&%-jm4ccooczk9m-m^s@04_d8@!o+89(i_*zm3_hv!puvaz4-'

# --- ALTERAÇÃO 1: Configurações de Produção ---
# DEBUG deve ser False em um ambiente de produção por segurança.
DEBUG = False

# Adicione seu subdomínio à lista de hosts permitidos.
ALLOWED_HOSTS = ['veracidadeonline.gabrielcorrea.tech']

# --- ADICIONE ESTE BLOCO DE CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO (HTTPS) ---

# Lista de origens (domínios) confiáveis para requisições POST seguras.
# Esta é a configuração principal que resolve o erro 403 CSRF.
CSRF_TRUSTED_ORIGINS = ['https://veracidadeonline.gabrielcorrea.tech']

# Garante que os cookies de sessão e CSRF só sejam enviados pelo navegador
# através de uma conexão segura HTTPS. É uma boa prática de segurança.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- FIM DAS NOVAS CONFIGURAÇÕES ---


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',  # --- ALTERAÇÃO 2: Adicionando seu app 'website' ---
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'IFAKE_WebApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'IFAKE_WebApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# --- ALTERAÇÃO 3: Configurações de Arquivos Estáticos e de Mídia ---

# URL para acessar os arquivos no navegador (ex: /static/css/style.css)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# O caminho no servidor para onde o 'collectstatic' irá reunir todos os arquivos estáticos.
# ESTA ERA A LINHA FALTANDO QUE CAUSAVA O ERRO DE BUILD.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Lista de pastas onde o Django irá procurar pelos seus arquivos estáticos (CSS, JS, etc).
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Onde os arquivos enviados por usuários (mídia) serão armazenados.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- FIM DAS ALTERAÇÕES ---

# Configuração para o campo de auto-incremento de chave primária (boa prática)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
