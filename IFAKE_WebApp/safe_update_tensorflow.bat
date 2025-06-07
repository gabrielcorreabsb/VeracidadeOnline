@echo off
chcp 65001 > nul
cls
echo =======================================
echo    Atualização Segura do TensorFlow
echo =======================================
echo.

:: Criar pasta de backup
if not exist "tf_backup" mkdir tf_backup

:: Salvar estado atual
echo Salvando estado atual do ambiente...
pipenv requirements > "tf_backup/requirements_pre_update.txt"
pipenv graph > "tf_backup/dependencies_pre_update.txt"

:: Verificar versões atuais
echo.
echo Verificando versões instaladas...
echo.
pipenv run python -c "import tensorflow as tf; print('TensorFlow atual:', tf.__version__)"
pipenv run python -c "import numpy as np; print('NumPy atual:', np.__version__)"
pipenv run python -c "import keras; print('Keras atual:', keras.__version__)"

echo.
echo =======================================
echo    Menu de Atualização
echo =======================================
echo 1. Testar compatibilidade
echo 2. Atualizar TensorFlow para 2.10.0
echo 3. Restaurar backup
echo 4. Sair
echo.

:menu
set /p opcao="Escolha uma opção (1-4): "

if "%opcao%"=="1" (
    echo.
    echo Testando compatibilidade...
    echo.
    pipenv run pip check
    echo.
    pause
    goto menu
)

if "%opcao%"=="2" (
    echo.
    echo Iniciando atualização...
    echo.

    :: Remover versões antigas
    echo Removendo TensorFlow e Keras...
    pipenv uninstall tensorflow keras

    :: Instalar novas versões
    echo.
    echo Instalando TensorFlow 2.10.0...
    pipenv install tensorflow==2.10.0

    :: Verificar instalação
    echo.
    echo Verificando nova instalação...
    pipenv run python -c "import tensorflow as tf; print('Nova versão TensorFlow:', tf.__version__)"

    :: Reinstalar dependências específicas
    echo.
    echo Verificando dependências...
    pipenv install Django==3.2.1
    pipenv install numpy==1.19.5
    pipenv install scipy==1.6.1
    pipenv install pandas==1.2.3
    pipenv install Pillow==9.5.0
    pipenv install opencv-contrib-python==4.5.5.62
    pipenv install matplotlib==3.3.4
    pipenv install scikit-image==0.18.1
    pipenv install scikit-learn==0.24.1
    pipenv install pdf2image==1.16.0
    pipenv install tqdm==4.59.0

    echo.
    pause
    goto menu
)

if "%opcao%"=="3" (
    echo.
    echo Restaurando backup...
    pipenv --rm
    pipenv install -r "tf_backup/requirements_pre_update.txt"
    echo.
    echo Ambiente restaurado!
    pause
    goto menu
)

if "%opcao%"=="4" (
    exit /b 0
)

echo.
echo Opção inválida!
timeout /t 2 > nul
goto menu
