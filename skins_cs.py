import requests
import os

WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477798883500228870/PDHh7XuQEqdLLY83BuTx85f2IzUeBUWwaui8UJYmdmjkCU8BmOP8Kq4Y9m8zwMzW03N3"
HISTORIAL_FILE = 'historial_skins.txt'

def enviar_discord(mensaje):
    data = {"content": f"🔫 **ALERTA DE SKIN:** {mensaje}"}
    requests.post(WEBHOOK_URL, json=data)

def buscar_skins():
    # Estas son de prueba, luego le conectamos una web real
    return [
        {"id": "ak47_ice", "nombre": "AK-47 | Ice Coaled (MW) - ¡Oferta!"},
        {"id": "glock_gamma", "nombre": "Glock-18 | Gamma Doppler - ¡Nuevo Sorteo!"}
    ]

if __name__ == "__main__":
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w') as f: f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r') as f:
        historial = f.read().splitlines()

    nuevas = buscar_skins()
    with open(HISTORIAL_FILE, 'a') as f:
        for s in nuevas:
            if s['id'] not in historial:
                enviar_discord(s['nombre'])
                f.write(s['id'] + '\n')