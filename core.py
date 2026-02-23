import os
import sys
import time
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)


WHITE = Fore.WHITE + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
RESET = Style.RESET_ALL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(rel_path):
    """Transforma um caminho relativo em absoluto baseado na pasta do script"""
    return os.path.join(BASE_DIR, rel_path)

EXECUTAVEIS = {
    "01": get_path("Util/программа/Scanner de vulnerabilidades.py"),
    "02": get_path("Util/программа/WebScanner.py"),
    "03": get_path("Util/программа/URL scanner.py"),
    "04": get_path("Util/программа/IP scanner.py"),
    "05": get_path("Util/программа/Scanner de portas IP.py"),
    "06": get_path("Util/программа/Ping IP.py"),
    "07": get_path("Util/программа/Conta Instagram.py"),
    "08": get_path("Util/программа/Criar Dox.py"),
    "09": get_path("Util/программа/Rastrear Dox.py"),
    "10": get_path("Util/программа/Obter Exif de imagem.py"),
    "11": get_path("Util/программа/Google Dorking.py"),
    "12": get_path("Util/программа/Rastreador de usuários.py"),
    "13": get_path("Util/программа/Rastrear login.py"),
    "14": get_path("Util/программа/Localizar conta.py"),
    "15": get_path("Util/программа/Buscar número.py"),
    "16": get_path("Util/программа/Buscar IP.py"),
    "17": get_path("Util/программа/Buscar em banco de dados.py"),
    "18": get_path("Util/программа/Dark web links.py"),
    "19": get_path("Util/DOXBIN/search in doxbin.py"),

    "20": get_path("Util/CCTV/cctv.py"),
    "21": get_path("Util/camphish/Hackear webcam.py"),
    "22": get_path("Util/DDOS/DDoS.py"),
    "23": get_path("Util/программа/Criptografar Hash de senha.py"),
    "24": get_path("Util/программа/Descriptografar Hash de senha.py"),
    "25": get_path("Util/программа/Clonar site.py"),
    "26": get_path("Util/программа/Buscar numero.py"),
    "27": get_path(""),
    "28": get_path(""),
    "29": get_path(""),
    "30": get_path("Util/RAMSONWARE/builder.py"),
    "31": get_path("Util/RAT/Rat.py"),
    "32": get_path("Util/SPYWARE/spyware.py"),
    "33": get_path("Util/KEYLOGGER/keylogger.py"),
    "34": get_path(""),
    "35": get_path(""),
    "36": get_path(""),
    "37": get_path(""),
    "38": get_path(""),
    "39": get_path(""),
    "40": get_path("Util/программа/Roblox-Id-Info.py"),
    "41": get_path("Util/программа/Roblox-Cookie-Info.py"),
    "42": get_path("Util/программа/Roblox-Cookie-Login.py"),
    "43": get_path("Util/программа/Roblox-User-Info.py"),
    "44": get_path(""),
    "45": get_path(""),
    "46": get_path(""),
    "47": get_path(""),
    "48": get_path(""),
    "49": get_path(""),


"50": get_path("Util/DISCORD/программа/Discord-Bot-Invite-To-Id.py"),
"51": get_path("Util/DISCORD/программа/Discord-Bot-Server-Nuker.py"),
"52": get_path("Util/DISCORD/программа/Discord-Nitro-Generator.py"),
"53": get_path("Util/DISCORD/программа/Discord-Server-Info.py"),
"54": get_path("Util/DISCORD/программа/Discord-Token-Block-Friends.py"),
"55": get_path("Util/DISCORD/программа/Discord-Token-Delete-Dm.py"),
"56": get_path("Util/DISCORD/программа/Discord-Token-Delete-Friends.py"),
"57": get_path("Util/DISCORD/программа/Discord-Token-Generator.py"),
"58": get_path("Util/DISCORD/программа/Discord-Token-House-Changer.py"),
"59": get_path("Util/DISCORD/программа/Discord-Token-Info.py"),

"60": get_path("Util/DISCORD/программа/Discord-Token-Joiner.py"),
"61": get_path("Util/DISCORD/программа/Discord-Token-Language-Changer.py"),
"62": get_path("Util/DISCORD/программа/Discord-Token-Leaver.py"),
"63": get_path("Util/DISCORD/программа/Discord-Token-Login.py"),
"64": get_path("Util/DISCORD/программа/Discord-Token-Mass-Dm.py"),
"65": get_path("Util/DISCORD/программа/Discord-Token-Nuker.py"),
"66": get_path("Util/DISCORD/программа/Discord-Token-Server-Raid.py"),
"67": get_path("Util/DISCORD/программа/Discord-Token-Spammer.py"),
"68": get_path("Util/DISCORD/программа/Discord-Token-Status-Changer.py"),
"69": get_path("Util/DISCORD/программа/Discord-Token-Theme-Changer.py"),

"70": get_path("Util/DISCORD/программа/Discord-Token-To-Id-And-Brute.py"),
"71": get_path("Util/DISCORD/программа/Discord-Webhook-Delete.py"),
"72": get_path("Util/DISCORD/программа/Discord-Webhook-Generator.py"),
"73": get_path("Util/DISCORD/программа/Discord-Webhook-Info.py"),
"74": get_path("Util/DISCORD/программа/Discord-Webhook-Spammer.py")
}

