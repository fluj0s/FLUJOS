import os
import re
import time
from transformers import BertTokenizer
from collections import Counter
from tqdm import tqdm

stopwords = [
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con",
    "no", "una", "su", "al", "es", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "fue", "este",
    "ha", "sí", "porque", "esta", "son", "entre", "cuando", "muy", "sin", "sobre", "también", "me",
    "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
    "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué",
    "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada",
    "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis",
    "tú", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosotros", "vosotras", "os", "mío", "mía",
    "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro",
    "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas",
    "estoy", "estás", "está", "estamos", "estáis", "están", "esté", "estés", "estemos", "estéis",
    "estén", "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán", "estaría", "estarías",
    "estaríamos", "estaríais", "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban",
    "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras",
    "estuviéramos", "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuviésemos", "estuvieseis",
    "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad"
]

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    palabras = texto.split()
    palabras_limpias = [palabra for palabra in palabras if palabra not in stopwords]
    return ' '.join(palabras_limpias)

def limpiar_nombre_archivo(nombre):
    nombre = re.sub(r'[\\/*?:"<>|]', "_", nombre)
    return nombre

tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-cased')

def tokenizar_y_guardar(texto, nombre_archivo):
    tokens_ids = tokenizer.encode(
        texto,
        truncation=True,
        max_length=512
    )
    tokens_str = ' '.join(map(str, tokens_ids))
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(tokens_str)
    return tokens_ids

def obtener_info_carpeta(ruta):
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(ruta):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            total_files += 1
    return total_size, total_files

LIMITE_TAMANIO_CARPETA = 100 * 1024 * 1024 * 1024

