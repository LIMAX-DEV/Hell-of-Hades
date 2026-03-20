import os
import sys
import time
import subprocess
import threading
import random
import math
from colorama import init, Fore, Back, Style

init(autoreset=True)


C = {
    "bg":       "\033[48;5;232m",
    "reset":    Style.RESET_ALL,
    "blue":     "\033[38;5;33m",      
    "blue_dim": "\033[38;5;24m",       
    "blue_light": "\033[38;5;39m",     
    "white":    "\033[38;5;255m",
    "gray":     "\033[38;5;240m",
    "dark":     "\033[38;5;236m",
    "bold":     Style.BRIGHT,
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(rel):
    return os.path.join(BASE_DIR, rel)


TOOLS = {
    "01": {"label": "Scanner de vulnerabilidades", "cat": "net",  "path": get_path("Util/программа/Scanner de vulnerabilidades.py")},
    "02": {"label": "WebScanner",                  "cat": "net",  "path": get_path("Util/программа/WebScanner.py")},
    "03": {"label": "URL Scanner",                 "cat": "net",  "path": get_path("Util/программа/URL scanner.py")},
    "04": {"label": "IP Scanner",                  "cat": "net",  "path": get_path("Util/программа/IP scanner.py")},
    "05": {"label": "Scanner de Portas",           "cat": "net",  "path": get_path("Util/программа/Scanner de portas IP.py")},
    "06": {"label": "Ping IP",                     "cat": "net",  "path": get_path("Util/программа/Ping IP.py")},
    

    "07": {"label": "Conta Instagram",             "cat": "osint","path": get_path("Util/программа/Conta Instagram.py")},
    "08": {"label": "Criar Dox",                    "cat": "osint","path": get_path("Util/программа/Criar Dox.py")},
    "09": {"label": "Rastrear Dox",                 "cat": "osint","path": get_path("Util/программа/Rastrear Dox.py")},
    "10": {"label": "Obter Exif de Imagem",         "cat": "osint","path": get_path("Util/программа/Obter Exif de imagem.py")},
    "11": {"label": "Google Dorking",               "cat": "osint","path": get_path("Util/программа/Google Dorking.py")},
    "12": {"label": "Rastreador de usuários",       "cat": "osint","path": get_path("Util/программа/Rastreador de usuários.py")},
    "13": {"label": "Rastrear login",               "cat": "osint","path": get_path("Util/программа/Rastrear login.py")},
    "14": {"label": "Localizar conta",              "cat": "osint","path": get_path("Util/программа/Localizar conta.py")},
    "15": {"label": "Buscar número",                 "cat": "osint","path": get_path("Util/программа/Buscar número.py")},
    "16": {"label": "Buscar IP",                     "cat": "osint","path": get_path("Util/программа/Buscar IP.py")},
    "17": {"label": "Buscar em banco de dados",      "cat": "osint","path": get_path("Util/программа/Buscar em banco de dados.py")},
    "18": {"label": "Dark web links",                 "cat": "osint","path": get_path("Util/программа/Dark web links.py")},
    "19": {"label": "Search in doxbin",               "cat": "osint","path": get_path("Util/DOXBIN/search in doxbin.py")},
    

    "20": {"label": "CCTV",                           "cat": "hack", "path": get_path("Util/CCTV/cctv.py")},
    "21": {"label": "Camphish (Hackear webcam)",      "cat": "hack", "path": get_path("Util/camphish/Hackear webcam.py")},
    "22": {"label": "DDoS (simple)",                   "cat": "hack", "path": get_path("Util/DDOS/DDoS.py")},
    "23": {"label": "Criptografar Hash",               "cat": "util", "path": get_path("Util/программа/Criptografar Hash de senha.py")},
    "24": {"label": "Descriptografar Hash",            "cat": "util", "path": get_path("Util/программа/Descriptografar Hash de senha.py")},
    "25": {"label": "Clonar site",                     "cat": "hack", "path": get_path("Util/программа/Clonar site.py")},
    "26": {"label": "Buscar numero",                    "cat": "osint","path": get_path("Util/программа/Buscar numero.py")},
    
    "30": {"label": "Ransomware Builder",               "cat": "virus","path": get_path("Util/RAMSONWARE/builder.py")},
    "31": {"label": "RAT (Telegram)",                    "cat": "virus","path": get_path("Util/RAT/Rat.py")},
    "32": {"label": "Spyware (Telegram)",                "cat": "virus","path": get_path("Util/SPYWARE/spyware.py")},
    "33": {"label": "Keylogger",                         "cat": "virus","path": get_path("Util/KEYLOGGER/keylogger.py")},
    
    "40": {"label": "Roblox Id Info",                    "cat": "roblox","path": get_path("Util/программа/Roblox-Id-Info.py")},
    "41": {"label": "Roblox Cookie Info",                "cat": "roblox","path": get_path("Util/программа/Roblox-Cookie-Info.py")},
    "42": {"label": "Roblox Cookie Login",               "cat": "roblox","path": get_path("Util/программа/Roblox-Cookie-Login.py")},
    "43": {"label": "Roblox User Info",                   "cat": "roblox","path": get_path("Util/программа/Roblox-User-Info.py")},
    
    "50": {"label": "Discord Bot Invite To Id",          "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Bot-Invite-To-Id.py")},
    "51": {"label": "Discord Bot Server Nuker",          "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Bot-Server-Nuker.py")},
    "52": {"label": "Discord Nitro Generator",           "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Nitro-Generator.py")},
    "53": {"label": "Discord Server Info",               "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Server-Info.py")},
    "54": {"label": "Discord Token Block Friends",       "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Block-Friends.py")},
    "55": {"label": "Discord Token Delete Dm",           "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Delete-Dm.py")},
    "56": {"label": "Discord Token Delete Friends",      "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Delete-Friends.py")},
    "57": {"label": "Discord Token Generator",           "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Generator.py")},
    "58": {"label": "Discord Token House Changer",       "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-House-Changer.py")},
    "59": {"label": "Discord Token Info",                 "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Info.py")},
    "60": {"label": "Discord Token Joiner",               "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Joiner.py")},
    "61": {"label": "Discord Token Language Changer",     "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Language-Changer.py")},
    "62": {"label": "Discord Token Leaver",               "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Leaver.py")},
    "63": {"label": "Discord Token Login",                "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Login.py")},
    "64": {"label": "Discord Token Mass Dm",              "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Mass-Dm.py")},
    "65": {"label": "Discord Token Nuker",                "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Nuker.py")},
    "66": {"label": "Discord Token Server Raid",          "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Server-Raid.py")},
    "67": {"label": "Discord Token Spammer",              "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Spammer.py")},
    "68": {"label": "Discord Token Status Changer",       "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Status-Changer.py")},
    "69": {"label": "Discord Token Theme Changer",        "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-Theme-Changer.py")},
    "70": {"label": "Discord Token To Id And Brute",      "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Token-To-Id-And-Brute.py")},
    "71": {"label": "Discord Webhook Delete",             "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Webhook-Delete.py")},
    "72": {"label": "Discord Webhook Generator",          "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Webhook-Generator.py")},
    "73": {"label": "Discord Webhook Info",               "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Webhook-Info.py")},
    "74": {"label": "Discord Webhook Spammer",            "cat": "disc", "path": get_path("Util/DISCORD/программа/Discord-Webhook-Spammer.py")},
}

