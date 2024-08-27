import pandas as pd
from pymongo import MongoClient
from obsei.source.pandas_source import PandasSource, PandasSourceConfig
from obsei.analyzer.classification_analyzer import ClassificationAnalyzerConfig, ZeroShotClassificationAnalyzer
from obsei.sink.pandas_sink import PandasSink, PandasSinkConfig

# Configura la fuente
source = PandasSource()
source_config = PandasSourceConfig(
    # Proporciona tu configuración aquí
)

# Configura el analizador
analyzer = ZeroShotClassificationAnalyzer(
    # Proporciona tu configuración aquí
)
analyzer_config = ClassificationAnalyzerConfig(
    # Proporciona tu configuración aquí
)

# Configura el sumidero
sink = PandasSink()
sink_config = PandasSinkConfig(
    # Proporciona tu configuración aquí
)

# Ejecuta el flujo de trabajo
source_response_list = source.lookup(source_config)
analyzer_response_list = analyzer.analyze_input(
    source_response_list=source_response_list,
    analyzer_config=analyzer_config
)
sink_response_list = sink.send_data(analyzer_response_list, sink_config)

# Ahora `sink_response_list` es una lista de DataFrames.
# Puedes concatenarlos en un solo DataFrame si es necesario.
df = pd.concat(sink_response_list)

# Realiza cualquier transformación o limpieza de datos necesaria aquí...

# Finalmente, guarda el DataFrame en MongoDB.
client = MongoClient('mongodb://localhost:27017/')
db = client['nombre_de_tu_base_de_datos']
collection = db['nombre_de_tu_coleccion']
collection.insert_many(df.to_dict('records'))
