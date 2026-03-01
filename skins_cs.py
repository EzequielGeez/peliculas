import requests
import os

# Tu URL de Webhook directo para Skins
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1477798883500228870/PDHh7XuQEqdLLY83BuTx85f2IzUeBUWwaui8UJYmdmjkCU8BmOP8Kq4Y9m8zwMzW03N3"
HISTORIAL_FILE = 'historial_skins.txt'

def enviar_discord(mensaje):
    data = {"content": f"🎯 **NUEVA SKIN DETECTADA:** {mensaje}"}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"Enviado: {mensaje}")
    except Exception as e:
        print(f"Error enviando a Discord: {e}")

def buscar_skins():
    # Aquí simulamos la detección de una skin barata o sorteo
    # Podés cambiar estos nombres para probar si llega el mensaje
    skins_encontradas = [
        {"id": "skin_test_001", "nombre": "AK-47 | Ice Coaled (Minimal Wear) - ¡Precio bajo!"},
        {"id": "skin_test_002", "nombre": "M4A1-S | Emphorosaur-S - ¡Oferta Relámpago!"}
    ]
    return skins_encontradas

if __name__ == "__main__":
    # Verificamos si existe el historial, si no, lo creamos
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'w') as f:
            f.write("inicio\n")

    with open(HISTORIAL_FILE, 'r') as f:
        historial = f.read().splitlines()

    nuevas_skins = buscar_skins()
    
    with open(HISTORIAL_FILE, 'a') as f:
        for skin in nuevas_skins:
            if skin['id'] not in historial:
                enviar_discord(skin['nombre'])
                f.write(skin['id'] + '\n')