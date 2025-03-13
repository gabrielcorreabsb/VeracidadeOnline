

```markdown
# Veracidade Online

<div align="center">
  <img src="https://raw.githubusercontent.com/shraddhavijay/IFAKE/master/screenshots/text.gif" alt="Veracidade Online">
  <h3>Sistema de Verificação de Autenticidade de Conteúdo Digital</h3>
  <p>Baseado no projeto <a href="https://github.com/shraddhavijay/IFAKE">IFAKE</a></p>
</div>

## 📋 Sobre o Projeto

O Veracidade Online é uma iniciativa acadêmica dedicada à investigação e verificação da autenticidade de conteúdo digital, com foco em identificar e combater a disseminação de imagens e vídeos manipulados nas redes sociais e internet. O projeto utiliza como base o IFAKE, uma aplicação robusta de detecção de falsificações em imagens e vídeos.

### Objetivo Principal

Aplicar e expandir as capacidades do IFAKE para criar uma solução eficiente de verificação de autenticidade de conteúdos digitais, visando combater a desinformação através da detecção de manipulações digitais.

## 🚀 Funcionalidades Principais

### 1. Detecção de Falsificação em Imagens
- Detecção de manipulações usando CNN
- Análise através de Error Level Analysis (ELA)
- Classificação de imagens originais e manipuladas
- Geração de relatórios detalhados

### 2. Detecção de Falsificação em Vídeos
- Análise frame por frame
- Detecção de inconsistências temporais
- Identificação de manipulações em vídeos
- Relatório de análise de vídeo

### 3. Análise de Metadados
- Extração e análise de dados EXIF
- Verificação de informações da câmera
- Histórico de modificações
- Detalhes técnicos da imagem/vídeo

### 4. Recursos Adicionais
- Interface web intuitiva
- Geração de relatórios em PDF
- Visualização de resultados em tempo real
- Suporte a múltiplos formatos de arquivo

### 5. Sistema de Educação e Conscientização
- Base de conhecimento sobre manipulações digitais
- Exemplos de casos reais
- Guias de boas práticas
- Material educativo sobre verificação de autenticidade

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- Python3 e pip3
- Dependências específicas listadas em `requirements.txt`

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/veracidade-online.git

# Entre no diretório
cd veracidade-online

# Instale as dependências
pip3 install -r requirements.txt

# Inicie a aplicação
python3 manage.py runserver
```

Acesse `http://127.0.0.1:8000/` para utilizar a aplicação.

## 📸 Screenshots

<div align="center">
  <img src="https://raw.githubusercontent.com/shraddhavijay/IFAKE/master/screenshots/index.JPG" alt="Página Inicial" width="80%">
  <br><br>
  <img src="https://raw.githubusercontent.com/shraddhavijay/IFAKE/master/screenshots/imageDetection1.png" alt="Detecção de Imagem" width="80%">
  <br><br>
  <img src="https://raw.githubusercontent.com/shraddhavijay/IFAKE/master/screenshots/metadata.JPG" alt="Análise de Metadados" width="80%">
</div>

## 📚 Base Científica

Este projeto é baseado no artigo "[Image Forgery Detection and Classification Using Deep Learning and FIDAC Dataset](https://ieeexplore.ieee.org/document/9862034)", publicado no IEEE Explore, que apresenta o modelo CNN utilizado no IFAKE e o dataset FIDAC.

O [dataset FIDAC](https://ieee-dataport.org/documents/fidac-forged-images-detection-and-classification) está disponível no IEEE Dataport e contém imagens originais junto com suas versões adulteradas.

## 🙏 Créditos

Este projeto é baseado no IFAKE, desenvolvido por:
- Shraddha Pawar
- Gaurangi Pradhan
- Bhavin Goswami

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```
