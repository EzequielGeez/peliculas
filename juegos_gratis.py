import requests
from bs4 import BeautifulSoup
import os

# Webhook de Juegos Gratis que me pasaste
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477781995089170683/LHcVrnZ2LkWE9IZYDU1TFPmFFfILpwclRviSde5PhVK_Pkrm9TKD0YwQfv5VxJhjWJea"
HISTORIAL_FILE = 'historial_juegos.txt'

def buscar_juegos():
    url = "https://www.gamerpower.com/free-games"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('h3', class_='ga-title')[:5]
        return [item.text.strip() for item in items]
    except:
        return []

if __name__ == "__main__":
    # Si el archivo no existe, lo creamos con el formato correcto (UTF-8)
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            f.write("inicio\n")

    # Leemos el historial usando UTF-8 para evitar errores rojos
    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        historial = f.read().splitlines()

    juegos_actuales = buscar_juegos()
    
    with open(HISTORIAL_FILE, 'a', encoding='utf-8') as f:
        for juego in juegos_actuales:
            if juego not in historial:
                payload = {"content": f"🎮 **¡NUEVO JUEGO GRATIS!**\n> {juego}"}
                requests.post(WEBHOOK_URL, json=payload)
                f.write(juego + '\n')