@echo off
echo ===================================
echo    Backup do Ambiente Virtual
echo ===================================
echo.

:: Criar pasta de backup
if not exist "env_backup" mkdir env_backup

:: Data atual para nome do arquivo
set DATE_TIME=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%
set DATE_TIME=%DATE_TIME: =0%

:: Exportar requirements
echo Exportando requirements...
pipenv requirements > "env_backup/requirements_%DATE_TIME%.txt"

:: Exportar Pipfile e Pipfile.lock
echo Copiando Pipfile...
copy Pipfile "env_backup/Pipfile_%DATE_TIME%"
if exist Pipfile.lock (
    copy Pipfile.lock "env_backup/Pipfile_%DATE_TIME%.lock"
)

:: Exportar grafo de dependências
echo Exportando grafo de dependencias...
pipenv graph > "env_backup/dependencies_%DATE_TIME%.txt"

:: Criar arquivo de informações
echo Criando arquivo de informacoes...
echo Environment Info > "env_backup/info_%DATE_TIME%.txt"
echo Date: %DATE_TIME% >> "env_backup/info_%DATE_TIME%.txt"
echo. >> "env_backup/info_%DATE_TIME%.txt"
echo Python Version: >> "env_backup/info_%DATE_TIME%.txt"
python --version >> "env_backup/info_%DATE_TIME%.txt"
echo. >> "env_backup/info_%DATE_TIME%.txt"
echo Pipenv Version: >> "env_backup/info_%DATE_TIME%.txt"
pipenv --version >> "env_backup/info_%DATE_TIME%.txt"

echo.
echo Backup completo! Arquivos salvos em: env_backup/
echo.
echo Para restaurar o ambiente:
echo 1. pipenv --rm           (remove ambiente atual se existir)
echo 2. pipenv install -r "env_backup/requirements_%DATE_TIME%.txt"
echo.
pause
