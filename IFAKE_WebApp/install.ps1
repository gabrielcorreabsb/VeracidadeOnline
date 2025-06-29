# Remova o ambiente anterior
Write-Host "Removendo ambiente anterior..."
pipenv --rm

# Crie novo ambiente
Write-Host "Criando novo ambiente com Python 3.9..."
pipenv --python 3.9

# Instale as dependÍncias
Write-Host "Instalando dependÍncias..."
pipenv install -r requirements.txt

Write-Host "Ativando o ambiente..."
pipenv shell