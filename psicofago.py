import cv2
import numpy as np
import os
import sys
import time
import subprocess
from shutil import get_terminal_size


RESOLUTION_SETTINGS = {
    'auto': None,           
    'full': None,           
    'hd': (80, 24),        
    'wide': (120, 30),     
    'large': (160, 40),    
    'custom': None         
}


SELECTED_RESOLUTION = 'auto' 


CUSTOM_WIDTH = 100
CUSTOM_HEIGHT = 30


QUALITY_SETTINGS = {
    'low': 1,    
    'medium': 2,   
    'high': 3      
}
SELECTED_QUALITY = 'medium' 

def get_console_size():
    """Obtém o tamanho exato da área de trabalho do console"""
    try:
        if os.name == 'nt': 
            import ctypes
            from ctypes import wintypes
            
            class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes._COORD),
                    ("dwCursorPosition", wintypes._COORD),
                    ("wAttributes", wintypes.WORD),
                    ("srWindow", wintypes.SMALL_RECT),
                    ("dwMaximumWindowSize", wintypes._COORD),
                ]
            
            kernel32 = ctypes.windll.kernel32
            stdout_handle = kernel32.GetStdHandle(-11)
            
            csbi = CONSOLE_SCREEN_BUFFER_INFO()
            if kernel32.GetConsoleScreenBufferInfo(stdout_handle, ctypes.byref(csbi)):
                width = csbi.srWindow.Right - csbi.srWindow.Left + 1
                height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1
                return width, height
    except:
        pass
    
    size = get_terminal_size()
    return size.columns, size.lines

def get_target_resolution():
    """Obtém a resolução alvo baseada na configuração"""
    global SELECTED_RESOLUTION, CUSTOM_WIDTH, CUSTOM_HEIGHT
    
    if SELECTED_RESOLUTION == 'auto':
        return get_console_size()
    elif SELECTED_RESOLUTION == 'full':
        maximize_terminal()
        time.sleep(0.3)
        return get_console_size()
    elif SELECTED_RESOLUTION == 'hd':
        return RESOLUTION_SETTINGS['hd']
    elif SELECTED_RESOLUTION == 'wide':
        return RESOLUTION_SETTINGS['wide']
    elif SELECTED_RESOLUTION == 'large':
        return RESOLUTION_SETTINGS['large']
    elif SELECTED_RESOLUTION == 'custom':
        return (CUSTOM_WIDTH, CUSTOM_HEIGHT)
    else:
        return get_console_size()

def maximize_terminal():
    """Maximiza a janela do terminal no Windows"""
    if os.name == 'nt':
        try:
            import ctypes
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 3)  
        except:
            pass

def resize_frame(frame, target_width, target_height):
    """Redimensiona o frame com diferentes níveis de qualidade"""
    frame_height, frame_width = frame.shape[:2]
    aspect_ratio = frame_width / frame_height
    

    if SELECTED_QUALITY == 'low':
        interpolation = cv2.INTER_NEAREST  
    elif SELECTED_QUALITY == 'medium':
        interpolation = cv2.INTER_LINEAR  
    else:
        interpolation = cv2.INTER_CUBIC   
    
    
    new_width = target_width
    new_height = int(new_width / aspect_ratio)
    
    if new_height < target_height:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    
   
    resized = cv2.resize(frame, (new_width, new_height), interpolation=interpolation)
    
    
    if resized.shape[0] > target_height:
        resized = resized[:target_height, :]
    if resized.shape[1] > target_width:
        resized = resized[:, :target_width]
    
    return resized

def rgb_to_ansi(r, g, b):
    """Converte RGB para código ANSI de cor verdadeira"""
    return f"\033[38;2;{r};{g};{b}m"

def frame_to_colored_ascii(frame):
    """Converte frame para ASCII usando APENAS o caractere █ com cores reais"""
    ascii_frame = []
    
    for row in frame:
        ascii_row = []
        for pixel in row:
            b, g, r = pixel
            colored_char = f"{rgb_to_ansi(r, g, b)}█\033[0m"
            ascii_row.append(colored_char)
        
        ascii_frame.append(''.join(ascii_row))
    
    return '\n'.join(ascii_frame)

def clear_screen():
    """Limpa completamente a tela do terminal"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def hide_cursor():
    """Esconde o cursor do terminal"""
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

def show_cursor():
    """Mostra o cursor do terminal"""
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

def move_cursor_home():
    """Move o cursor para o início da tela"""
    sys.stdout.write('\033[H')
    sys.stdout.flush()

def set_terminal_title(title):
    """Define o título da janela do terminal"""
    sys.stdout.write(f'\033]0;{title}\007')
    sys.stdout.flush()

def execute_main_py():
    """Executa o arquivo core.py na pasta Util"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        core_path = os.path.join(current_dir, "Util", "core.py")
        
        if os.path.exists(core_path):
            print(f"\nExecutando {core_path}...")
            print("="*50)
            
            if os.name == 'nt': 
                subprocess.run([sys.executable, core_path], check=True)
            else:  # Linux/Mac
                subprocess.run([sys.executable, core_path], check=True)
            
            print("="*50)
            print("core.py finalizado!")
        else:
            print(f"\nAviso: Arquivo {core_path} não encontrado!")
            print("Pressione Enter para continuar...")
            input()
            
    except Exception as e:
        print(f"\nErro ao executar core.py: {e}")
        print("Pressione Enter para continuar...")
        input()

def main():
    video_path = "img/edit.mp4"
    
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo não encontrado em {video_path}")
        print("Certifique-se de que o arquivo existe no caminho especificado.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Erro: Não foi possível abrir o vídeo.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    

    fps = cap.get(cv2.CAP_PROP_FPS)
    
    clear_screen()
    hide_cursor()
    set_terminal_title("")
    
    try:
        frame_count = 0
        start_time = time.time()
        
        while True:
            target_width, target_height = get_target_resolution()
            
            ret, frame = cap.read()
            if not ret:
                clear_screen()
                break
            
            if SELECTED_QUALITY == 'low':
                for _ in range(1):
                    ret = cap.read()
                    if not ret:
                        break
            
            resized_frame = resize_frame(frame, target_width, target_height)
            colored_ascii = frame_to_colored_ascii(resized_frame)
            
            move_cursor_home()
            sys.stdout.write(colored_ascii)
            sys.stdout.flush()
            
            frame_count += 1
            expected_time = frame_count / fps
            actual_time = time.time() - start_time
            if actual_time < expected_time:
                time.sleep(expected_time - actual_time)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nVídeo interrompido!")
    finally:
        show_cursor()
        cap.release()
        print("\nPlayer ASCII finalizado!")

        execute_main_py()
        
        print("\nPrograma encerrado. Pressione Enter para sair...")
        input()

if __name__ == "__main__":
    main()