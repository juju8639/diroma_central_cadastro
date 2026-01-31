"""
Sistema de Solicitações - Design Premium Dashboard
Inspirado em padrões corporativos modernos
"""

import os
import json
import sqlite3
import hashlib
import secrets
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

APP_TITLE = "diRoma | Central de Cadastro"
DB_PATH = "app.db"
UPLOAD_DIR = "uploads"

ADMIN_EMAIL = "juliano.teixeira@diroma.com.br"
ADMIN_PASSWORD = "abc123"
ADMIN_EMAILS = {ADMIN_EMAIL}

# EMAIL CONFIGURATION
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "seu_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "sua_senha_app")
EMAIL_SMTP = "smtp.gmail.com"
EMAIL_PORT = 587

HOTELS = [
    ("01", "Roma Empreendimento Matriz", "ROMA_EMPREENDIMENTO"),
    ("02", "Roma Empreendimento Filial", "ROMA_EMPREENDIMENTO"),
    ("03", "Império Romano", "ROMA_HOTEIS"),
    ("04", "Villas", "ROMA_HOTEIS"),
    ("05", "Hotel Roma", "ROMA_HOTEIS"),
    ("06", "Resort", "ROMA_HOTEIS"),
    ("07", "Fiori", "ROMA_HOTEIS"),
    ("09", "Thermas Secretária", "ROMA_HOTEIS"),
    ("10", "Jardins Comercial", "ROMA_HOTEIS"),
    ("11", "Exclusive", "ROMA_HOTEIS"),
    ("12", "Lacqua I", "ROMA_HOTEIS"),
    ("13", "Lacqua II", "ROMA_HOTEIS"),
    ("14", "Lacqua III", "ROMA_HOTEIS"),
    ("15", "Lacqua IV", "ROMA_HOTEIS"),
    ("16", "Lacqua V", "ROMA_HOTEIS"),
    ("17", "Jardins Acqua Park", "ROMA_HOTEIS"),
    ("18", "Piazza", "ROMA_HOTEIS"),
    ("19", "Spazzio", "SPAZZIO"),
]

CONTAS_POR_GRUPO = {
    "ROMA_EMPREENDIMENTO": {
        "Alimentos": ("1.1.02.020.0001", "5.1.02.004"),
        "Bebidas": ("1.1.02.020.0002", "5.1.02.001"),
        "Material de Limpeza": ("1.1.02.020.0003", "6.2.01.101"),
        "Material de Escritório": ("1.1.02.020.0004", "6.2.01.209"),
        "Embalagens": ("1.1.02.020.0005", "6.2.01.103"),
        "Boutique": ("1.1.02.020.0007", "5.1.02.003"),
        "Material de Manutenção": ("1.1.02.020.0008", "6.2.01.401"),
        "Utensílios": ("1.1.02.020.0009", "6.2.01.106"),
        "Óleo Diesel": ("1.1.02.020.0010", "6.2.01.201"),
        "Material p/ Hóspede": ("1.1.02.020.0013", "6.2.01.102"),
        "Gás Cozinha": ("1.1.02.020.0014", "6.2.01.104"),
        "SESMT - Seg. Med. Trab.": ("1.1.02.020.0015", "6.1.01.007"),
    },
    "ROMA_HOTEIS": {
        "Alimentos": ("1.1.02.020.0001", "5.1.02.007"),
        "Bebidas": ("1.1.02.020.0002", "5.1.02.001"),
        "Material de Limpeza": ("1.1.02.020.0003", "6.2.01.101"),
        "Material de Escritório": ("1.1.02.020.0004", "6.2.01.208"),
        "Embalagens": ("1.1.02.020.0005", "6.2.01.103"),
        "Material de Manutenção": ("1.1.02.020.0008", "6.2.01.401"),
        "Utensílios": ("1.1.02.020.0009", "6.2.01.106"),
        "Recreação": ("1.1.02.020.0010", "6.2.01.105"),
        "Uniforme": ("1.1.02.020.0011", "6.1.01.006"),
        "Material p/ Hóspede": ("1.1.02.020.0013", "6.2.01.102"),
        "SESMT - Segurança do Trabalho": ("1.1.02.020.0015", "6.1.01.006"),
    },
    "SPAZZIO": {
        "Alimentos": ("1.1.02.010.0001", "5.1.02.001"),
        "Bebidas": ("1.1.02.010.0002", "5.1.02.002"),
        "Material de Limpeza": ("1.1.02.010.0003", "6.2.01.101"),
        "Material de Escritório": ("1.1.02.010.0004", "6.2.01.201"),
        "Embalagens": ("1.1.02.010.0005", "6.2.01.105"),
        "Material de Manutenção": ("1.1.02.010.0006", "6.2.01.301"),
        "Utensílios": ("1.1.02.010.0007", "6.2.01.106"),
        "Material p/ Hóspede": ("1.1.02.010.0009", "6.2.01.102"),
        "SESMT - Seg. Med. Trab.": ("1.1.02.010.0010", "6.1.01.005"),
    },
}

HOTEL_OPTIONS = [f"{code} - {name}" for code, name, _ in HOTELS]
HOTEL_BY_CODE = {code: {"name": name, "group": group} for code, name, group in HOTELS}


