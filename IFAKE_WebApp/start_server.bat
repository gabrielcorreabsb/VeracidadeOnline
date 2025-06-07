# Criar o arquivo start_server.bat
with open('start_server.bat', 'w') as f:
    f.write('@echo off\n')
    f.write('echo ===================================\n')
    f.write('echo Iniciando servidor Django...\n')
    f.write('echo ===================================\n')
    f.write('echo.\n')
    f.write('cd "%~dp0"\n')  # Muda para o diretório do script
    f.write('pipenv shell && python manage.py runserver\n')
    f.write('echo.\n')
    f.write('echo Se o servidor nao iniciar, tente executar manualmente:\n')
    f.write('echo pipenv shell\n')
    f.write('echo python manage.py runserver\n')
    f.write('echo.\n')
    f.write('pause\n')

print("Arquivo start_server.bat criado com sucesso!")