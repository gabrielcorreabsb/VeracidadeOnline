# Veracidade Online

<div align="center">
  <img src="https://github.com/gabrielcorreabsb/VeracidadeOnline/blob/main/assets/imgs/logo.png?raw=true" alt="Veracidade Online" width="150">
  <h3>Plataforma de Análise Forense de Conteúdo Digital</h3>
  <p>Uma expansão e aprimoramento do projeto <a href="https://github.com/shraddhavijay/IFAKE">IFAKE</a>, focado em verificação de imagens e análise de documentos.</p>
</div>

## 📋 Sobre o Projeto

O Veracidade Online é uma plataforma web acadêmica dedicada a combater a desinformação digital. A ferramenta oferece um conjunto de utilitários de análise forense para que usuários possam verificar a autenticidade de conteúdos visuais e a integridade de documentos. O projeto expande as funcionalidades do IFAKE, aprimorando seus algoritmos e adicionando um novo e robusto módulo de análise de documentos (PDF, DOCX, XLSX).

O objetivo principal é oferecer uma ferramenta prática, acessível e educativa que capacite os usuários a identificar manipulações, promovendo uma cultura de verificação e pensamento crítico em relação ao conteúdo consumido na internet.

## 🚀 Funcionalidades Implementadas

O projeto foi dividido em dois módulos principais de análise:

### 1. Análise Forense de Imagens
- **Detecção de Manipulação com IA:** Utiliza o modelo MobileNetV2 para classificar imagens como "Authentic" ou "Forged".
- **Análise de Nível de Erro (ELA):** Revela inconsistências na compressão JPEG da imagem.
- **Análise de Metadados:** Extrai e exibe dados EXIF embutidos no arquivo, como informações da câmera, software utilizado e datas.
- **Técnicas Adicionais:** Inclui análise de ruído, mapa de bordas e gradiente de luminância para investigações mais profundas.

### 2. Análise Forense de Documentos
- **Suporte a Múltiplos Formatos:** Analisa arquivos PDF (`.pdf`), Word (`.docx`) e Excel (`.xlsx`).
- **Verificação de Integridade com Hashes:** Calcula as "impressões digitais" (hashes MD5 e SHA256) do arquivo. Isso permite comparar dois documentos e determinar matematicamente se eles são idênticos ou se houve qualquer alteração.
- **Extração de Metadados:** Extrai metadados internos do documento, como autor, empresa, datas de criação/modificação e o software utilizado para gerar o arquivo.

### 3. Plataforma e Educação
- **Interface Web Intuitiva:** Uma aplicação desenvolvida com Django que permite o upload de arquivos e a visualização clara dos relatórios de análise.
- **Seção Educacional:** Área do site dedicada a explicar os conceitos de desinformação, as técnicas de manipulação e como cada ferramenta de análise funciona, capacitando o usuário a interpretar os resultados.

*(Nota: A funcionalidade de análise de vídeo foi pausada no escopo atual para focar na robustez dos módulos de imagem e documentos).*

## 🛠️ Tecnologias e Dependências

A plataforma foi construída com um conjunto de tecnologias modernas e robustas:

- **Back-end:** Python, Django, Gunicorn
- **Análise de Imagem:** TensorFlow, Keras, OpenCV, Pillow
- **Análise de Documentos:** PyPDF2, python-docx, openpyxl, hashlib
- **Front-end:** HTML5, CSS3, JavaScript, Bootstrap
- **Deploy:** Docker, Docker Compose, Nginx, Certbot (Let's Encrypt) em um servidor Ubuntu.

## 🚀 Demonstração Online

A aplicação está implantada e pode ser acessada no seguinte subdomínio:
**[https://veracidadeonline.gabrielcorrea.tech](https://veracidadeonline.gabrielcorrea.tech)**

## 📸 Screenshots

<div align="center">
  <p>Página Principal</p>
  <img src="https://i.imgur.com/qYXN8Na.png" alt="Análise de Documentos" width="80%">
  <br><br>
  <p>Página de Análise de Documentos</p>
  <img src="https://i.imgur.com/ApsxzYk.png" alt="Análise de Documentos" width="80%">
  <br><br>
  <p>Página de Análise de Imagens</p>
  <img src="https://i.imgur.com/gfEOp9S.png" alt="Análise de Imagens" width="80%">
</div>

## 📚 Base Científica e Agradecimentos

Este projeto expande o trabalho original **IFAKE**, que pode ser encontrado no artigo "[Image Forgery Detection and Classification Using Deep Learning and FIDAC Dataset](https://ieeexplore.ieee.org/document/9862034)" (IEEE Xplore). A validação dos modelos de imagem utilizou o **[ARTIFACT Dataset](https://www.kaggle.com/datasets/awsaf49/artifact-dataset)**.

**Créditos ao projeto base IFAKE:**
- Shraddha Pawar
- Gaurangi Pradhan
- Bhavin Goswami

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