def TOKENIZER():
    if not os.path.exists('articulos_tokenizados'):
        os.makedirs('articulos_tokenizados')

    archivos = os.listdir('articulos_wikipedia')
    for archivo in tqdm(archivos, desc="Tokenizando artículos", unit="archivo"):
        ruta_archivo = os.path.join('articulos_wikipedia', archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            tokens_ids = tokenizer.encode(contenido, add_special_tokens=False)
            nombre_tokens = os.path.join('articulos_tokenizados', archivo)
            with open(nombre_tokens, 'w', encoding='utf-8') as f_tokens:
                f_tokens.write(' '.join(map(str, tokens_ids)))
    print("Tokenización completada para todos los artículos.")

temas = {
    "inteligencia y seguridad": [
        "inteligencia", "seguridad", "espionaje", "ciberseguridad", "NSA", "FBI", "CIA", "CNI",
        "interpol", "operaciones encubiertas", "guerras proxy", "agencia", "contraterrorismo",
        "criptografía", "vigilancia", "espionaje industrial", "ataques cibernéticos", "hackeo",
        "información clasificada", "agente", "reclutamiento", "amenazas", "infraestructuras críticas",
        "tecnologías de la información", "redes", "criptomonedas", "privacidad", "protección de datos",
        "seguridad nacional", "terrorismo", "extremismo", "análisis de inteligencia", "ciberespionaje",
        "ciberguerra", "ciberdelito", "criptografía", "phishing", "ransomware", "malware", "ingeniería social",
        "ataques DDoS", "defensa cibernética", "vulnerabilidades", "parches de seguridad", "software de seguridad",
        "firewalls", "antivirus", "seguridad en la nube", "seguridad móvil", "protección de identidad",
        "autenticación multifactor", "ciberseguridad empresarial", "ciberseguridad gubernamental", "hacktivismo",
        "forense digital", "resiliencia cibernética", "respuestas a incidentes", "gestión de riesgos", "infraestructura crítica",
        "protección de la privacidad", "cumplimiento de normativas", "regulaciones de seguridad", "marco de seguridad",
        "pruebas de penetración", "evaluaciones de seguridad", "auditorías de seguridad", "educación en ciberseguridad",
        "conciencia en ciberseguridad", "seguridad en redes sociales", "protección de datos personales", "intercambio de información",
        "colaboración internacional", "alianzas de seguridad", "sistemas de control industrial", "criptografía cuántica", "tecnologías emergentes",
        "amenazas persistentes avanzadas", "seguridad de IoT", "infraestructura de clave pública", "normativas de seguridad",
        "seguridad en la cadena de suministro", "seguridad física", "protección de infraestructuras críticas", "seguridad en la gestión de identidades",
        "defensa de la red", "investigación en ciberseguridad", "innovación en seguridad", "seguridad en dispositivos médicos",
        "ciberinteligencia", "estrategias de seguridad", "planes de contingencia", "gestión de crisis", "comunicaciones seguras",
        "análisis de amenazas", "evaluaciones de vulnerabilidades", "monitoreo de seguridad", "seguridad en dispositivos móviles", "normativas internacionales"
    ],
    "guerras": [
        "guerra", "conflicto", "batalla", "militar", "guerra mundial", "guerra civil", "guerra fría",
        "intervención militar", "revolución", "insurgencia", "combate", "fuerzas armadas", "ejército",
        "marina", "fuerza aérea", "infantería", "tanques", "artillería", "misiles", "nuclear", "estrategia",
        "táctica", "frente", "trincheras", "guerrilla", "resistencia", "conquista", "ocupación", "aliados",
        "enemigos", "acuerdo de paz", "alto el fuego", "tratado", "armisticio", "bloqueo", "embargo", "sanciones",
        "misión de paz", "intervención humanitaria", "reconstrucción", "desarme", "democracia", "dictadura",
        "autoritarismo", "nacionalismo", "independencia", "soberanía", "imperialismo", "colonialismo",
        "expansionismo", "hegemonía", "doctrina", "alianza", "coalición", "inteligencia militar", "espionaje",
        "sabotaje", "operaciones especiales", "misión de rescate", "contrainteligencia", "logística", "suministros",
        "comunicaciones", "radar", "sonar", "drones", "ciberguerra", "guerra biológica", "guerra química",
        "propaganda", "desinformación", "guerra psicológica", "reclutamiento", "conscripción", "voluntarios",
        "mercenarios", "contratistas", "veteranos", "prisioneros de guerra", "refugiados", "desplazados",
        "víctimas civiles", "crímenes de guerra", "genocidio", "tribunales militares", "justicia transicional",
        "memoria histórica", "reparaciones", "compensaciones", "resolución de conflictos", "mediación",
        "arbitraje", "observadores internacionales", "derechos humanos", "derecho internacional humanitario",
        "cruz roja", "organizaciones no gubernamentales", "desminado", "reconstrucción postconflicto", "vigilancia",
        "seguridad fronteriza"
    ],
    "corporaciones": [
        "empresa", "negocios", "economía", "finanzas", "multinacionales", "mercado bursátil", "Wall Street",
        "IBEX35", "BlackRock", "Vanguard", "inversiones", "acciones", "bonos", "dividendos", "capital",
        "mercado de valores", "índice", "trading", "brokers", "mercados emergentes", "fusiones", "adquisiciones",
        "venture capital", "capital privado", "startups", "emprendimiento", "empresas familiares", "pymes",
        "conglomerados", "industria", "manufactura", "exportaciones", "importaciones", "comercio internacional",
        "aranceles", "barreras comerciales", "globalización", "competencia", "monopolio", "oligopolio",
        "regulación", "desregulación", "privatización", "nacionalización", "política económica", "recesión",
        "crisis financiera", "depresión económica", "estímulo económico", "plan de rescate", "deuda soberana",
        "deficit", "superávit", "bancos centrales", "reserva federal", "BCE", "inflación", "deflación", "tipos de interés",
        "política monetaria", "liquidez", "crédito", "rating", "calificación crediticia", "riesgo financiero",
        "gestión de riesgos", "auditoría", "contabilidad", "fiscalidad", "impuestos", "evasión fiscal",
        "elusión fiscal", "paraísos fiscales", "transparencia", "gobierno corporativo", "ética empresarial",
        "responsabilidad social corporativa", "sostenibilidad", "desarrollo sostenible", "inversión responsable",
        "filantropía", "emisiones de carbono", "huella ecológica", "energías renovables", "economía circular",
        "reciclaje", "innovación", "tecnología", "transformación digital", "industria 4.0", "big data", "inteligencia artificial",
        "blockchain", "fintech", "e-commerce", "marketing digital", "publicidad", "marca", "branding", "cliente",
        "fidelización", "experiencia del cliente", "servicio al cliente", "logística", "cadena de suministro",
        "gestión de operaciones", "productividad", "eficiencia", "calidad", "mejora continua", "lean manufacturing",
        "six sigma", "gestión del cambio", "liderazgo", "gestión de recursos humanos", "cultura organizacional",
        "diversidad", "inclusión", "equidad", "bienestar", "desarrollo del talento", "formación", "desarrollo profesional"
    ],
    "demografía": [
        "población", "demografía", "estadísticas", "censos", "crecimiento poblacional", "migración", "densidad de población",
        "esperanza de vida", "natalidad", "mortalidad", "fecundidad", "estructura etaria", "pirámide poblacional",
        "envejecimiento", "juventud", "urbanización", "ruralidad", "movimientos migratorios", "emigración", "inmigración",
        "refugiados", "desplazados internos", "asilo", "diaspora", "repatriación", "integración", "segregación",
        "multiculturalidad", "etnicidad", "raza", "lengua", "religión", "educación", "alfabetización", "matrimonio",
        "divorcio", "familia", "hogar", "vivienda", "género", "sexo", "orientación sexual", "identidad de género",
        "discriminación", "igualdad", "equidad", "salud", "mortalidad infantil", "esperanza de vida saludable", "morbosidad",
        "enfermedades", "pandemias", "epidemias", "nutrición", "desnutrición", "sobrepeso", "obesidad", "acceso a servicios",
        "agua potable", "saneamiento", "electricidad", "internet", "telecomunicaciones", "transporte", "movilidad",
        "desigualdad", "pobreza", "exclusión social", "desempleo", "empleo", "subempleo", "economía informal", "remesas",
        "desarrollo humano", "calidad de vida", "bienestar", "índice de desarrollo humano", "pobreza multidimensional",
        "vulnerabilidad", "resiliencia", "adaptación", "políticas públicas", "planificación familiar", "derechos reproductivos",
        "salud sexual", "maternidad", "paternidad", "cuidados", "envejecimiento activo", "retiro", "pensiones", "seguridad social",
        "educación continua", "aprendizaje a lo largo de la vida", "movilidad social", "clase social", "estratificación",
        "desigualdad de ingresos", "equidad de género", "violencia de género", "derechos humanos", "justicia social", "participación ciudadana"
    ],
    "cambio climático": [
        "cambio climático", "calentamiento global", "medio ambiente", "sostenibilidad", "energías renovables", "deforestación",
        "emisiones de carbono", "huella de carbono", "gases de efecto invernadero", "protocolos internacionales", "acuerdo de París",
        "protocolo de Kioto", "energía solar", "energía eólica", "energía hidroeléctrica", "biomasa", "biocombustibles", "eficiencia energética",
        "conservación de la energía", "transición energética", "economía verde", "desarrollo sostenible", "resiliencia climática", "adaptación climática",
        "mitigación climática", "descarbonización", "economía circular", "reciclaje", "gestión de residuos", "reducción de residuos", "contaminación",
        "contaminación del aire", "contaminación del agua", "contaminación del suelo", "calidad del aire", "calidad del agua", "conservación de la biodiversidad",
        "ecosistemas", "especies en peligro de extinción", "áreas protegidas", "conservación de la vida silvestre", "reforestación", "aforestación", "restauración ecológica",
        "agricultura sostenible", "agricultura orgánica", "agricultura regenerativa", "ganadería sostenible", "pesca sostenible", "acuicultura sostenible", "alimentación sostenible",
        "consumo responsable", "producción responsable", "infraestructura verde", "ciudades sostenibles", "urbanismo sostenible", "transporte sostenible", "movilidad sostenible",
        "infraestructura de movilidad", "vehículos eléctricos", "transporte público", "caminabilidad", "ciclismo urbano", "espacios verdes", "parques urbanos", "agua potable",
        "saneamiento", "infraestructura de agua", "gestión del agua", "conservación del agua", "eficiencia hídrica", "infraestructura resiliente", "planificación urbana",
        "vivienda sostenible", "arquitectura sostenible", "materiales sostenibles", "construcción sostenible", "edificios verdes", "certificación LEED", "certificación BREEAM",
        "turismo sostenible", "turismo ecológico", "economía azul", "infraestructura natural", "infraestructura ecológica", "infraestructura climática", "finanzas verdes",
        "inversión sostenible", "bonos verdes", "mercados de carbono", "compensación de carbono", "política climática", "derecho ambiental", "educación ambiental",
        "conciencia ambiental", "activismo ambiental", "movimientos ambientales", "justicia climática", "derechos de la naturaleza", "derechos indígenas", "comunidades locales",
        "participación ciudadana", "colaboración internacional", "alianzas climáticas", "acuerdos multilaterales", "financiación climática", "innovación climática",
        "tecnología climática", "soluciones climáticas", "empresas sostenibles", "emprendimiento verde", "liderazgo climático", "estrategias climáticas", "planes de acción climática"
    ],
    "organizaciones internacionales": [
        "OTAN", "BRICS", "ONU", "Unión Europea", "FMI", "Banco Mundial", "OEA", "OPEP", "organización internacional", "tratados internacionales",
        "diplomacia", "relaciones internacionales", "cooperación internacional", "política exterior", "seguridad internacional", "desarrollo internacional",
        "derechos humanos", "paz y seguridad", "resolución de conflictos", "mediación internacional", "arbitraje internacional", "misiones de paz", "asistencia humanitaria",
        "ayuda al desarrollo", "crisis humanitarias", "desplazamiento forzado", "refugiados", "migración internacional", "asilo político", "comercio internacional",
        "comercio multilateral", "libre comercio", "acuerdos comerciales", "aranceles", "barreras comerciales", "propiedad intelectual", "derechos de autor",
        "patentes", "marcas registradas", "innovación", "tecnología", "transferencia de tecnología", "ciencia y tecnología", "investigación y desarrollo",
        "educación internacional", "intercambio educativo", "becas internacionales", "cooperación educativa", "cultura internacional", "intercambio cultural",
        "diversidad cultural", "patrimonio cultural", "protección del patrimonio", "conservación cultural", "turismo internacional", "movilidad internacional",
        "transporte internacional", "infraestructura global", "infraestructura de transporte", "energía internacional", "seguridad energética", "transición energética",
        "energías renovables", "cambio climático", "desarrollo sostenible", "economía circular", "gestión de residuos", "conservación ambiental", "protección de la biodiversidad",
        "gestión del agua", "derechos de agua", "infraestructura hídrica", "salud global", "seguridad sanitaria", "pandemias", "epidemias", "enfermedades infecciosas",
        "vacunas", "acceso a medicamentos", "cobertura sanitaria universal", "derechos de salud", "equidad sanitaria", "financiación de la salud", "gobernanza sanitaria",
        "derechos de las mujeres", "equidad de género", "empoderamiento de las mujeres", "participación política de las mujeres", "derechos de los niños",
        "protección infantil", "educación infantil", "trabajo infantil", "violencia contra los niños", "derechos de los indígenas", "autonomía indígena",
        "cultura indígena", "protección de los pueblos indígenas", "derechos de los discapacitados", "inclusión de los discapacitados", "accesibilidad",
        "derechos de los ancianos", "envejecimiento activo", "seguridad social", "protección social", "pobreza", "desigualdad", "desarrollo económico",
        "inclusión financiera", "banca internacional", "finanzas internacionales", "mercados financieros", "regulación financiera", "corrupción",
        "transparencia", "gobernanza", "estado de derecho", "justicia internacional", "cortes internacionales", "tribunales internacionales", "crímenes de guerra",
        "crímenes contra la humanidad", "genocidio", "derecho internacional", "derecho humanitario", "derecho ambiental", "derecho del mar", "derecho comercial",
        "derecho penal internacional", "derecho de los refugiados", "derecho de asilo", "derecho de los derechos humanos", "derecho de los tratados",
        "derecho de las organizaciones internacionales", "diplomacia preventiva", "diplomacia económica", "diplomacia cultural", "diplomacia científica",
        "diplomacia de la salud", "diplomacia deportiva", "diplomacia digital", "diplomacia pública", "diplomacia parlamentaria", "diplomacia de la paz",
        "diplomacia de la seguridad", "diplomacia de la energía", "diplomacia de la defensa", "diplomacia de la información", "diplomacia de la educación",
        "diplomacia de la cultura", "diplomacia de la tecnología", "diplomacia de la ciencia", "diplomacia de la innovación", "diplomacia de la justicia",
        "diplomacia de los derechos humanos", "diplomacia de los tratados", "diplomacia de las organizaciones internacionales", "diplomacia de la ONU",
        "diplomacia de la OTAN", "diplomacia de la Unión Europea", "diplomacia del BRICS", "diplomacia del FMI", "diplomacia del Banco Mundial",
        "diplomacia de la OEA", "diplomacia de la OPEP", "diplomacia de la OMS", "diplomacia de la UNICEF", "diplomacia de la UNESCO"
    ],
    "gobiernos autoritarios": [
        "dictadura", "autoritario", "represión política", "censura", "control estatal", "violaciones de derechos humanos",
        "tortura", "detención arbitraria", "desaparición forzada", "prisioneros políticos", "exilio", "disidencia",
        "oposición política", "elecciones fraudulentas", "manipulación electoral", "medios de comunicación controlados",
        "propaganda", "desinformación", "vigilancia masiva", "interceptación de comunicaciones", "control de internet",
        "bloqueo de sitios web", "restricción de redes sociales", "censura de prensa", "revisionismo histórico",
        "culto a la personalidad", "golpes de estado", "estados policiales", "corrupción", "nepotismo", "clientelismo",
        "impunidad", "violencia política", "represión violenta", "masacres", "genocidio", "persecución de minorías",
        "persecución de disidentes", "persecución de periodistas", "persecución de activistas", "persecución de intelectuales",
        "persecución de académicos", "persecución de estudiantes", "persecución de trabajadores", "persecución de campesinos",
        "persecución de indígenas", "persecución de mujeres", "persecución de niños", "persecución de ancianos",
        "persecución de discapacitados", "persecución de LGBTI", "persecución de opositores políticos"
    ]
}

if not os.path.exists('articulos_wikipedia'):
    os.makedirs('articulos_wikipedia')

num_articulos_descargados = 0
titulos_descargados = set()

for tema, palabras_clave in temas.items():
    for palabra_clave in palabras_clave:
        print(f"Buscando artículos sobre: {palabra_clave}")
        offset = 0
        while True:
            titulos_articulos = buscar_articulos(palabra_clave, max_articulos=50, offset=offset)
            if not titulos_articulos:
                break
            nuevos_articulos = 0
            for titulo in titulos_articulos:
                if titulo not in titulos_descargados:
                    contenido = obtener_contenido_wikipedia(titulo)
                    if contenido:
                        nombre_archivo = os.path.join('articulos_wikipedia', f"{limpiar_nombre_archivo(titulo)}.txt")
                        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                            archivo.write(contenido)
                        titulos_descargados.add(titulo)
                        num_articulos_descargados += 1
                        nuevos_articulos += 1
                        print(f"Descargado: {titulo}")
                        total_size, total_files = obtener_info_carpeta('articulos_wikipedia')
                        print(f"Total de artículos descargados: {total_files}")
                        print(f"Tamaño total de la carpeta: {total_size / (1024 * 1024):.2f} MB")
                        if total_size > LIMITE_TAMANIO_CARPETA:
                            print(f"Se ha alcanzado el límite de tamaño de la carpeta de 100 GB.")
                            TOKENIZER()
                            exit(0)
            if nuevos_articulos == 0:
                break
            offset += 50
            time.sleep(1)

print(f"Total de artículos descargados: {num_articulos_descargados}")
total_size, total_files = obtener_info_carpeta('articulos_wikipedia')
print(f"Tamaño total de la carpeta: {total_size / (1024 * 1024):.2f} MB")

TOKENIZER()

articulos_descargados = os.listdir('articulos_wikipedia')
if len(articulos_descargados) >= 2:
    articulo1 = open(os.path.join('articulos_wikipedia', articulos_descargados[0]), 'r', encoding='utf-8').read()
    articulo2 = open(os.path.join('articulos_wikipedia', articulos_descargados[1]), 'r', encoding='utf-8').read()

    articulo1_limpio = limpiar_texto(articulo1)
    articulo2_limpio = limpiar_texto(articulo2)

    tokens_articulo1 = tokenizar_y_guardar(articulo1_limpio, 'tokens_articulo1.txt')
    tokens_articulo2 = tokenizar_y_guardar(articulo2_limpio, 'tokens_articulo2.txt')

    def contar_palabras(nombre_archivo):
        with open(nombre_archivo, 'r') as f:
            palabras = f.read().split()
        return Counter(palabras)

    conteo_articulo1 = contar_palabras('tokens_articulo1.txt')
    conteo_articulo2 = contar_palabras('tokens_articulo2.txt')

    palabras_comunes = set(conteo_articulo1.keys()) & set(conteo_articulo2.keys())
    num_palabras_comunes = sum(min(conteo_articulo1[p], conteo_articulo2[p]) for p in palabras_comunes)
    num_palabras_totales = sum(conteo_articulo1.values()) + sum(conteo_articulo2.values())

    porcentaje_similitud = (num_palabras_comunes / num_palabras_totales) * 100

    print(f"Porcentaje de similitud entre los dos primeros artículos descargados: {porcentaje_similitud:.2f}%")
else:
    print("No hay suficientes artículos descargados para comparar similitud.")
