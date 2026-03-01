import requests
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN ---
URL_CUEVANA = "https://wv3.cuevana3.eu/"
# Tu Webhook de Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1277489715329372305/-fdm8J523E84DDLvhk1sG_OU7A1rIec27" 

def buscar_estrenos():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(URL_CUEVANA, headers=headers)
        if response.status_code != 200: return
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscamos las últimas 10 películas
        posts = soup.find_all('li', class_='peli', limit=10)
        
        for post in posts:
            titulo = post.find('h2').text.strip()
            link = post.find('a')['href']
            img_tag = post.find('img')
            imagen_url = img_tag['data-src'] if img_tag.has_attr('data-src') else img_tag['src']
            
            # Intentar sacar la sinopsis
            sinopsis = post.find('div', class_='resumen')
            texto_sinopsis = sinopsis.text.strip() if sinopsis else "Sin sinopsis disponible."

            embed = {
                "title": titulo,
                "url": link,
                "description": texto_sinopsis,
                "color": 15158332,
                "image": {"url": imagen_url}
            }
            requests.post(WEBHOOK_URL, json={"embeds": [embed]})
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    buscar_estrenos()