#!/usr/bin/env python3
"""
Script para fazer upload automático de arquivos para GitHub
Desenvolvido para diRoma Central de Cadastro
"""

import os
import shutil
from pathlib import Path
from git import Repo
import time

# Configurações
REPO_URL = "https://github.com/juju8639/diroma_central_cadastro.git"
CADASTRO_DIR = Path("c:/cadastro")
TEMP_DIR = Path(os.getenv("TEMP")) / "diroma_upload"
REPO_DIR = TEMP_DIR / "diroma_central_cadastro"

# Arquivos a fazer upload
ARQUIVOS = [
    "app.py",
    "requirements.txt",
    "logo.svg",
    "README.md",
    "DEPLOY_PRONTO.md",
    ".gitignore",
    "COMECE_AQUI.md",
]

PASTAS = [
    ".streamlit",
]

def clean_temp():
    """Remove pasta temporária antiga"""
    if TEMP_DIR.exists():
        print(f"🧹 Removendo pasta temporária antiga: {TEMP_DIR}")
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

def clone_repo():
    """Clone do repositório"""
    print(f"\n📥 Clonando repositório...")
    print(f"   URL: {REPO_URL}")
    try:
        repo = Repo.clone_from(REPO_URL, REPO_DIR)
        print(f"   ✅ Repositório clonado em: {REPO_DIR}")
        return repo
    except Exception as e:
        print(f"   ❌ Erro ao clonar: {e}")
        return None

def copy_files(repo):
    """Copia arquivos necessários"""
    print(f"\n📁 Copiando arquivos...")
    copied = 0
    
    # Copiar arquivos
    for arquivo in ARQUIVOS:
        src = CADASTRO_DIR / arquivo
        dst = REPO_DIR / arquivo
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ {arquivo}")
            copied += 1
        else:
            print(f"   ⚠️  {arquivo} não encontrado")
    
    # Copiar pastas
    for pasta in PASTAS:
        src = CADASTRO_DIR / pasta
        dst = REPO_DIR / pasta
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"   ✅ {pasta}/")
            copied += 1
        else:
            print(f"   ⚠️  {pasta}/ não encontrado")
    
    print(f"\n   Total: {copied} itens copiados")
    return copied > 0

def commit_and_push(repo):
    """Commit e push dos arquivos"""
    print(f"\n📤 Enviando para GitHub...")
    
    try:
        # Adicionar todos os arquivos
        repo.git.add(A=True)
        print(f"   ✅ Arquivos preparados")
        
        # Commit
        commit_msg = "✨ Deploy automático - app.py, emails, logo e documentação completa"
        repo.index.commit(commit_msg)
        print(f"   ✅ Commit: {commit_msg}")
        
        # Push
        origin = repo.remote(name='origin')
        origin.push()
        print(f"   ✅ Push realizado com sucesso!")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 UPLOAD AUTOMÁTICO - diRoma Central de Cadastro")
    print("=" * 60)
    
    # Step 1: Limpeza
    clean_temp()
    
    # Step 2: Clone
    repo = clone_repo()
    if not repo:
        print("\n❌ Falha ao clonar repositório")
        return False
    
    # Step 3: Cópia de arquivos
    if not copy_files(repo):
        print("\n❌ Falha ao copiar arquivos")
        return False
    
    # Step 4: Commit e Push
    if not commit_and_push(repo):
        print("\n❌ Falha ao enviar para GitHub")
        return False
    
    # Sucesso!
    print("\n" + "=" * 60)
    print("✅ UPLOAD CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\n📝 Próximas etapas:")
    print("   1. Acesse: https://streamlit.io/cloud")
    print("   2. Clique em 'New app'")
    print("   3. Selecione seu repositório")
    print("   4. Clique em 'Deploy'")
    print("\n⏱️  Seu app estará live em ~2 minutos!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Pressione Enter para fechar...")
            input()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
import os
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r"C:\Users\dougl\AppData\Local\GitHubDesktop\app-3.5.4\resources\app\git\cmd\git.exe"

import shutil
from pathlib import Path
from git import Repo
import time
