import requests
from bs4 import BeautifulSoup
import os

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
    # Forzamos encoding UTF-8 para evitar el error de tus fotos
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        historial = f.read().splitlines()

    juegos_actuales = buscar_juegos()
    
    with open(HISTORIAL_FILE, 'a', encoding='utf-8') as f:
        for juego in juegos_actuales:
            if juego not in historial:
                data = {"content": f"🎮 **¡JUEGO GRATIS!** \n> {juego}"}
                requests.post(WEBHOOK_URL, json=data)
                f.write(juego + '\n')