# ============================================================================
# STREAMLIT CONFIG
# ============================================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS PREMIUM - NOVO DESIGN
CSS = """
<style>
/* Fundo geral */
.stApp {
  background: radial-gradient(1200px 600px at 50% 0%, #3d5b86 0%, #223552 45%, #1a2a42 100%);
}

/* remove padding default e controla largura */
.block-container {
  padding-top: 1.0rem;
  padding-bottom: 2.0rem;
  max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1b2f4b 0%, #13243a 55%, #0f1d31 100%);
  border-right: 1px solid rgba(255,255,255,0.06);
}
.sidebar-brand {
  display:flex;
  align-items:center;
  gap:10px;
  padding: 8px 6px 14px 6px;
  color:#ffffff;
  font-weight:700;
  font-size:22px;
  letter-spacing:0.2px;
}
.sidebar-user {
  display:flex;
  align-items:center;
  gap:10px;
  padding: 10px 6px 14px 6px;
  color:#d9e4ff;
  font-size:14px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  margin-bottom: 10px;
}
.pill {
  display:inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: rgba(72,118,255,0.18);
  border: 1px solid rgba(110,150,255,0.25);
  color:#dfe9ff;
  font-size:12px;
}
.sidebar-item {
  margin: 6px 0;
}
.sidebar-item button {
  width: 100%;
  text-align: left;
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  background: rgba(255,255,255,0.04) !important;
  color: #eaf1ff !important;
  padding: 10px 12px !important;
  font-weight: 500 !important;
}
.sidebar-item button:hover{
  border: 1px solid rgba(120,160,255,0.35) !important;
  background: rgba(120,160,255,0.12) !important;
}

/* Topbar */
.topbar {
  background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.75) 100%);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 18px;
  padding: 14px 16px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.22);
  margin-bottom: 20px;
}
.topbar-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
}
.topbar-left{
  display:flex;
  align-items:center;
  gap: 12px;
  color:#1a2a42;
}
.iconbtn{
  width: 36px;
  height: 36px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius: 12px;
  background: rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.06);
  cursor: pointer;
}
.searchbox{
  display:flex;
  align-items:center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 14px;
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(0,0,0,0.07);
  min-width: 280px;
  flex: 1;
  max-width: 500px;
}
.profile{
  display:flex;
  align-items:center;
  gap: 10px;
  color:#1a2a42;
  font-weight:600;
}
.avatar{
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6c8cff 0%, #3f63ff 100%);
  display:flex;
  align-items:center;
  justify-content:center;
  color:white;
  font-weight:800;
  font-size: 12px;
}

/* Título principal */
.h1 {
  color: #eaf1ff;
  font-size: 28px;
  font-weight: 800;
  margin: 20px 0 14px 0;
  text-shadow: 0 10px 26px rgba(0,0,0,0.25);
}
.h1 span{
  color:#d8e6ff;
  font-weight:700;
}

/* Cards */
.grid {
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 16px;
}
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.78) 100%);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 18px;
  padding: 16px 16px 14px 16px;
  box-shadow: 0 14px 32px rgba(0,0,0,0.24);
  position: relative;
  overflow: hidden;
}
.card:before{
  content:"";
  position:absolute;
  inset:-40px -60px auto auto;
  width: 280px;
  height: 160px;
  background: radial-gradient(circle at 30% 30%, rgba(90,140,255,0.18), rgba(255,255,255,0));
  transform: rotate(8deg);
}
.card-title{
  display:flex;
  align-items:center;
  gap: 10px;
  color:#1a2a42;
  font-size: 18px;
  font-weight: 800;
}
.card-sub{
  color: rgba(26,42,66,0.75);
  margin-top: 4px;
  font-size: 13px;
}
.card-btnrow{
  margin-top: 14px;
  display:flex;
  justify-content:flex-end;
}
.primary-btn{
  padding: 10px 18px;
  border-radius: 14px;
  background: linear-gradient(180deg, #4c78ff 0%, #2d55e8 100%);
  color: white;
  font-weight: 700;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 10px 18px rgba(46,86,232,0.35);
  cursor:pointer;
  user-select:none;
}
.primary-btn:hover{
  filter: brightness(1.05);
}

/* Form container */
.form-container {
  background: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.78) 100%);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 14px 32px rgba(0,0,0,0.24);
  margin-top: 16px;
}

/* Ajuste Streamlit: esconder headers */
header[data-testid="stHeader"] {background: transparent;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================================
# UTILITÁRIOS
# ============================================================================

def ensure_dirs():
    Path(UPLOAD_DIR).mkdir(exist_ok=True)


def send_email(to_email: str, subject: str, body: str):
    """Envia email para notificação"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False


def notify_new_request(user_email: str, req_id: int, category: str, subcategory: str, hotel_name: str):
    """Notifica sobre nova solicitação"""
    subject = f"✅ Solicitação #{req_id} Criada - {category}"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #4c78ff;">✅ Nova Solicitação Criada</h2>
            <p>Sua solicitação foi registrada com sucesso!</p>
            <table style="width:100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><b>ID Solicitação:</b></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">#{req_id}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><b>Categoria:</b></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{category}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><b>Tipo:</b></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{subcategory}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><b>Hotel:</b></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{hotel_name}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><b>Status:</b></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">⏳ Pendente</td>
                </tr>
            </table>
            <p>Você receberá uma notificação quando sua solicitação for respondida.</p>
            <p><small>diRoma - Central de Cadastro</small></p>
        </body>
    </html>
    """
    send_email(user_email, subject, body)
    send_email(ADMIN_EMAIL, f"📥 Nova Solicitação - {category}", body)


def notify_response(user_email: str, req_id: int, response: str):
    """Notifica sobre resposta a solicitação"""
    subject = f"✅ Sua Solicitação #{req_id} foi Respondida!"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #4c78ff;">✅ Solicitação Respondida</h2>
            <p>Sua solicitação #<b>{req_id}</b> foi respondida!</p>
            <div style="background-color: #f0f7ff; padding: 15px; border-left: 4px solid #4c78ff; margin: 20px 0;">
                <h3>Resposta do Administrador:</h3>
                <p>{response}</p>
            </div>
            <p>Acesse o sistema para mais detalhes.</p>
            <p><small>diRoma - Central de Cadastro</small></p>
        </body>
    </html>
    """
    send_email(user_email, subject, body)