option_next_txt = f"{WHITE}[N] NEXT{RESET}"
option_back_txt = f"{WHITE}[B] BACK{RESET}"

option_01_txt = f"{BLUE}[01]{WHITE} Scanner vuln      "
option_02_txt = f"{BLUE}[02]{WHITE} WebScanner        "
option_03_txt = f"{BLUE}[03]{WHITE} URL scanner       "
option_04_txt = f"{BLUE}[04]{WHITE} IP scanner        "
option_05_txt = f"{BLUE}[05]{WHITE} Scanner de portas "
option_06_txt = f"{BLUE}[06]{WHITE} Ping IP           "
option_07_txt = f"{BLUE}[07]{WHITE} Conta Instagram   "
option_08_txt = f"{BLUE}[08]{WHITE} Criar Dox         "
option_09_txt = f"{BLUE}[09]{WHITE} Rastrear Dox      "
option_10_txt = f"{BLUE}[10]{WHITE} Obter Exif        "
option_11_txt = f"{BLUE}[11]{WHITE} Google Dorking    "
option_12_txt = f"{BLUE}[12]{WHITE} Rastreador users  "
option_13_txt = f"{BLUE}[13]{WHITE} Rastrear login    "
option_14_txt = f"{BLUE}[14]{WHITE} Localizar conta   "
option_15_txt = f"{BLUE}[15]{WHITE} Buscar número     "
option_16_txt = f"{BLUE}[16]{WHITE} Buscar IP         "
option_17_txt = f"{BLUE}[17]{WHITE} Buscar DB         "
option_18_txt = f"{BLUE}[18]{WHITE} Dark web links    "
option_19_txt = f"{BLUE}[19]{WHITE} search in doxbin  "
option_20_txt = f"{BLUE}[20]{WHITE} CCTV     "
option_21_txt = f"{BLUE}[21]{WHITE} camphish (website)"
option_22_txt = f"{BLUE}[22]{WHITE} DDoS (simple)   "
option_23_txt = f"{BLUE}[23]{WHITE} Criptografar Hash de senha "
option_24_txt = f"{BLUE}[24]{WHITE} Descriptografar Hash de senha "
option_25_txt = f"{BLUE}[25]{WHITE} Clonar site    "
option_26_txt = f"{BLUE}[26]{WHITE} Buscar numero       "

menu1 = f"""
 ┌─────────────────────────────────────────────────────────────────────────────────────────────{option_next_txt}─┐
 │         ┌─────────────────┐                        ┌───────┐                         ┌───────────┐   │
 └─┬───────┤ scanner and DOX ├─────────┬──────────────┤ Osint ├──────────────┬──────────┤ Utilities ├───┘
   │       └─────────────────┘         │              └───────┘              │          └───────────┘
   ├─ {option_01_txt}          ├─ {option_10_txt}            ├─ {option_20_txt}
   ├─ {option_02_txt}          ├─ {option_11_txt}            ├─ {option_21_txt}
   ├─ {option_03_txt}          ├─ {option_12_txt}            ├─ {option_22_txt}
   ├─ {option_04_txt}          ├─ {option_13_txt}            ├─ {option_23_txt}
   ├─ {option_05_txt}          ├─ {option_14_txt}            ├─ {option_24_txt}
   ├─ {option_06_txt}          ├─ {option_15_txt}            ├─ {option_25_txt}
   ├─ {option_07_txt}          ├─ {option_16_txt}            └─ {option_26_txt}
   ├─ {option_08_txt}          ├─ {option_17_txt}
   └─ {option_09_txt}          ├─ {option_18_txt}
                                       └─ {option_19_txt}
"""

