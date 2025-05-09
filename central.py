import threading
import asyncio
import random
import json
from datetime import datetime

# Simula la llegada de noticias desde diferentes fuentes en distintos formatos (pertenece al primer nodo)
def simulate_news_source(city):   
    async def fetch_news():
        while True:
            await asyncio.sleep(random.uniform(1, 3))  # llegada de noticias con un tiempo random
            if random.random() < 0.2:  # simulo fallos de la fuente
                print(f"[{city}] No se consiguieron datos de la fuente.")
                continue
            format_type = random.choice(["json", "xml", "html"])
            article = generate_article(city, format_type)
            standardized = standardize_article(article, format_type)
            if standardized:
                send_to_central_server(standardized, city)

    asyncio.run(fetch_news())

# Esta función corresponde con el otro nodo que genera y modeliza los articulos (mismo formato)
def generate_article(city, format_type):
    content = {
        "title": f"Noticia de {city}",
        "date": datetime.utcnow().isoformat(),
        "body": f"Contenido generado desde {city}."
    }
    if format_type == "json":
        return json.dumps(content)
    elif format_type == "xml":
        return f"<news><title>{content['title']}</title><date>{content['date']}</date><body>{content['body']}</body></news>"
    elif format_type == "html":
        return f"<html><h1>{content['title']}</h1><p>{content['date']}</p><div>{content['body']}</div></html>"
    return None

# Esta pertenece al mismo nodo que la anterior. Estandariza el artículo recibido en diferentes formatos
def standardize_article(article, format_type):
    try:
        if format_type == "json":
            data = json.loads(article)
            return {
                "title": data["title"],
                "date": data["date"],
                "content": data["body"]
            }
        elif format_type == "xml":
            # Simula la extracción de datos de un XML (uso str)
            def extract(tag): return article.split(f"<{tag}>")[1].split(f"</{tag}>")[0]
            return {
                "title": extract("title"),
                "date": extract("date"),
                "content": extract("body")
            }
        elif format_type == "html":
            def extract(tag_start, tag_end):
                return article.split(tag_start)[1].split(tag_end)[0]
            return {
                "title": extract("<h1>", "</h1>"),
                "date": extract("<p>", "</p>"),
                "content": extract("<div>", "</div>")
            }
    except Exception as e:
        print(f"[Error al estandarizar]: {e}")
        return None

# Esta función simula el envío de datos a un servidor central (para simularlo en el ordenador, los imprimo)
def send_to_central_server(article, city):
    print(f"[{city} → Frankfurt] Artículo recibido:")
    print(json.dumps(article, indent=2))

# La función principal crea las listas de centrales y de hilos
def main():
    locations = ["Madrid", "Londres", "Sao Paulo"]
    threads = []

    # Asigno hilos a cada ciudad
    for city in locations:
        t = threading.Thread(target=simulate_news_source, args=(city,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