CAT_LABELS = {
    "net":    ("NETWORK SCANNER",   C["blue"]),
    "osint":  ("OSINT & DOX",       C["blue_light"]),
    "hack":   ("HACKING TOOLS",     C["blue"]),
    "util":   ("UTILITIES",         C["blue_light"]),
    "virus":  ("MALWARE BUILDER",   C["blue"]),
    "roblox": ("ROBLOX EXPLOITS",   C["blue_light"]),
    "disc":   ("DISCORD TOOLS",     C["blue"]),
}

W = 90  


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def cx(n):
    return C[n]

def write(txt, delay=0.0):
    if delay:
        for ch in txt:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
    else:
        sys.stdout.write(txt)
        sys.stdout.flush()

def hline(char="─", color=None, w=W):
    c = color or C["blue_dim"]
    print(f"{c}{char * w}{C['reset']}")

def box_top(w=W, color=None):
    c = color or C["blue_dim"]
    print(f"{c}╔{'═'*(w-2)}╗{C['reset']}")

def box_bot(w=W, color=None):
    c = color or C["blue_dim"]
    print(f"{c}╚{'═'*(w-2)}╝{C['reset']}")

def box_mid(txt, w=W, color=None, txt_color=None):
    c = color or C["blue_dim"]
    tc = txt_color or C["white"]
    inner = w - 4
    visible = len(strip_ansi(txt))
    pad = inner - visible
    print(f"{c}║{C['reset']} {tc}{txt}{' '*pad}{C['reset']} {c}║{C['reset']}")

def strip_ansi(s):
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


GLITCH_CHARS = "!@#$%^&*░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌"

