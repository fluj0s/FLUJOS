import os

def dividir_archivo_grande(input_file, output_dir, lineas_por_archivo=1000000):
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(input_file, 'r') as f_in:
            archivo_indice = 1
            f_out = open(os.path.join(output_dir, f'parte_{archivo_indice}.txt'), 'w')
            for i, linea in enumerate(f_in):
                if i % lineas_por_archivo == 0 and i > 0:
                    f_out.close()
                    archivo_indice += 1
                    f_out = open(os.path.join(output_dir, f'parte_{archivo_indice}.txt'), 'w')
                f_out.write(linea)
            f_out.close()
        print(f"Archivo '{input_file}' dividido en {archivo_indice} partes en '{output_dir}'")
    except Exception as e:
        print(f"Error al dividir el archivo '{input_file}': {e}")

def procesar_comparaciones():
    # Directorio base
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FLUJOS_DATOS', 'COMPARACIONES')

    # Definir los nombres de las comparaciones y sus carpetas correspondientes
    comparaciones = {
        'wikipedia_vs_noticias': 'wikipedia_vs_noticias.txt',
        'wikipedia_vs_torrents': 'wikipedia_vs_torrents.txt',
        'torrents_vs_noticias': 'torrents_vs_noticias.txt'
    }

    # Configurar las rutas de salida
    for nombre_carpeta, nombre_archivo in comparaciones.items():
        input_file = os.path.join(base_dir, nombre_archivo)
        output_dir = os.path.join(base_dir, nombre_carpeta)

        # Verificar si el archivo de entrada existe
        if os.path.exists(input_file):
            dividir_archivo_grande(input_file, output_dir, lineas_por_archivo=1000000)
        else:
            print(f"El archivo '{input_file}' no existe. No se puede dividir.")

if __name__ == "__main__":
    procesar_comparaciones()
