import pandas as pd
from obsei.source.pandas_source import PandasSource, PandasSourceConfig

# Initialize your Pandas DataFrame from your sources like csv, excel, sql etc
# In following example we are reading csv which have two columns title and text
csv_file = "https://raw.githubusercontent.com/deepset-ai/haystack/master/tutorials/small_generator_dataset.csv"
dataframe = pd.read_csv(csv_file)

# initialize pandas sink config
sink_config = PandasSourceConfig(
   dataframe=dataframe,
   include_columns=["score"],
   text_columns=["name", "degree"],
)

# initialize pandas sink
sink = PandasSource()