def glitch_line(text, intensity=0.15):
    out = []
    for ch in text:
        if ch != ' ' and random.random() < intensity:
            out.append(random.choice(GLITCH_CHARS))
        else:
            out.append(ch)
    return ''.join(out)


BANNER_LINES = [
" ██▓███    ██████  ██▓ ▄████▄   ▒█████    █████▒▄▄▄        ▄████  ▒█████  ",
"▓██░  ██▒▒██    ▒ ▓██▒▒██▀ ▀█  ▒██▒  ██▒▓██   ▒▒████▄     ██▒ ▀█▒▒██▒  ██▒",
"▓██░ ██▓▒░ ▓██▄   ▒██▒▒▓█    ▄ ▒██░  ██▒▒████ ░▒██  ▀█▄  ▒██░▄▄▄░▒██░  ██▒",
"▒██▄█▓▒ ▒  ▒   ██▒░██░▒▓▓▄ ▄██▒▒██   ██░░▓█▒  ░░██▄▄▄▄██ ░▓█  ██▓▒██   ██░",
"▒██▒ ░  ░▒██████▒▒░██░▒ ▓███▀ ░░ ████▓▒░░▒█░    ▓█   ▓██▒░▒▓███▀▒░ ████▓▒░",
"▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░▓  ░ ░▒ ▒  ░░ ▒░▒░▒░  ▒ ░    ▒▒   ▓▒█░ ░▒   ▒ ░ ▒░▒░▒░ ",
"░▒ ░     ░ ░▒  ░ ░ ▒ ░  ░  ▒     ░ ▒ ▒░  ░       ▒   ▒▒ ░  ░   ░   ░ ▒ ▒░ ",
"░░       ░  ░  ░   ▒ ░░        ░ ░ ░ ▒   ░ ░     ░   ▒   ░ ░   ░ ░ ░ ░ ▒  ",
"               ░   ░  ░ ░          ░ ░               ░  ░      ░     ░ ░  ",
"                      ░                                                   "
]
def show_banner_animated():
    clr()
    

    for step in range(8):
        clr()
        print()
        intensity = max(0, 0.8 - step * 0.12)
        for i, line in enumerate(BANNER_LINES):
            if step < 6:
                gl = glitch_line(line, intensity)
                print(f"  {C['blue']}{gl}{C['reset']}")
            else:
                print(f"  {C['blue']}{line}{C['reset']}")
        time.sleep(0.06)
    

    clr()
    print()
    for i, line in enumerate(BANNER_LINES):
        write(f"  {C['blue']}")
        for ch in line:
            write(ch)
            time.sleep(0.002)
        write(f"{C['reset']}\n")
    

    print()
    subtitle = ""
    spaces = " " * 28
    sub = f"{spaces}{subtitle}"
    write(f"{C['blue_dim']}")
    for ch in sub:
        write(ch)
        time.sleep(0.01)
    write(f"{C['reset']}\n")
    

    github_text = "github.com/LIMAX-DEV"
    spaces = " " * 30
    sub = f"{spaces}{github_text}"
    write(f"{C['blue_dim']}")
    for ch in sub:
        write(ch)
        time.sleep(0.01)
    write(f"{C['reset']}\n")
    print()
    time.sleep(0.3)


def boot_sequence():
    clr()
    steps = [
        ("Inicializando núcleo do PSICÓFAGO...",     C["blue"]),
        ("Carregando módulos de rede...",            C["blue_light"]),
        ("Verificando dependências...",              C["blue_dim"]),
        ("Configurando ambiente...",                  C["blue"]),
        ("Montando interface...",                      C["blue_light"]),
        ("Sistema pronto.",                            C["white"]),
        ("Carregando módulos ofensivos...",            C["blue"]),
        ("Acessando payloads...",                       C["blue_light"]),
    ]
    print()
    print(f"  {C['blue_dim']}{'─'*60}{C['reset']}")
    for msg, col in steps:
        prefix = f"  {C['gray']}[{C['blue']}  OK  {C['gray']}]{C['reset']} "
        write(prefix)
        write(f"{col}")
        for ch in msg:
            write(ch)
            time.sleep(0.018)
        write(f"{C['reset']}\n")
        time.sleep(0.08)
    print(f"  {C['blue_dim']}{'─'*60}{C['reset']}")
    time.sleep(0.4)