option_30_txt = f"{BLUE}[30]{WHITE} ransomware       "
option_31_txt = f"{BLUE}[31]{WHITE} RAT telegram      "
option_32_txt = f"{BLUE}[32]{WHITE} spyware telegram  "
option_33_txt = f"{BLUE}[33]{WHITE} keylogger      "
option_34_txt = f"{BLUE}[34]{WHITE} soon      "

option_40_txt = f"{BLUE}[40]{WHITE} Roblox Id Info  "
option_41_txt = f"{BLUE}[41]{WHITE} Roblox Cookie Info  "
option_42_txt = f"{BLUE}[42]{WHITE} Roblox Cookie Login       "
option_43_txt = f"{BLUE}[43]{WHITE} Roblox User Info "
option_44_txt = f"{BLUE}[44]{WHITE} soon "
option_45_txt = f"{BLUE}[45]{WHITE} soon " 
option_46_txt = f"{BLUE}[46]{WHITE} soon "
option_47_txt = f"{BLUE}[47]{WHITE} soon "
option_48_txt = f"{BLUE}[48]{WHITE} soon "
option_49_txt = f"{BLUE}[49]{WHITE} soon "

menu2 = f"""
 ┌─────────────────────────────────────────────────────────────────────────────────────────────────────{option_next_txt}┐
 │        ┌───────────────┐                         ┌─────────────┐                          ┌────────┐{option_back_txt}│
 └─┬──────┤ Virus Builder ├──────────┬──────────────┤Roblox e Util├────────────┬─────────────┤ Roblox ├────────┘
   │      └───────────────┘          │              └─────────────┘            │             └────────┘
   └─ {option_30_txt}         │                                         ├─{option_46_txt}
        ├─ {option_31_txt}   ├─ {option_34_txt}                        ├─{option_47_txt}
        ├─ {option_32_txt}   ├─ {option_40_txt}                  ├─{option_48_txt}          
        └─ {option_33_txt}      ├─ {option_41_txt}              └─{option_49_txt}
                                     ├─ {option_42_txt}                                          
                                     ├─ {option_43_txt} 
                                     ├─ {option_44_txt} 
                                     └─ {option_45_txt}        
                                                                                                                                                                                                     
""" 

option_50_txt = f"{BLUE}[50]{WHITE} Discord Bot Invite To Id      "
option_51_txt = f"{BLUE}[51]{WHITE} Discord Bot Server Nuker      "
option_52_txt = f"{BLUE}[52]{WHITE} Discord Nitro Generator       "
option_53_txt = f"{BLUE}[53]{WHITE} Discord Server Info           "
option_54_txt = f"{BLUE}[54]{WHITE} Discord Token Block Friends   "
option_55_txt = f"{BLUE}[55]{WHITE} Discord Token Delete Dm       "
option_56_txt = f"{BLUE}[56]{WHITE} Discord Token Delete Friends  "
option_57_txt = f"{BLUE}[57]{WHITE} Discord Token Generator       "
option_58_txt = f"{BLUE}[58]{WHITE} Discord Token House Changer   "
option_59_txt = f"{BLUE}[59]{WHITE} Discord Token Info            "

option_60_txt = f"{BLUE}[60]{WHITE} Discord Token Joiner          "
option_61_txt = f"{BLUE}[61]{WHITE} Discord Token Language Changer"
option_62_txt = f"{BLUE}[62]{WHITE} Discord Token Leaver          "
option_63_txt = f"{BLUE}[63]{WHITE} Discord Token Login           "
option_64_txt = f"{BLUE}[64]{WHITE} Discord Token Mass Dm         "
option_65_txt = f"{BLUE}[65]{WHITE} Discord Token Nuker           "
option_66_txt = f"{BLUE}[66]{WHITE} Discord Token Server Raid     "
option_67_txt = f"{BLUE}[67]{WHITE} Discord Token Spammer         "
option_68_txt = f"{BLUE}[68]{WHITE} Discord Token Status Changer  "
option_69_txt = f"{BLUE}[69]{WHITE} Discord Token Theme Changer   "

option_70_txt = f"{BLUE}[70]{WHITE} Discord Token To Id And Brute "
option_71_txt = f"{BLUE}[71]{WHITE} Discord Webhook Delete        "
option_72_txt = f"{BLUE}[72]{WHITE} Discord Webhook Generator     "
option_73_txt = f"{BLUE}[73]{WHITE} Discord Webhook Info          "
option_74_txt = f"{BLUE}[74]{WHITE} Discord Webhook Spammer       "

