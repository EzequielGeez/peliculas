import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477798883500228870/PDHh7XuQEqdLLY83BuTx85f2IzUeBUWwaui8UJYmdmjkCU8BmOP8Kq4Y9m8zwMzW03N3"
HISTORIAL_FILE = 'historial_skins.txt'

def buscar_skins_reales():
    url = "https://www.gamerpower.com/giveaways/csgo" 
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('h3', class_='ga-title')[:3]
        if not items:
            return [{"id": "check_v1", "nombre": "🔍 Bot de Skins activo: Buscando nuevas ofertas..."}]
        return [{"id": item.text.strip(), "nombre": item.text.strip()} for item in items]
    except:
        return []

if __name__ == "__main__":
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        historial = f.read().splitlines()

    nuevas = buscar_skins_reales()
    with open(HISTORIAL_FILE, 'a', encoding='utf-8') as f:
        for s in nuevas:
            if s['id'] not in historial:
                data = {"content": f"🔫 **ALERTA DE CS:** {s['nombre']}"}
                requests.post(WEBHOOK_URL, json=data)
                f.write(s['id'] + '\n')