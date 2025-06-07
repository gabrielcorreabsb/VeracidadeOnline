@echo off
echo ===================================
echo    Restaurar Ambiente Virtual
echo ===================================
echo.

:: Listar backups disponíveis
echo Backups disponiveis:
dir /b "env_backupequirements_*.txt"
echo.

set /p BACKUP_FILE="Digite o nome do arquivo de backup (requirements_*.txt): "

:: Verificar se arquivo existe
if not exist "env_backup\%BACKUP_FILE%" (
    echo Arquivo nao encontrado!
    pause
    exit /b 1
)

:: Remover ambiente atual
echo Removendo ambiente virtual atual...
pipenv --rm

:: Criar novo ambiente
echo Criando novo ambiente...
pipenv install -r "env_backup\%BACKUP_FILE%"

echo.
echo Ambiente restaurado!
echo.
pause