def play_notification(kind: str):
    """Plays a short beep in the browser. kind: 'new' or 'responded'"""
    if kind == "new":
        freq = 880
    else:
        freq = 440
    # Generate a short WAV beep on the server and embed as base64 audio element.
    try:
        import io
        import base64
        import math
        import struct
        import wave

        duration = 0.16  # seconds
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        max_amp = 32767 // 3

        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            frames = bytearray()
            for i in range(n_samples):
                t = i / sample_rate
                sample = int(max_amp * math.sin(2.0 * math.pi * freq * t))
                frames += struct.pack('<h', sample)
            wf.writeframes(frames)

        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        audio_html = f'<audio autoplay><source src="data:audio/wav;base64,{b64}" type="audio/wav"></audio>'
        try:
            from streamlit.components.v1 import html as _html
            _html(audio_html, height=0)
        except Exception:
            # Fallback: try injecting as markdown (less reliable)
            try:
                st.markdown(audio_html, unsafe_allow_html=True)
            except Exception:
                pass
    except Exception:
        # If audio generation fails, silently ignore to avoid breaking the app
        pass

def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def hash_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = secrets.token_bytes(16)
    pw = password.encode("utf-8")
    dk = hashlib.pbkdf2_hmac("sha256", pw, salt, 120_000)
    return salt.hex(), dk.hex()

def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    _, candidate = hash_password(password, salt)
    return secrets.compare_digest(candidate, hash_hex)

def save_upload_file(uploaded_file) -> str:
    ensure_dirs()
    if not uploaded_file:
        return ""
    ext = os.path.splitext(uploaded_file.name)[1].lower() or ".bin"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_name = f"{timestamp}_{secrets.token_hex(6)}{ext}"
    dest = os.path.join(UPLOAD_DIR, new_name)
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest

def nav_button(label, page_name, icon=""):
    """Botão de navegação"""
    if st.sidebar.button(f"{icon} {label}", use_container_width=True, key=f"nav_{page_name}"):
        st.session_state.page = page_name
        st.rerun()


