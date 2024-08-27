import os
import re
import numpy as np
from collections import Counter
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from elasticsearch import Elasticsearch, helpers
import pandas as pd
from datetime import datetime

# Parámetros de configuración
SIMILARITY_THRESHOLD = 0.75
LINEAS_POR_ARCHIVO = 1200000
ELASTICSEARCH_INDEX = 'informacion'
LOG_FILE = 'pipeline_subidas.txt'

# Conexión a Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Temáticas y palabras clave para asignación de temas y subtemas
tematicas = {
    'inteligencia y seguridad': ['seguridad', 'inteligencia', 'espionaje', 'contraterrorismo', 'seguridad nacional'],
    'cambio climático': ['cambio climatico', 'desastres naturales', 'calentamiento global', 'energia renovable', 'contaminacion', 'conservacion'],
    'guerra global': ['conflictos internacionales', 'armas', 'dictaduras', 'alianzas militares', 'terrorismo'],
    'demografía y sociedad': ['migración', 'enfermedad', 'población', 'sociedad', 'sobrepoblación'],
    'economia y corporaciones': ['economia global', 'corporaciones multinacionales', 'comercio internacional', 'organismos financieros', 'desigualdad economica']
}

# Función para registrar log en archivo y terminal
def registrar_log(mensaje):
    print(mensaje)
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()}: {mensaje}\n")

# Función para asignar tema y subtema basado en el nombre del archivo
def asignar_tema_y_subtema(nombre_archivo):
    for tema, palabras_clave in tematicas.items():
        for palabra_clave in palabras_clave:
            if palabra_clave.lower() in nombre_archivo.lower():
                return tema, palabra_clave
    return 'otros', 'general'

# Función para extraer la fecha del nombre del archivo
def extraer_fecha_de_nombre(nombre_archivo):
    try:
        fecha_str = re.search(r'\d{4}-\d{2}-\d{2}', nombre_archivo).group(0)
        return datetime.strptime(fecha_str, '%Y-%m-%d')
    except:
        return None