menu3 = f"""
 ┌─────────────────────────────────────────────────────────────────────────────────────────────{option_back_txt}─┐
 │                                                         ┌─────────┐                                  │
 └─┬───────────────────────────────────────────────────────┤ Discord ├──────────────────────────────────┘
   │                                                       └─────────┘
   ├─ {option_50_txt}├─ {option_60_txt}├─ {option_70_txt}
   ├─ {option_51_txt}├─ {option_61_txt}├─ {option_71_txt}
   ├─ {option_52_txt}├─ {option_62_txt}├─ {option_72_txt}
   ├─ {option_53_txt}├─ {option_63_txt}├─ {option_73_txt}
   ├─ {option_54_txt}├─ {option_64_txt}├─ {option_74_txt}
   ├─ {option_55_txt}├─ {option_65_txt}│
   ├─ {option_56_txt}├─ {option_66_txt}│
   ├─ {option_57_txt}├─ {option_67_txt}│
   ├─ {option_58_txt}├─ {option_68_txt}│
   └─ {option_59_txt}└─ {option_69_txt}│
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_program(programa):
    if programa == "exit":
        print(f"{WHITE}Saindo...{RESET}")
        sys.exit(0)
    
    if os.path.isfile(programa):
        try:
            subprocess.run([sys.executable, programa], check=True, cwd=os.path.dirname(programa))
        except Exception as e:
            print(f"{RED}[!] Erro ao executar: {e}{RESET}")
            time.sleep(3)
    else:
        print(f"{RED}[!] Erro: Arquivo não encontrado em:{RESET}")
        print(f"{WHITE}{programa}{RESET}")
        time.sleep(4)

def show_banner():      
    banner = f"""{BLUE}
    ██╗  ██╗███████╗██╗     ██╗          ██████╗ ███████╗    ██╗  ██╗ █████╗ ██████╗ ███████╗███████╗    
    ██║  ██║██╔════╝██║     ██║         ██╔═══██╗██╔════╝    ██║  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝    
    ███████║█████╗  ██║     ██║         ██║   ██║█████╗      ███████║███████║██║  ██║█████╗  ███████╗    
    ██╔══██║██╔══╝  ██║     ██║         ██║   ██║██╔══╝      ██╔══██║██╔══██║██║  ██║██╔══╝  ╚════██║    
    ██║  ██║███████╗███████╗███████╗    ╚██████╔╝██║         ██║  ██║██║  ██║██████╔╝███████╗███████║    
    ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝     ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝    
                                                                                                                                                                                                                                                                                                                                                                  

                                        https://github.com/LIMAX-DEV
{RESET}"""
    print(banner)

def main():
    current_menu = 1
    
    while True:
        clear_screen()
        show_banner()
        
        if current_menu == 1:
            print(menu1)
            print(f"\n{BLUE}DIGA FILHO MEU, O QUE QUERES{RESET}")
        elif current_menu == 2:
            print(menu2)
            print(f"\n{BLUE}DIGA FILHO MEU, O QUE QUERES{RESET}")
        elif current_menu == 3:
            print(menu3)
            print(f"\n{BLUE}DIGA FILHO MEU, O QUE QUERES{RESET}")
        
        escolha = input(">").strip().lower()
        
        # Navegação entre menus
        if escolha == 'n' and current_menu < 3:
            current_menu += 1
            continue
        elif escolha == 'b' and current_menu > 1:
            current_menu -= 1
            continue
        elif escolha == 'i':
            print(f"\n{WHITE}Informações sobre o sistema OSINT{RESET}")
            print(f"{BLUE}Desenvolvido para análise de informações abertas{RESET}")
            time.sleep(2)
            continue
        elif escolha == 's':
            print(f"\n{WHITE}Site: https://github.com/LIMAX-DEV{RESET}")
            time.sleep(2)
            continue
        
        # Processar escolhas numéricas
        if escolha.isdigit():
            if len(escolha) == 1:
                escolha = f"0{escolha}"
            
            if escolha in EXECUTAVEIS:
                start_program(EXECUTAVEIS[escolha])
            else:
                print(f"{RED}Opção inválida!{RESET}")
                time.sleep(1)
        elif escolha:
            print(f"{RED}Opção inválida!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()