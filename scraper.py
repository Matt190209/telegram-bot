import requests
from bs4 import BeautifulSoup

# URL del periódico
URL = "https://www.elheraldo.co/"  # Cambia esta URL al del periódico que quieres scrapear

# Función para scrapear noticias
def obtener_noticias():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encuentra las noticias relevantes
        # Este selector CSS depende de la estructura del sitio
        noticias = soup.select('h2 a')  # Selector para titulares con enlaces
        lista_noticias = []

        for noticia in noticias[:5]:  # Obtén solo las 5 primeras
            titulo = noticia.get_text(strip=True)
            enlace = noticia['href']
            if not enlace.startswith('http'):
                enlace = URL + enlace  # Asegurarse de que el enlace sea una URL completa
            
            # Busca descripción y la imagen
            descripcion = noticia.find_next('p').get_text(strip=True) if noticia.find_next('p') else "No hay descripción disponible."
            imagen = noticia.find_previous('img')['src'] if noticia.find_previous('img') else None

            lista_noticias.append({
                'titulo': titulo,
                'enlace': enlace,
                'descripcion': descripcion,
                'imagen': imagen
            })
        
        return lista_noticias
    except Exception as e:
        print(f"Error al obtener noticias: {e}")
        return []

# Test
if __name__ == "__main__":
    noticias = obtener_noticias()
    for noticia in noticias:
        print(f"Título: {noticia['titulo']}")
        print(f"Enlace: {noticia['enlace']}")
        print(f"Descripción: {noticia['descripcion']}")
        print(f"Imagen: {noticia['imagen']}")
        print("-" * 50)