def render_menu():
    """Renderizar menu na sidebar"""
    # Logo e brand
    st.sidebar.markdown(
        """<div class="sidebar-brand" style="display:flex; align-items:center; gap:8px; margin-bottom:20px;">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 80'%3E%3Cdefs%3E%3ClinearGradient id='blueGrad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%234c78ff;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%232d55e8;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Ctext x='20' y='55' font-family='Arial' font-size='48' font-weight='bold' fill='url(%23blueGrad)' letter-spacing='2'%3EdiRoma%3C/text%3E%3Cpath d='M 10 65 Q 20 60, 30 65 T 50 65' stroke='%234c78ff' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E" style="width:32px; height:32px;" />
          <span style="font-weight:700; font-size:16px;">diRoma</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # User Info
    email_parts = st.session_state.user_email.split("@")[0].split(".")
    nome_usuario = " ".join([p.capitalize() for p in email_parts])
    iniciais = "".join([p[0].upper() for p in email_parts[:2]])
    
    user_role = "Admin" if st.session_state.user_role == "admin" else "Usuário"
    
    st.sidebar.markdown(
        f"""<div class="sidebar-user" style="margin-bottom:20px;">
          <div class="avatar">{iniciais}</div>
          <div style="display:flex; flex-direction:column; gap:2px; flex:1;">
            <div style="font-weight:700; color:#ffffff; font-size:14px;">{nome_usuario}</div>
            <div style="font-size:11px; opacity:0.8;">{st.session_state.user_email}</div>
            <div class="pill" style="margin-top:6px;">Perfil: {user_role}</div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    # Menu Items
    nav_button("Dashboard", "menu", "📊")
    nav_button("Itens", "itens", "📋")
    nav_button("Compras", "compras", "🛒")
    nav_button("Fornecedor", "fornecedor", "🏪")
    nav_button("Minhas Solicitações", "minhas_solicitacoes", "✉️")

    if st.session_state.user_role == "admin":
        st.sidebar.markdown("---")
        nav_button("Painel Admin", "admin", "🛠️")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair", use_container_width=True, key="nav_logout"):
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.rerun()


# ============================================================================
# BANCO DE DADOS
# ============================================================================

class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            salt_hex TEXT NOT NULL,
            hash_hex TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            hotel_code TEXT NOT NULL,
            hotel_name TEXT NOT NULL,
            hotel_group TEXT NOT NULL,
            condominio TEXT,
            data_json TEXT NOT NULL,
            image_path TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            admin_response TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
        self.conn.commit()

        cur.execute("SELECT * FROM users WHERE email = ?", (ADMIN_EMAIL,))
        if not cur.fetchone():
            salt_hex, hash_hex = hash_password(ADMIN_PASSWORD)
            cur.execute(
                "INSERT INTO users(email, salt_hex, hash_hex, role, created_at) VALUES (?,?,?,?,?)",
                (ADMIN_EMAIL, salt_hex, hash_hex, "admin", now_iso()),
            )
            self.conn.commit()

    def get_user(self, email: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
        return cur.fetchone()

    def create_user(self, email: str, password: str):
        email = email.strip().lower()
        salt_hex, hash_hex = hash_password(password)
        role = "admin" if email in ADMIN_EMAILS else "user"
        cur = self.conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users(email, salt_hex, hash_hex, role, created_at) VALUES (?,?,?,?,?)",
                (email, salt_hex, hash_hex, role, now_iso()),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def create_request(self, user_id: int, user_email: str, category: str, 
                      subcategory: str, hotel_code: str, hotel_name: str, 
                      hotel_group: str, condominio: str, data: dict, image_path: str = ""):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO requests(
                user_id, user_email, category, subcategory,
                hotel_code, hotel_name, hotel_group, condominio,
                data_json, image_path, status, admin_response, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id, user_email, category, subcategory,
            hotel_code, hotel_name, hotel_group, condominio,
            json.dumps(data, ensure_ascii=False), image_path,
            "Pendente", None, now_iso(), now_iso()
        ))
        self.conn.commit()

    def get_user_requests(self, user_id: int):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM requests WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        return cur.fetchall()

    def get_all_requests(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
        return cur.fetchall()

    def get_request(self, req_id: int):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM requests WHERE id = ?", (req_id,))
        return cur.fetchone()

    def update_request(self, req_id: int, status: str, response: str):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE requests SET status = ?, admin_response = ?, updated_at = ? WHERE id = ?",
            (status, response or None, now_iso(), req_id)
        )
        self.conn.commit()


# ============================================================================
# SESSÃO
# ============================================================================

def init_session():
    if "db" not in st.session_state:
        st.session_state.db = Database(DB_PATH)
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.user_role = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

init_session()


# ============================================================================
# PÁGINAS
# ============================================================================

def page_login():
    """Tela de Login/Cadastro"""
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        # Header
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 32px; margin-top: 60px;'>
                <div style='margin-bottom: 12px;'><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 80'%3E%3Cdefs%3E%3ClinearGradient id='blueGrad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%234c78ff;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%232d55e8;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Ctext x='20' y='55' font-family='Arial' font-size='48' font-weight='bold' fill='url(%23blueGrad)' letter-spacing='2'%3EdiRoma%3C/text%3E%3Cpath d='M 10 65 Q 20 60, 30 65 T 50 65' stroke='%234c78ff' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E" style="width:150px; height:60px;" /></div>
                <h1 style='color: #eaf1ff; font-size: 32px; margin: 0 0 8px 0; font-weight: 800;'>diRoma</h1>
                <p style='color: #cbd5e1; font-size: 14px; margin: 0;'>Central de Cadastro</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Container
        st.markdown(
            """
            <div class="form-container">
            """,
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])

        with tab1:
            st.write("**Faça Login**")
            email = st.text_input("E-mail", placeholder="seu.email@diroma.com.br", key="login_email")
            password = st.text_input("Senha", type="password", placeholder="sua senha", key="login_pwd")
            
            if st.button("Entrar", use_container_width=True, key="btn_login"):
                if not email or not password:
                    st.error("⚠️ Preencha todos os campos")
                    return
                
                if not email.endswith("@diroma.com.br"):
                    st.error("❌ Use um e-mail @diroma.com.br")
                    return
                
                user = st.session_state.db.get_user(email)
                if not user:
                    st.error("❌ Usuário não encontrado")
                    return
                
                if not verify_password(password, user["salt_hex"], user["hash_hex"]):
                    st.error("❌ Senha inválida")
                    return
                
                st.session_state.authenticated = True
                st.session_state.user_id = user["id"]
                st.session_state.user_email = user["email"]
                st.session_state.user_role = user["role"]
                st.session_state.page = "menu"
                st.success("✅ Login realizado!")
                time.sleep(1)
                st.rerun()

        with tab2:
            st.write("**Criar Conta**")
            email = st.text_input("E-mail", placeholder="seu.email@diroma.com.br", key="reg_email")
            password = st.text_input("Senha", type="password", placeholder="sua senha", key="reg_pwd1")
            confirm = st.text_input("Confirmar", type="password", placeholder="confirme a senha", key="reg_pwd2")
            
            if st.button("Criar Conta", use_container_width=True, key="btn_register"):
                if not email or not password or not confirm:
                    st.error("⚠️ Preencha todos os campos")
                    return
                if not email.endswith("@diroma.com.br"):
                    st.error("❌ Use um e-mail @diroma.com.br")
                    return
                if password != confirm:
                    st.error("❌ Senhas não conferem")
                    return
                
                if st.session_state.db.create_user(email, password):
                    st.success("✅ Conta criada! Faça login agora")
                else:
                    st.error("❌ E-mail já cadastrado")

        st.markdown("</div>", unsafe_allow_html=True)


