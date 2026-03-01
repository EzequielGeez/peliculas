import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477798883500228870/PDHh7XuQEqdLLY83BuTx85f2IzUeBUWwaui8UJYmdmjkCU8BmOP8Kq4Y9m8zwMzW03N3"
HISTORIAL_FILE = 'historial_skins.txt'

def buscar_skins_reales():
    # Usamos una fuente que siempre tenga algo para probar
    url = "https://www.gamerpower.com/giveaways/csgo" 
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('h3', class_='ga-title')[:3]
        if not items:
            # Si no hay sorteos de CS, buscamos generales para que el canal no muera
            items = soup.find_all('h3', class_='ga-title')[:1]
        return [{"id": item.text.strip(), "nombre": item.text.strip()} for item in items]
    except:
        return []

def enviar_discord(mensaje):
    data = {"content": f"🔫 **BOT DE SKINS:** {mensaje}"}
    requests.post(WEBHOOK_URL, json=data)

if __name__ == "__main__":
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w') as f: f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r') as f:
        historial = f.read().splitlines()

    nuevas = buscar_skins_reales()
    
    with open(HISTORIAL_FILE, 'a') as f:
        for s in nuevas:
            if s['id'] not in historial:
                enviar_discord(s['nombre'])
                f.write(s['id'] + '\n')