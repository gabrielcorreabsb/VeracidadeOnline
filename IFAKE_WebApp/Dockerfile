# Dockerfile Definitivo

# 1. Imagem Base
FROM python:3.9-slim

# 2. Variáveis de Ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Instalação Completa de Dependências do Sistema
# Instala bibliotecas para processamento gráfico/de vídeo (para OpenCV)
# e as ferramentas do Poppler (para pdf2image) de uma só vez.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Dependências do OpenCV (gráficas e de vídeo)
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    # Dependência do Poppler (para pdf2image)
    poppler-utils \
    # Limpa o cache do apt para manter a imagem pequena
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Diretório de Trabalho
WORKDIR /app

# 5. Instalar Dependências do Python
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --ignore-pipfile

# 6. Copiar o Código do Projeto
COPY . /app/

# 7. Coletar Arquivos Estáticos
RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "IFAKE_WebApp.wsgi:application"]
