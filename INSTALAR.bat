@echo off
chcp 65001 > nul
title Instalador - diRoma Central de Cadastro
color 0A

echo.
echo ============================================
echo   diRoma - Central de Cadastro
echo   Instalador Automático
echo ============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado!
    echo.
    echo Baixe e instale de: https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Instalar dependências
echo Instalando dependências... (streamlit, pandas, openpyxl, Pillow)
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ✅ Instalação concluída com sucesso!
echo.
echo Para iniciar o aplicativo, clique duas vezes em:
echo   ► INICIAR.bat
echo.
pause
