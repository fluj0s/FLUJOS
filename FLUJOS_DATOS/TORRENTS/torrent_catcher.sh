#!/bin/bash

# URL de la página web que contiene los enlaces de torrents
URL="https://file.wikileaks.org/"

# Directorio donde se guardarán los torrents descargados
TORRENT_DIR="home/sito/PROGRAMACION/FLUJOS_TODO_FLUJOS_DATOS/TORRENTS/"  # Cambia esta ruta al directorio donde quieras guardar los torrents

# Crear el directorio si no existe
mkdir -p "TORRENTS_WIKILEAKS_COMPLETO"

# Descargar la página web
curl -s "$URL" -o /tmp/page.html

# Extraer los enlaces de torrent (supone que los enlaces contienen ".torrent")
grep -oP 'href="\K[^"]+\.torrent' /tmp/page.html > /tmp/torrent_links.txt

# Descargar cada archivo torrent
while IFS= read -r link; do
    # Asegurarse de que el enlace es absoluto
    if [[ $link != http* ]]; then
        link="${URL}${link}"
    fi

    # Descargar el archivo torrent
    aria2c -d "TORRENTS_WIKILEAKS_COMPLETO" "$link"
done < /tmp/torrent_links.txt

# Limpiar archivos temporales
rm /tmp/page.html /tmp/torrent_links.txt

echo "Descarga de torrents completada."