def render_menu(selected=None, filter_cat=None):
    clr()
    show_banner_static()


    cats = {}
    for key, t in TOOLS.items():
        c = t["cat"]
        if filter_cat and c != filter_cat:
            continue
        cats.setdefault(c, []).append((key, t))

    print()
    for cat_key, items in cats.items():
        label, cat_col = CAT_LABELS[cat_key]
        print(f"  {cat_col}{C['bold']}  ┌─ {label} {'─'*(W-len(label)-8)}┐{C['reset']}")
        
        row = []
        for key, t in items:
            lbl  = t["label"]
            hi   = selected == key
            num_col = C["blue_light"] if hi else C["blue_dim"]
            lbl_col = C["white"] if hi else C["blue"]
            bg_hi   = "\033[48;5;17m" if hi else ""
            entry = f"{bg_hi}{num_col}[{key}]{C['reset']}{bg_hi} {lbl_col}{lbl:<35}{C['reset']}"
            row.append(entry)
        
        pairs = [row[i:i+2] for i in range(0, len(row), 2)]
        for pair in pairs:
            line = f"  {C['blue_dim']}  │{C['reset']}  {pair[0]}"
            if len(pair) > 1:
                line += f"   {pair[1]}"
            print(line)
        print(f"  {cat_col}  └{'─'*(W-4)}┘{C['reset']}")
        print()

    print(f"  {C['blue_light']}DIGA FILHO MEU, O QUE QUERES{C['reset']}")
    print()
    write(f"  {C['blue']}> {C['white']}")

def show_banner_static():
    print()
    for i, line in enumerate(BANNER_LINES):
        print(f"  {C['blue']}{line}{C['reset']}")
    subtitle = ""
    spaces = " " * 28
    print(f"{C['blue_dim']}{spaces}{subtitle}{C['reset']}")
    github_text = "github.com/LIMAX-DEV"
    spaces = " " * 30
    print(f"{C['blue_dim']}{spaces}{github_text}{C['reset']}")
    print()

def run_tool(key):
    t = TOOLS.get(key)
    if not t:
        return
    path = t["path"]
    label = t["label"]
    
    clr()
    print()
    hline("═", C["blue"])
    box_mid(f"  >  Iniciando: {label}", txt_color=C["blue_light"])
    hline("═", C["blue"])
    print()
    
    if not os.path.isfile(path):
        print(f"  {C['blue']}✗  Arquivo não encontrado:{C['reset']}")
        print(f"  {C['blue_dim']}{path}{C['reset']}")
        print()
        print(f"  {C['blue_dim']}Pressione ENTER para voltar...{C['reset']}")
        input()
        return
    
    try:
        subprocess.run([sys.executable, path], check=True, cwd=os.path.dirname(path))
    except KeyboardInterrupt:
        print(f"\n  {C['blue']}⚠  Interrompido pelo usuário.{C['reset']}")
    except Exception as e:
        print(f"\n  {C['blue']}✗  Erro: {e}{C['reset']}")
    
    print()
    print(f"  {C['blue_dim']}────────────────────────────────────────{C['reset']}")
    print(f"  {C['blue']}Pressione ENTER para voltar ao menu...{C['reset']}")
    input()


def choose_category():
    clr()
    show_banner_static()
    print(f"  {C['blue']}Escolha uma categoria para filtrar:{C['reset']}\n")
    cat_keys = list(CAT_LABELS.keys())
    for i, k in enumerate(cat_keys, 1):
        label, col = CAT_LABELS[k]
        print(f"    {col}[{i}]{C['reset']} {C['blue']}{label}{C['reset']}")
    print(f"    {C['blue_dim']}[0]{C['reset']} {C['blue']}Todas{C['reset']}")
    print()
    write(f"  {C['blue']}> {C['white']}")
    try:
        ch = input().strip()
        if ch == "0" or not ch:
            return None
        idx = int(ch) - 1
        if 0 <= idx < len(cat_keys):
            return cat_keys[idx]
    except:
        pass
    return None


def main():
    boot_sequence()
    show_banner_animated()
    
    filter_cat = None
    last_sel   = None
    
    while True:
        render_menu(selected=last_sel, filter_cat=filter_cat)
        
        try:
            choice = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
        
        if choice in ("q", "exit", "sair"):
            clr()
            print(f"\n  {C['blue']}Até logo.{C['reset']}\n")
            break
        
        elif choice == "f":
            filter_cat = choose_category()
            last_sel = None
        
        elif choice == "r":
            filter_cat = None
            last_sel = None
        
        elif choice.isdigit() or (len(choice) == 2 and choice[0].isdigit()):
            key = choice.zfill(2)
            if key in TOOLS:
                last_sel = key
                run_tool(key)
            else:
                render_menu(filter_cat=filter_cat)
                print(f"  {C['blue']}✗  Opção '{choice}' não encontrada.{C['reset']}")
                time.sleep(1.2)
        else:
            pass

if __name__ == "__main__":
    main()