# Función para contar palabras en un archivo tokenizado
def contar_palabras(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as f:
            palabras = f.read().split()
        return Counter(palabras)
    except Exception as e:
        registrar_log(f"Error al contar palabras en {nombre_archivo}: {e}")
        return Counter()

# Función para comparar dos archivos y calcular el porcentaje de similitud
def comparar_archivos(archivo1, archivo2):
    conteo1 = contar_palabras(archivo1)
    conteo2 = contar_palabras(archivo2)

    palabras_comunes = set(conteo1.keys()) & set(conteo2.keys())
    num_palabras_comunes = sum(min(conteo1[p], conteo2[p]) for p in palabras_comunes)
    num_palabras_totales = sum(conteo1.values()) + sum(conteo2.values())

    porcentaje_similitud = (num_palabras_comunes / num_palabras_totales) * 100
    return porcentaje_similitud

# Función para manejar archivos de comparación y escribir los resultados en partes
def manejar_comparaciones(archivo1, archivo2, output_dir, parte_indice, resultados_guardados):
    try:
        nombre_archivo1 = os.path.basename(archivo1)
        nombre_archivo2 = os.path.basename(archivo2)

        if f"{nombre_archivo1}_{nombre_archivo2}" in resultados_guardados:
            registrar_log(f"Saltando {nombre_archivo1} vs {nombre_archivo2}, ya procesado.")
            return parte_indice

        porcentaje = comparar_archivos(archivo1, archivo2)

        output_file = os.path.join(output_dir, f"parte_{parte_indice}.txt")

        # Crear un nuevo archivo si el actual ha alcanzado el tamaño límite
        if os.path.exists(output_file) and os.stat(output_file).st_size >= LINEAS_POR_ARCHIVO:
            parte_indice += 1
            output_file = os.path.join(output_dir, f"parte_{parte_indice}.txt")

        with open(output_file, 'a') as f_out:
            f_out.write(f"{nombre_archivo1} vs {nombre_archivo2}: {porcentaje:.2f}% de similitud\n")
            f_out.flush()

        resultados_guardados.add(f"{nombre_archivo1}_{nombre_archivo2}")
        registrar_log(f"Comparado {nombre_archivo1} vs {nombre_archivo2}: {porcentaje:.2f}% de similitud")
        return parte_indice
    except Exception as e:
        registrar_log(f"Error al manejar comparación {archivo1} vs {archivo2}: {e}")
        return parte_indice

# Función para cargar el progreso de las comparaciones guardadas
def cargar_resultados_guardados(output_dir):
    resultados_guardados = set()
    parte_indice = 1
    output_file = os.path.join(output_dir, f"parte_{parte_indice}.txt")

    while os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                for linea in f:
                    partes = linea.split(" vs ")
                    if len(partes) > 1:
                        resultados_guardados.add(f"{partes[0].strip()}_{partes[1].split(':')[0].strip()}")
            parte_indice += 1
            output_file = os.path.join(output_dir, f"parte_{parte_indice}.txt")
        except Exception as e:
            registrar_log(f"Error al cargar resultados guardados en {output_file}: {e}")
            break

    return resultados_guardados, parte_indice - 1

# Función para comparar todas las carpetas y manejar la reanudación del procesamiento
def comparar_carpetas(carpeta1, carpeta2, nombre_comparacion):
    try:
        registrar_log(f"Iniciando procesamiento de {nombre_comparacion}...")
        output_dir = os.path.join(os.getcwd(), nombre_comparacion)  # Usar el directorio actual
        os.makedirs(output_dir, exist_ok=True)

        resultados_guardados, parte_indice = cargar_resultados_guardados(output_dir)

        archivos1 = sorted([os.path.join(carpeta1, f) for f in os.listdir(carpeta1) if f.endswith('.txt')])
        archivos2 = sorted([os.path.join(carpeta2, f) for f in os.listdir(carpeta2) if f.endswith('.txt')])

        for archivo1 in tqdm(archivos1, desc=f"Comparando {nombre_comparacion} - Archivos 1"):
            for archivo2 in tqdm(archivos2, desc=f"Comparando {nombre_comparacion} - Archivos 2", leave=False):
                parte_indice = manejar_comparaciones(
                    archivo1,
                    archivo2,
                    output_dir,
                    parte_indice,
                    resultados_guardados
                )
        registrar_log(f"Comparación {nombre_comparacion} completada.")
    except Exception as e:
        registrar_log(f"Error durante el procesamiento de {nombre_comparacion}: {e}")

# Función para preparar el documento antes de subirlo a Elasticsearch
def preparar_documento(ruta_archivo, indice):
    nombre_archivo = os.path.basename(ruta_archivo)
    fecha = extraer_fecha_de_nombre(nombre_archivo)
    tema, subtema = asignar_tema_y_subtema(nombre_archivo)

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    doc = {
        '_index': indice,
        '_source': {
            'contenido': contenido,
            'nombre_archivo': nombre_archivo,
            'fecha': fecha,
            'tema': tema,
            'subtema': subtema,
            'tipo_archivo': 'txt',
        }
    }
    registrar_log(f"Documento preparado: {nombre_archivo} con tema {tema} y subtema {subtema}")
    return doc

# Función para subir archivos a Elasticsearch
def subir_a_elasticsearch(directorio, indice):
    archivos = os.listdir(directorio)
    total_archivos = len(archivos)
    acciones = []

    with tqdm(total=total_archivos, desc=f"Subiendo archivos a {indice}", unit="archivo") as barra_progreso:
        for archivo in archivos:
            ruta_archivo = os.path.join(directorio, archivo)
            if os.path.isdir(ruta_archivo):
                continue  # Saltar directorios
            doc = preparar_documento(ruta_archivo, indice)
            if doc:
                acciones.append(doc)
            barra_progreso.update(1)

    if acciones:
        helpers.bulk(es, acciones)
        registrar_log(f"Archivos subidos a Elasticsearch en el índice: {indice}")

# Función para obtener el tamaño total de la base de datos en Elasticsearch
def obtener_tamano_total_elasticsearch():
    stats = es.indices.stats(index='_all')
    total_in_bytes = stats['_all']['total']['store']['size_in_bytes']
    return total_in_bytes / (1024 * 1024)  # Convertir a MB

# Función principal del pipeline
def main():
    try:
        # Rutas a las carpetas
        carpeta_wikipedia = os.path.join('..', 'WIKIPEDIA', 'articulos_tokenizados')
        carpeta_torrents = os.path.join('..', 'TORRENTS', 'TORRENTS_WIKILEAKS_COMPLETO', 'tokenized')
        carpeta_noticias = os.path.join('..', 'NOTICIAS', 'tokenized')

        # Comparar las carpetas y guardar los resultados
        registrar_log("Comparando textos entre diferentes fuentes...")
        comparar_carpetas(carpeta_wikipedia, carpeta_noticias, 'wikipedia_vs_noticias')
        comparar_carpetas(carpeta_wikipedia, carpeta_torrents, 'wikipedia_vs_torrents')
        comparar_carpetas(carpeta_torrents, carpeta_noticias, 'torrents_vs_noticias')

        # Subir los archivos comparados a Elasticsearch
        subir_a_elasticsearch(os.getcwd(), ELASTICSEARCH_INDEX)

        # Mostrar el tamaño total de Elasticsearch
        tamano_total = obtener_tamano_total_elasticsearch()
        registrar_log(f"Tamaño total de la base de datos en Elasticsearch: {tamano_total:.2f} MB")

    except Exception as e:
        registrar_log(f"Error en la función principal: {e}")

if __name__ == "__main__":
    # Limpiar el archivo de log al inicio
    with open(LOG_FILE, 'w') as log_file:
        log_file.write(f"{datetime.now()}: Iniciando pipeline de procesamiento y subida\n")

    main()
