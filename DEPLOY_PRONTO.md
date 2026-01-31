# 🚀 Pronto para Deploy - diRoma Central de Cadastro

## ✅ O que foi feito

### 1️⃣ Notificações por Email
- ✅ Quando uma nova solicitação é criada → email para usuário + admin
- ✅ Quando uma solicitação é respondida → email para usuário
- ✅ Configuração via variáveis de ambiente (seguro)

### 2️⃣ Arquivos Limpos
Removidos arquivos desnecessários:
- `start_server.py`
- `server.py`
- `run_both.bat`, `run_streamlit.bat`, `ABRIR.bat`, `iniciar.bat`
- `dashboard.html`, `teste.html`, `streamlit_app.py`
- `app.py.backup`, `COMPARTILHAR.md`

### 3️⃣ Preparado para Streamlit Cloud
- ✅ `.streamlit/config.toml` criado
- ✅ `requirements.txt` atualizado
- ✅ `.gitignore` configurado
- ✅ `README.md` pronto com instruções

---

## 📋 Arquivos Finais (Seu Repositório)

```
seu_repositorio_github/
├── app.py                    # App principal com notificações por email
├── requirements.txt          # Dependências
├── logo.svg                  # Logo diRoma
├── .streamlit/
│   └── config.toml          # Config Streamlit
├── .gitignore               # Arquivos ignorados
├── README.md                # Instruções deploy
└── uploads/                 # Pasta (criada automaticamente)
```

---

## 🌐 Como Deploy no Streamlit Cloud

### Passo 1: GitHub
1. Crie repositório no GitHub
2. Faça upload de TODOS os arquivos acima
3. Commit & Push

### Passo 2: Streamlit Cloud
1. Vá em: https://streamlit.io/cloud
2. Clique "New app"
3. Selecione seu repositório + `app.py`

### Passo 3: Secrets (Variáveis de Ambiente)
No painel do Streamlit Cloud (⚙️ Settings → Secrets):

```toml
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_app_gmail"
```

**Como obter a senha de app:**
1. Google Account → https://myaccount.google.com/apppasswords
2. Ative 2FA se não tiver
3. Selecione "Mail" e "Windows Computer"
4. Google gera uma senha de 16 caracteres → use essa

### Passo 4: Pronto! 🎉
O app está live em:
```
https://seu_usuario-seu_repositorio-xxxxx.streamlit.app
```

---

## 🧪 Testar Localmente Antes de Deploy

```powershell
cd c:\cadastro
pip install -r requirements.txt
streamlit run app.py
```

Acesse: `http://localhost:8501`

---

## 📧 Teste de Emails

1. Faça login como usuário
2. Crie uma solicitação
3. Verifique se recebeu email em:
   - Seu email (usuário)
   - `juliano.teixeira@diroma.com.br` (admin)

Para testar resposta:
1. Faça login como admin (`juliano.teixeira@diroma.com.br` / `abc123`)
2. Vá em "Painel Admin"
3. Responda uma solicitação
4. Verifique email do usuário

---

## 🔐 Credenciais Padrão

**Admin:**
- Email: `juliano.teixeira@diroma.com.br`
- Senha: `abc123`

⚠️ **ALTERE NA PRIMEIRA EXECUÇÃO!**

---

## 🎯 Checklist Final

- [ ] Arquivo `.gitignore` criado
- [ ] `requirements.txt` atualizado
- [ ] `.streamlit/config.toml` criado
- [ ] `app.py` tem notificações por email
- [ ] `README.md` com instruções
- [ ] `logo.svg` presente
- [ ] Repositório GitHub criado
- [ ] Todos os arquivos comitados
- [ ] Streamlit Cloud conectado
- [ ] Secrets (`EMAIL_SENDER`, `EMAIL_PASSWORD`) configurados
- [ ] App rodando em `https://seu_app.streamlit.app`

---

## 🐛 Troubleshooting

### Email não funciona?
1. Verifique as secrets no Streamlit Cloud
2. Confirme que é senha de app (16 caracteres), não a senha principal
3. Verifique se 2FA está ativado na conta Google
4. Veja logs no Streamlit Cloud

### Dados desaparecem ao reiniciar?
Normal em Streamlit Cloud. Use:
- Para produção: Integre Firestore, PostgreSQL, ou Supabase
- Para agora: Dados permanecem enquanto app estiver rodando

### App fica muito lento?
1. Otimize as queries do banco
2. Use `@st.cache_data` para dados estáticos
3. Considere migrar para banco de dados em nuvem

---

## 📞 Próximos Passos

Se precisar de mais:
1. **Banco de dados em nuvem**: Firebase Firestore ou Supabase
2. **Autenticação social**: Login com Google/GitHub
3. **Pagamentos**: Integração Stripe/PayPal
4. **Analytics**: Google Analytics ou Mixpanel

---

**Status:** ✅ Pronto para deploy  
**Data:** Janeiro 2026  
**Versão:** 1.0
