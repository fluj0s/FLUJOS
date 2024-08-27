from pandas import DataFrame
from obsei.sink.pandas_sink import PandasSink, PandasSinkConfig

# initialize pandas sink config
sink_config = PandasSinkConfig(
   dataframe=DataFrame()
)

# initialize pandas sink
sink = PandasSink()