def page_menu():
    """Menu Principal - Dashboard com novo design"""
    # Topbar com search e profile
    st.markdown(
        f"""<div class="topbar">
          <div class="topbar-row">
            <div style="display:flex; gap:8px;">
              <div class="topbar-icon">📱</div>
              <div class="topbar-icon">🔔</div>
              <div class="topbar-icon">⚙️</div>
            </div>
            <div class="searchbox">
              <span style="color:#1a2a42; opacity:0.7;">🔍</span>
              <input type="text" placeholder="Pesquisar..." style="border:none; background:transparent; outline:none; color:#1a2a42; flex:1; font-size:13px;" />
            </div>
            <div class="profile">
              <div class="avatar" style="width:32px; height:32px;">{''.join([p[0].upper() for p in st.session_state.user_email.split('@')[0].split('.')[:2]])}</div>
              <div style="text-align:right;">
                <div style="font-size:13px; font-weight:600;">Perfil</div>
                <div style="font-size:11px; opacity:0.8;">{st.session_state.user_email}</div>
              </div>
            </div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # Título principal
    st.markdown(
        """<div class="h1">Bem-vindo à <span>Central de Cadastro</span></div>""",
        unsafe_allow_html=True,
    )

    # Grid de cards
    st.markdown(
        """<div class="grid">""",
        unsafe_allow_html=True,
    )

    # Card 1: Itens
    st.markdown(
        """<div class="card">
          <div class="card-title">📋 Itens</div>
          <div class="card-sub">Cadastrar novos itens para o sistema</div>
          <div class="card-btnrow">""",
        unsafe_allow_html=True,
    )
    if st.button("Acessar", use_container_width=True, key="btn_itens"):
        st.session_state.page = "itens"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Card 2: Compras
    st.markdown(
        """<div class="card">
          <div class="card-title">🛒 Compras</div>
          <div class="card-sub">Solicitar compras para seus hotéis</div>
          <div class="card-btnrow">""",
        unsafe_allow_html=True,
    )
    if st.button("Acessar", use_container_width=True, key="btn_compras"):
        st.session_state.page = "compras"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Card 3: Fornecedor
    st.markdown(
        """<div class="card">
          <div class="card-title">🏪 Fornecedor</div>
          <div class="card-sub">Cadastrar novos fornecedores</div>
          <div class="card-btnrow">""",
        unsafe_allow_html=True,
    )
    if st.button("Acessar", use_container_width=True, key="btn_fornecedor"):
        st.session_state.page = "fornecedor"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Card 4: Minhas Solicitações
    st.markdown(
        """<div class="card">
          <div class="card-title">✉️ Solicitações</div>
          <div class="card-sub">Gerenciar todas as solicitações</div>
          <div class="card-btnrow">""",
        unsafe_allow_html=True,
    )
    if st.button("Ver Solicitações", use_container_width=True, key="btn_minhas"):
        st.session_state.page = "minhas_solicitacoes"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Card 5: Meu Perfil
    st.markdown(
        """<div class="card">
          <div class="card-title">👤 Perfil</div>
          <div class="card-sub">Editar dados pessoais</div>
          <div class="card-btnrow">""",
        unsafe_allow_html=True,
    )
    if st.button("Acessar", use_container_width=True, key="btn_perfil"):
        st.session_state.page = "perfil"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Card 6: Admin (se for admin)
    if st.session_state.user_role == "admin":
        st.markdown(
            """<div class="card">
              <div class="card-title">🛠️ Administrador</div>
              <div class="card-sub">Gerenciar todas as solicitações</div>
              <div class="card-btnrow">""",
            unsafe_allow_html=True,
        )
        if st.button("Acessar Painel", use_container_width=True, key="btn_admin"):
            st.session_state.page = "admin"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def page_itens():
    """Cadastrar Itens"""
    st.markdown("""
    <div class='page-header'>
        <h1>📦 Cadastrar Itens</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Adicionar novos itens ao sistema</p>
    </div>
    """, unsafe_allow_html=True)

    hotel_label = st.selectbox("Hotel", ["Selecione..."] + HOTEL_OPTIONS, key="itens_hotel")
    if hotel_label == "Selecione...":
        st.info("Selecione um hotel para continuar")
        return

    hotel_code = hotel_label.split(" - ")[0]
    hotel_info = HOTEL_BY_CODE[hotel_code]
    hotel_group = hotel_info["group"]
    
    submenu = st.radio("Tipo de Solicitação", ["Associação", "Itens", "Itens de PDV", "Link"], horizontal=True)
    tipos_insumo = sorted(list(CONTAS_POR_GRUPO.get(hotel_group, {}).keys()))
    condominio = st.radio("Condomínio", ["Não", "Sim"], horizontal=True)

    if submenu == "Associação":
        with st.form("form_assoc"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome")
                codigo = st.text_input("Código")
            with col2:
                tipo_insumo = st.selectbox("Tipo de insumo", ["Selecione..."] + tipos_insumo, key="assoc_tipo")
                if tipo_insumo != "Selecione...":
                    ce, cs = CONTAS_POR_GRUPO[hotel_group].get(tipo_insumo, ("", ""))
                    col_ce, col_cs = st.columns(2)
                    with col_ce:
                        st.text_input("Conta Entrada", value=ce, disabled=True)
                    with col_cs:
                        st.text_input("Conta Saída", value=cs, disabled=True)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="assoc_img")
            obs = st.text_area("Observação", height=80)
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not nome or not codigo or tipo_insumo == "Selecione...":
                    st.error("Preencha os campos obrigatórios")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Associação", "nome": nome, "codigo": codigo, "tipo_insumo": tipo_insumo, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Itens", "Associação", hotel_code, hotel_info["name"], hotel_group, condominio, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Itens", "Associação", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()

    elif submenu == "Itens":
        with st.form("form_itens"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome")
                gramatura = st.text_input("Gramatura")
            with col2:
                tipo_insumo = st.selectbox("Tipo de insumo", ["Selecione..."] + tipos_insumo, key="itens_tipo")
                if tipo_insumo != "Selecione...":
                    ce, cs = CONTAS_POR_GRUPO[hotel_group][tipo_insumo]
                    col_ce, col_cs = st.columns(2)
                    with col_ce:
                        st.text_input("Conta Entrada", value=ce, disabled=True)
                    with col_cs:
                        st.text_input("Conta Saída", value=cs, disabled=True)
            obs = st.text_area("Observação", height=80)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="itens_img")
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not nome or not gramatura or tipo_insumo == "Selecione...":
                    st.error("Preencha os campos obrigatórios")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Itens", "nome": nome, "gramatura": gramatura, "tipo_insumo": tipo_insumo, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Itens", "Itens", hotel_code, hotel_info["name"], hotel_group, condominio, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Itens", "Itens", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()

    elif submenu == "Itens de PDV":
        with st.form("form_pdv"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome")
                gramatura = st.text_input("Gramatura")
            with col2:
                codigo_barras = st.text_input("Código de barras")
            obs = st.text_area("Observação", height=80)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="pdv_img")
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not nome or not gramatura or not codigo_barras:
                    st.error("Preencha os campos obrigatórios")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Itens de PDV", "nome": nome, "gramatura": gramatura, "codigo": codigo_barras, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Itens", "Itens de PDV", hotel_code, hotel_info["name"], hotel_group, condominio, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Itens", "Itens de PDV", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()

    else:
        with st.form("form_link"):
            link = st.text_input("Link")
            obs = st.text_area("Observação", height=100)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="link_img")
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not link:
                    st.error("Informe o link")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Link", "link": link, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Itens", "Link", hotel_code, hotel_info["name"], hotel_group, condominio, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Itens", "Link", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()


def page_compras():
    """Solicitar Compras"""
    st.markdown("""
    <div class='page-header'>
        <h1>🛒 Solicitar Compras</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Fazer novas solicitações de compra</p>
    </div>
    """, unsafe_allow_html=True)
    hotel_label = st.selectbox("Hotel", ["Selecione..."] + HOTEL_OPTIONS, key="comp_hotel")
    if hotel_label == "Selecione...":
        st.info("Selecione um hotel para continuar")
        return
    hotel_code = hotel_label.split(" - ")[0]
    hotel_info = HOTEL_BY_CODE[hotel_code]
    st.divider()
    modo = st.radio("Tipo de Solicitação", ["Via Link", "Via Itens"], horizontal=True)
    st.divider()

    if modo == "Via Link":
        with st.form("form_comp_link"):
            link = st.text_input("Link")
            obs = st.text_area("Observação", height=100)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="comp_link_img")
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not link:
                    st.error("Informe o link")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Compra via Link", "link": link, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Compras", "Via Link", hotel_code, hotel_info["name"], hotel_info["group"], None, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Compras", "Via Link", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()
    else:
        with st.form("form_comp_itens"):
            nome = st.text_input("Nome do item")
            gramatura = st.text_input("Gramatura")
            obs = st.text_area("Observação", height=100)
            img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="comp_itens_img")
            col_sub, col_can = st.columns(2)
            with col_sub:
                submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
            with col_can:
                st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
            if submitted:
                if not nome:
                    st.error("Informe o nome do item")
                    return
                with st.spinner("Salvando solicitação..."):
                    img_path = save_upload_file(img) if img else ""
                    data = {"tipo": "Compra via Itens", "nome": nome, "gramatura": gramatura, "obs": obs}
                    st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Compras", "Via Itens", hotel_code, hotel_info["name"], hotel_info["group"], None, data, img_path)
                    time.sleep(0.5)
                req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
                notify_new_request(st.session_state.user_email, req_id, "Compras", "Via Itens", hotel_info["name"])
                play_notification('new')
                st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
                time.sleep(2)
                st.session_state.page = "minhas_solicitacoes"
                st.rerun()


def page_fornecedor():
    """Cadastrar Fornecedor"""
    st.markdown("""
    <div class='page-header'>
        <h1>🏪 Cadastrar Fornecedor</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Registrar novos fornecedores no sistema</p>
    </div>
    """, unsafe_allow_html=True)
    hotel_label = st.selectbox("Hotel", ["Selecione..."] + HOTEL_OPTIONS, key="forn_hotel")
    if hotel_label == "Selecione...":
        st.info("Selecione um hotel para continuar")
        return
    hotel_code = hotel_label.split(" - ")[0]
    hotel_info = HOTEL_BY_CODE[hotel_code]
    with st.form("form_forn"):
        col1, col2 = st.columns(2)
        with col1:
            tipo_doc = st.radio("Tipo", ["CNPJ", "CPF"], horizontal=True)
        with col2:
            documento = st.text_input(f"{tipo_doc}")
        obs = st.text_area("Observação", height=100)
        img = st.file_uploader("Imagem", type=["png", "jpg", "jpeg", "webp"], key="forn_img")
        col_sub, col_can = st.columns(2)
        with col_sub:
            submitted = st.form_submit_button("✅ Salvar", use_container_width=True)
        with col_can:
            st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
        if submitted:
            if not documento:
                st.error(f"Informe o {tipo_doc}")
                return
            with st.spinner("Salvando solicitação..."):
                img_path = save_upload_file(img) if img else ""
                data = {"tipo": "Fornecedor", "tipo_doc": tipo_doc, "documento": documento, "obs": obs}
                st.session_state.db.create_request(st.session_state.user_id, st.session_state.user_email, "Fornecedor", "Cadastro", hotel_code, hotel_info["name"], hotel_info["group"], None, data, img_path)
                time.sleep(0.5)
            req_id = st.session_state.db.get_user_requests(st.session_state.user_id)[0]['id']
            notify_new_request(st.session_state.user_email, req_id, "Fornecedor", "Cadastro", hotel_info["name"])
            play_notification('new')
            st.success(f"✅ Solicitação #{req_id} efetuada com sucesso!")
            time.sleep(2)
            st.session_state.page = "minhas_solicitacoes"
            st.rerun()


def page_minhas_solicitacoes():
    """Minhas Solicitações"""
    st.markdown("""
    <div class='page-header'>
        <h1>📋 Minhas Solicitações</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Acompanhe todas as suas solicitações</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data Inicial", key="minhas_data_inicio")
    with col2:
        data_fim = st.date_input("Data Final", key="minhas_data_fim")
    
    requests = st.session_state.db.get_user_requests(st.session_state.user_id)
    if not requests:
        st.info("Você ainda não tem solicitações")
        return

    # Detectar respostas novas desde última verificação e notificar com som
    try:
        current_map = {r['id']: r['status'] for r in requests}
        prev_map = st.session_state.get('requests_status_map', {})
        for rid, status in current_map.items():
            if prev_map.get(rid) == 'Pendente' and status == 'Respondido':
                st.info(f"✅ Sua solicitação #{rid} foi respondida")
                play_notification('responded')
        st.session_state['requests_status_map'] = current_map
    except Exception:
        st.session_state['requests_status_map'] = {r['id']: r['status'] for r in requests}
    
    # Filtrar por data
    requests_filtradas = []
    for r in requests:
        data_req = r["created_at"][:10]
        if str(data_inicio) <= data_req <= str(data_fim):
            requests_filtradas.append(r)
    
    if not requests_filtradas:
        st.info("Nenhuma solicitação no período selecionado")
        return
    
    pendentes = [r for r in requests_filtradas if r["status"] == "Pendente"]
    concluidas = [r for r in requests_filtradas if r["status"] == "Respondido"]
    tab1, tab2 = st.tabs([f"⏳ Pendentes ({len(pendentes)})", f"✅ Concluídas ({len(concluidas)})"])

    with tab1:
        if not pendentes:
            st.info("Nenhuma solicitação pendente")
        else:
            data = []
            for r in pendentes:
                data.append({"ID": r["id"], "Categoria": r["category"], "Hotel": f"{r['hotel_code']}", "Tipo": r['subcategory'], "Data": r["created_at"][:10]})
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()
            st.write("**Detalhes:**")
            req_ids = [r["id"] for r in pendentes]
            selected_id = st.selectbox("Selecione", req_ids, format_func=lambda x: f"#{x}", key="pend_select")
            req = st.session_state.db.get_request(selected_id)
            if req:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ID", f"#{req['id']}")
                with col2:
                    st.metric("Status", "⏳ Pendente")
                with col3:
                    st.metric("Data", req['created_at'][:10])
                st.write(json.loads(req["data_json"]))
                if req["image_path"] and os.path.exists(req["image_path"]):
                    st.image(req["image_path"], use_container_width=True)

    with tab2:
        if not concluidas:
            st.info("Nenhuma solicitação concluída")
        else:
            data = []
            for r in concluidas:
                data.append({"ID": r["id"], "Categoria": r["category"], "Hotel": f"{r['hotel_code']}", "Tipo": r['subcategory'], "Data": r["created_at"][:10]})
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()
            st.write("**Detalhes:**")
            req_ids = [r["id"] for r in concluidas]
            selected_id = st.selectbox("Selecione", req_ids, format_func=lambda x: f"#{x}", key="conc_select")
            req = st.session_state.db.get_request(selected_id)
            if req:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ID", f"#{req['id']}")
                with col2:
                    st.metric("Status", "✅ Concluída")
                with col3:
                    st.metric("Data", req['created_at'][:10])
                st.write(json.loads(req["data_json"]))
                if req["image_path"] and os.path.exists(req["image_path"]):
                    st.image(req["image_path"], use_container_width=True)
                st.divider()
                st.write("**Resposta do Administrador:**")
                st.info(f"✅ {req['admin_response']}")


def page_perfil():
    """Editar Perfil"""
    st.markdown("""
    <div class='page-header'>
        <h1>⚙️ Meu Perfil</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Gerenciar informações da sua conta</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("**Informações da Conta**")
    st.text_input("E-mail", value=st.session_state.user_email, disabled=True)
    st.info("E-mail não pode ser alterado")
    st.write("**Segurança**")
    with st.form("form_senha"):
        senha_atual = st.text_input("Senha atual", type="password")
        senha_nova = st.text_input("Nova senha", type="password")
        confirma = st.text_input("Confirmar nova senha", type="password")
        col_sub, col_can = st.columns(2)
        with col_sub:
            submitted = st.form_submit_button("✅ Atualizar Senha", use_container_width=True)
        with col_can:
            st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
        if submitted:
            if not senha_atual or not senha_nova or not confirma:
                st.error("Preencha todos os campos")
                return
            user = st.session_state.db.get_user(st.session_state.user_email)
            if not verify_password(senha_atual, user["salt_hex"], user["hash_hex"]):
                st.error("Senha atual incorreta")
                return
            if senha_nova != confirma:
                st.error("As novas senhas não conferem")
                return
            with st.spinner("Atualizando..."):
                salt_hex, hash_hex = hash_password(senha_nova)
                cur = st.session_state.db.conn.cursor()
                cur.execute("UPDATE users SET salt_hex = ?, hash_hex = ? WHERE email = ?", (salt_hex, hash_hex, st.session_state.user_email))
                st.session_state.db.conn.commit()
                time.sleep(0.5)
            st.success("✅ Senha atualizada com sucesso!")
            time.sleep(2)


def page_admin():
    """Painel Administrativo"""
    if st.session_state.user_role != "admin":
        st.error("Acesso negado")
        return
    st.markdown("""
    <div class='page-header'>
        <h1>👨‍💼 Painel Administrativo</h1>
        <p style='color: #cbd5e1; margin: 8px 0 0 0;'>Gerenciar todas as solicitações do sistema</p>
    </div>
    """, unsafe_allow_html=True)
    requests = st.session_state.db.get_all_requests()
    # Notificação sonora para admin quando nova solicitação chega
    try:
        prev_count = st.session_state.get('admin_last_count', 0)
        if len(requests) > prev_count:
            st.warning("📥 Nova solicitação recebida")
            play_notification('new')
        st.session_state['admin_last_count'] = len(requests)
    except Exception:
        st.session_state['admin_last_count'] = len(requests)
    if not requests:
        st.info("Nenhuma solicitação no sistema")
        return
    st.write("**Filtros**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["Todas", "Pendente", "Respondido"], key="admin_status")
    with col2:
        cat_filter = st.selectbox("Categoria", ["Todas"] + list(set([r["category"] for r in requests])), key="admin_cat")
    with col3:
        data_inicio = st.date_input("Data Inicial", key="admin_data_inicio")
    with col4:
        data_fim = st.date_input("Data Final", key="admin_data_fim")

    filtered = []
    for r in requests:
        if status_filter != "Todas" and r["status"] != status_filter:
            continue
        if cat_filter != "Todas" and r["category"] != cat_filter:
            continue
        data_req = r["created_at"][:10]
        if not (str(data_inicio) <= data_req <= str(data_fim)):
            continue
        filtered.append(r)

    st.write(f"**Total:** {len(filtered)} solicitações")
    st.divider()
    data = []
    for r in filtered:
        data.append({"ID": r["id"], "E-mail": r["user_email"][:20], "Categoria": r["category"], "Hotel": f"{r['hotel_code']}", "Status": "✅" if r["status"] == "Respondido" else "⏳", "Data": r["created_at"][:10]})

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.write("**Responder Solicitação**")

    if filtered:
        req_ids = [r["id"] for r in filtered]
        selected_id = st.selectbox("Selecione", req_ids, format_func=lambda x: f"#{x}", key="admin_select")
        req = st.session_state.db.get_request(selected_id)
        if req:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ID", f"#{req['id']}")
            with col2:
                st.metric("E-mail", req["user_email"][:15])
            with col3:
                st.metric("Status", "✅" if req['status'] == "Respondido" else "⏳")
            st.divider()
            st.write(json.loads(req["data_json"]))
            if req["image_path"] and os.path.exists(req["image_path"]):
                st.image(req["image_path"], use_container_width=True)
            st.divider()
            with st.form("form_resposta"):
                novo_status = st.selectbox("Status", ["Pendente", "Respondido"], key="admin_novo_status", index=0 if req["status"] == "Pendente" else 1)
                resposta = st.text_area("Resposta", value=req["admin_response"] or "", height=100)
                col_sub, col_can = st.columns(2)
                with col_sub:
                    submitted = st.form_submit_button("💾 Salvar", use_container_width=True)
                with col_can:
                    st.form_submit_button("❌ Cancelar", use_container_width=True, disabled=True)
                if submitted:
                    if novo_status == "Respondido" and not resposta.strip():
                        st.error("A resposta é obrigatória")
                        return
                    with st.spinner("Processando resposta..."):
                        time.sleep(0.8)
                        st.session_state.db.update_request(selected_id, novo_status, resposta)
                        # Envia notificação por email ao usuário
                        if novo_status == "Respondido":
                            notify_response(req["user_email"], selected_id, resposta)
                    # Toca som para o admin e informa o usuário
                    play_notification('responded')
                    st.success(f"✅ Resposta salva! Notificado em {now_iso()}")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()


# ============================================================================
# MAIN
# ============================================================================

def main():
    ensure_dirs()
    if not st.session_state.authenticated:
        page_login()
    else:
        render_menu()
        page = st.session_state.page
        if page == "menu":
            page_menu()
        elif page == "itens":
            page_itens()
        elif page == "compras":
            page_compras()
        elif page == "fornecedor":
            page_fornecedor()
        elif page == "minhas_solicitacoes":
            page_minhas_solicitacoes()
        elif page == "perfil":
            page_perfil()
        elif page == "admin":
            page_admin()
        else:
            st.session_state.page = "menu"
            st.rerun()

if __name__ == "__main__":
    main()
