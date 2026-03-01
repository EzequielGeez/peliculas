import requests
import time
import os

# --- CONFIGURACIÓN ---
WEBHOOK_GAMING = "https://ptb.discord.com/api/webhooks/1477781995089170683/LHcVrnZ2LkWE9IZYDU1TFPmFFfILpwclRviSde5PhVK_Pkrm9TKD0YwQfv5VxJhjWJea"

def iniciar():
    # Usamos la API de GamerPower para obtener solo juegos completos gratis
    url = "https://www.gamerpower.com/api/giveaways?type=game"
    
    try:
        print("📡 Iniciando rastreo de juegos gratis...")
        res = requests.get(url, timeout=15)
        if res.status_code != 200: 
            print(f"❌ Error API: {res.status_code}")
            return
        
        juegos = res.json()
        
        # Archivo para recordar qué juegos ya mandamos
        historial_file = "historial_juegos.txt"
        if not os.path.exists(historial_file): 
            open(historial_file, 'w').close()
            
        with open(historial_file, 'r') as f:
            enviados = set(f.read().splitlines())

        nuevos_enviados = 0
        # Revisamos los últimos 5 publicados para ver si hay novedades
        for juego in juegos[:5]:
            id_juego = str(juego['id'])
            
            if id_juego in enviados:
                continue

            # Preparamos el mensaje de Discord
            payload = {
                "username": "Cazador de Ofertas",
                "content": f"🎮 **¡NUEVO JUEGO GRATIS DETECTADO!**\n\n**Título:** {juego['title']}\n**Plataformas:** {juego['platforms']}\n**Link:** {juego['open_giveaway_url']}"
            }

            # Enviamos al Webhook
            r = requests.post(WEBHOOK_GAMING, json=payload)
            
            if r.status_code <= 204:
                print(f"✅ Enviado con éxito: {juego['title']}")
                # Guardamos en la memoria del bot
                with open(historial_file, 'a') as f: 
                    f.write(id_juego + "\n")
                enviados.add(id_juego)
                nuevos_enviados += 1
                time.sleep(5) # Pausa de seguridad

        if nuevos_enviados == 0:
            print("☕ No hay juegos nuevos por ahora.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    iniciar()