# Script para fazer upload automático via GitHub Desktop
# Este script clona, copia arquivos e faz push

# Configurações
$GIT_EXE = "C:\Users\dougl\AppData\Local\GitHubDesktop\app-3.5.4\resources\app\git\cmd\git.exe"
$REPO_URL = "https://github.com/juju8639/diroma_central_cadastro.git"
$CADASTRO_DIR = "c:\cadastro"
$TEMP_DIR = "$env:TEMP\diroma_upload"
$REPO_DIR = "$TEMP_DIR\diroma_central_cadastro"

# Arquivos a copiar
$ARQUIVOS = @(
    "app.py",
    "requirements.txt",
    "logo.svg",
    "README.md",
    "DEPLOY_PRONTO.md",
    ".gitignore",
    "COMECE_AQUI.md"
)

# Pastas a copiar
$PASTAS = @(
    ".streamlit"
)

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🚀 UPLOAD AUTOMÁTICO - diRoma Central de Cadastro" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

# Step 1: Limpeza
Write-Host "`n🧹 Limpando pasta temporária..."
if (Test-Path $TEMP_DIR) {
    Remove-Item -Path $TEMP_DIR -Recurse -Force
    Write-Host "   ✅ Pasta removida"
}
New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null
Write-Host "   ✅ Pasta criada: $TEMP_DIR"

# Step 2: Clone
Write-Host "`n📥 Clonando repositório..."
Write-Host "   URL: $REPO_URL"

& $GIT_EXE clone $REPO_URL $REPO_DIR
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao clonar repositório" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Repositório clonado"

# Step 3: Copiar arquivos
Write-Host "`n📁 Copiando arquivos..."
$COPIED = 0

foreach ($arquivo in $ARQUIVOS) {
    $SRC = Join-Path $CADASTRO_DIR $arquivo
    $DST = Join-Path $REPO_DIR $arquivo
    
    if (Test-Path $SRC) {
        Copy-Item -Path $SRC -Destination $DST -Force
        Write-Host "   ✅ $arquivo"
        $COPIED++
    } else {
        Write-Host "   ⚠️  $arquivo não encontrado" -ForegroundColor Yellow
    }
}

# Copiar pastas
foreach ($pasta in $PASTAS) {
    $SRC = Join-Path $CADASTRO_DIR $pasta
    $DST = Join-Path $REPO_DIR $pasta
    
    if (Test-Path $SRC) {
        if (Test-Path $DST) {
            Remove-Item -Path $DST -Recurse -Force
        }
        Copy-Item -Path $SRC -Destination $DST -Recurse -Force
        Write-Host "   ✅ $pasta/"
        $COPIED++
    } else {
        Write-Host "   ⚠️  $pasta/ não encontrado" -ForegroundColor Yellow
    }
}

Write-Host "`n   Total: $COPIED itens copiados"

# Step 4: Commit e Push
Write-Host "`n📤 Enviando para GitHub..."

Push-Location $REPO_DIR

# Adicionar todos os arquivos
& $GIT_EXE add -A
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Erro ao adicionar arquivos" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "   ✅ Arquivos preparados"

# Commit
$COMMIT_MSG = "✨ Deploy automático - app.py, emails, logo e documentação completa"
& $GIT_EXE commit -m $COMMIT_MSG
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Erro ao fazer commit" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "   ✅ Commit realizado"

# Push
& $GIT_EXE push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ⚠️  Erro ao fazer push (pode ser erro de autenticação)" -ForegroundColor Yellow
    Write-Host "   📝 Tente manualmente no GitHub Desktop ou configure credenciais" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Push realizado com sucesso!"
}

Pop-Location

# Sucesso
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "✅ UPLOAD CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

Write-Host "`n📝 Próximas etapas:" -ForegroundColor Green
Write-Host "   1. Acesse: https://streamlit.io/cloud" -ForegroundColor White
Write-Host "   2. Clique em 'New app'" -ForegroundColor White
Write-Host "   3. Selecione seu repositório" -ForegroundColor White
Write-Host "   4. Clique em 'Deploy'" -ForegroundColor White
Write-Host "`n⏱️  Seu app estará live em ~2 minutos!" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

Write-Host "`n🎉 Pressione Enter para fechar..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
