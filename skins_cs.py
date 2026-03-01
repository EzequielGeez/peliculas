import requests
from bs4 import BeautifulSoup
import os

# Configuración
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477798883500228870/PDHh7XuQEqdLLY83BuTx85f2IzUeBUWwaui8UJYmdmjkCU8BmOP8Kq4Y9m8zwMzW03N3"
HISTORIAL_FILE = 'historial_skins.txt'

def buscar_fuentes():
    novedades = []
    
    # Fuente 1: GamerPower (Sección CS)
    try:
        r1 = requests.get("https://www.gamerpower.com/giveaways/csgo", timeout=15)
        soup1 = BeautifulSoup(r1.content, 'html.parser')
        items1 = [item.text.strip() for item in soup1.find_all('h3', class_='ga-title')[:3]]
        novedades.extend(items1)
    except: pass

    # Fuente 2: Giveaway.su (Búsqueda de Counter-Strike)
    try:
        r2 = requests.get("https://giveaway.su/giveaways/search?query=counter-strike", timeout=15)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        items2 = [item.text.strip() for item in soup2.find_all('div', class_='title')[:3]]
        novedades.extend(items2)
    except: pass

    # Fuente 3: FreebieTracker (Loot de Juegos)
    try:
        r3 = requests.get("https://freebietracker.com/category/pc-games/", timeout=15)
        soup3 = BeautifulSoup(r3.content, 'html.parser')
        items3 = [item.text.strip() for item in soup3.find_all('h2', class_='entry-title')[:2]]
        # Solo filtramos si mencionan algo de CS o Steam
        for i in items3:
            if "CS" in i or "Steam" in i:
                novedades.append(i)
    except: pass

    return list(set(novedades)) # Elimina duplicados si la misma skin está en dos sitios

def enviar_discord(mensaje):
    payload = {"content": f"🔫 **BOTÍN DETECTADO:**\n> {mensaje}"}
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    # Asegurar que el historial existe con encoding correcto
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            f.write("inicio\n")

    # Leer historial
    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        historial = f.read().splitlines()

    # Buscar en todas las fuentes
    skins_encontradas = buscar_fuentes()
    
    # Enviar novedades
    nuevas_contadas = 0
    with open(HISTORIAL_FILE, 'a', encoding='utf-8') as f:
        for skin in skins_encontradas:
            if skin not in historial:
                enviar_discord(skin)
                f.write(skin + '\n')
                nuevas_contadas += 1
    
    if nuevas_contadas == 0:
        print("Sin novedades por ahora. El bot sigue patrullando.")
    else:
        print(f"Se enviaron {nuevas_contadas} nuevas ofertas.")