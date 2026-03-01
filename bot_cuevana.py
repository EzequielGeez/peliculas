import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477655678259822757/PXn84JTNa-Wwiu1smpuBDNifgQeaD8dvbxN6Nh1YCOd8Qeg_xDNUUwd49gSjC_0DMex0"
HISTORIAL_FILE = 'historial.txt'

def buscar_pelis():
    url = "https://cuevana.biz/" 
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('h2')[:5] 
        return [item.text.strip() for item in items]
    except:
        return []

if __name__ == "__main__":
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
        historial = f.read().splitlines()

    pelis = buscar_pelis()
    with open(HISTORIAL_FILE, 'a', encoding='utf-8') as f:
        for p in pelis:
            if p not in historial:
                requests.post(WEBHOOK_URL, json={"content": f"🎬 **NUEVA PELI:** {p}"})
                f.write(p + '\n')