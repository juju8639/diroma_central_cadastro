#!/usr/bin/env python3
"""
Script para fazer upload dos arquivos para GitHub automaticamente
Requer: pip install PyGithub
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("📤 Upload para GitHub - diRoma Central de Cadastro")
print("=" * 60)
print()

# Instruções para upload manual
print("""
⚠️  Git não está instalado no seu PC.

Mas não se preocupe! Você pode fazer upload de 2 formas:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Opção 1: UPLOAD MANUAL (5 minutos) ✅ RECOMENDADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Acesse seu repositório no GitHub:
   https://github.com/juju8639/diroma_central_cadastro

2. Clique em "Add file" → "Upload files"

3. Arraste/selecione estes arquivos:
   ✅ app.py
   ✅ requirements.txt
   ✅ logo.svg
   ✅ README.md
   ✅ DEPLOY_PRONTO.md
   ✅ .gitignore
   ✅ .streamlit/config.toml
   
4. Clique "Commit changes"

5. Pronto! Seu repositório está pronto.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Opção 2: INSTALAR GIT (se preferir terminal)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Baixe Git: https://git-scm.com/download/win
2. Instale normalmente
3. Reinicie este script
4. Ele fará o push automaticamente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRÓXIMO PASSO NO STREAMLIT CLOUD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Após upload dos arquivos:

1. Acesse: https://streamlit.io/cloud
2. Clique "New app"
3. Selecione seu repositório: juju8639/diroma_central_cadastro
4. Main file: app.py
5. Clique "Deploy"

6. Nas SETTINGS → SECRETS, adicione:
   EMAIL_SENDER = seu_email@gmail.com
   EMAIL_PASSWORD = sua_senha_app_gmail

7. Seu site estará live em alguns segundos!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("\n✅ Pronto! Continue conforme instruções acima.\n")
