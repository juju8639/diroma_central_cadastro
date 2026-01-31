# 🏢 diRoma - Central de Cadastro
## Versão Streamlit Cloud

---

## 🚀 Deploy no Streamlit Cloud

Este é um app Streamlit pronto para ser deployado gratuitamente na **Streamlit Cloud**.

### Passo 1: Preparar GitHub

1. Crie um repositório no GitHub
2. Faça upload dos arquivos:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `logo.svg`

### Passo 2: Configurar Streamlit Cloud

1. Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
2. Clique em "New app"
3. Selecione seu repositório GitHub
4. Defina:
   - **Repository**: seu repositório
   - **Branch**: main (ou sua branch padrão)
   - **Main file path**: `app.py`

### Passo 3: Configurar Variáveis de Ambiente

No painel de settings do Streamlit Cloud (⚙️ Settings):

1. Vá até "Secrets"
2. Adicione:

```toml
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_app_gmail"
```

#### Como obter a senha de app do Gmail:

1. Ative 2FA em sua conta Google
2. Vá para: https://myaccount.google.com/apppasswords
3. Selecione "Mail" e "Windows Computer"
4. Google gerará uma senha de 16 caracteres
5. Use essa senha em `EMAIL_PASSWORD`

---

## 📧 Configuração de Emails

O sistema envia emails automaticamente quando:
- ✅ Uma nova solicitação é criada
- ✅ Uma solicitação é respondida

**Emails são enviados para:**
- O usuário que criou a solicitação
- O administrador (padrão: `juliano.teixeira@diroma.com.br`)

---

## 🔐 Credenciais Padrão

**Admin:**
- Email: `juliano.teixeira@diroma.com.br`
- Senha: `abc123`

⚠️ **Altere imediatamente na primeira execução!**

---

## 📊 Recursos

- ✅ Dashboard premium com design moderno
- ✅ Sistema de solicitações (Itens, Compras, Fornecedores)
- ✅ Notificações sonoras no navegador
- ✅ Notificações por email
- ✅ Filtros avançados por data, hotel, categoria
- ✅ Painel administrativo completo
- ✅ Responsivo para mobile

---

## 🛠️ Suporte Técnico

### Erro: "Permissão negada ao escrever no banco de dados"
**Solução:** Streamlit Cloud cria automaticamente um diretório para dados persistentes. Certifique-se de que `app.db` esteja no `.gitignore` (arquivos de dados não devem ser versionados).

### Erro: "Email não foi enviado"
**Verificação:**
1. As credenciais estão corretas em "Secrets"?
2. Você ativou 2FA no Gmail?
3. Está usando senha de app (16 caracteres), não a senha principal?
4. Seu IP/provedor não está bloqueado por Gmail?

---

## 📦 Estrutura de Arquivos

```
diRoma_Central_Cadastro/
├── app.py                    # Aplicação principal
├── requirements.txt          # Dependências Python
├── logo.svg                  # Logo diRoma
├── .streamlit/
│   └── config.toml          # Configuração Streamlit
├── uploads/                 # Pasta para anexos (criada automaticamente)
├── app.db                   # Banco de dados SQLite (criado automaticamente)
└── README.md                # Este arquivo
```

---

## 🌐 Links Úteis

- [Streamlit Cloud](https://streamlit.io/cloud)
- [Documentação Streamlit](https://docs.streamlit.io)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [GitHub](https://github.com)

---

**Desenvolvido com ❤️ usando Streamlit**  
**Versão 1.0 | Janeiro 2026**
