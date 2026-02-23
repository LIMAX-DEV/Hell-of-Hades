from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading
from datetime import datetime

# Contador global de requisições
request_count = 0
request_lock = threading.Lock()

class WeakServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global request_count
        
        # Incrementa o contador de requisições
        with request_lock:
            request_count += 1
            current_count = request_count
        
        # Log da requisição
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Requisição #{current_count} recebida de {self.client_address[0]}")
        
        # Simula um servidor lento/sobrecarregado
        time.sleep(0.5)  # Atraso artificial de 500ms
        
        # Envia resposta simples (tela branca)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Página em branco com contador mínimo
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Servidor de Teste</title>
            <style>
                body {{ 
                    background: white; 
                    margin: 0; 
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }}
                #counter {{
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background: #f0f0f0;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div id="counter">Requisições: {current_count}</div>
            <!-- Página em branco -->
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        # Suprime os logs padrão do servidor
        pass

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WeakServer)
    print(f"🚀 Servidor fraco rodando em http://localhost:{port}")
    print(f"📊 Monitorando requisições em tempo real...")
    print(f"⚠️  Pressione Ctrl+C para parar o servidor\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor encerrado.")
        print(f"📊 Total de requisições recebidas: {request_count}")

if __name__ == '__main__':
    run_server()