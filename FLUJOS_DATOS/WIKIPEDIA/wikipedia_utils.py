import wikipedia
import wikipediaapi
import time

# Inicializar Wikipedia API en español con un user agent adecuado
user_agent = 'HacklabLaRaizBot/1.0 (hacklab.laraiz@protonmail.com)'
wikipedia.set_lang("es")
wikipedia.set_user_agent(user_agent)

wiki_wiki = wikipediaapi.Wikipedia(
    language='es',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

def buscar_articulos(palabra_clave, max_articulos=50, offset=0):
    search_results = wikipedia.search(palabra_clave, results=max_articulos)
    return search_results

def obtener_contenido_wikipedia(titulo):
    pagina = wiki_wiki.page(titulo)
    return pagina.text if pagina.exists() else ''
