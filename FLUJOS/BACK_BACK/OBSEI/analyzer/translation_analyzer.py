from obsei.analyzer.translation_analyzer import TranslationAnalyzer

# Translator does not need analyzer config
analyzer_config = None

# initialize translator
# For supported models refer https://huggingface.co/models?pipeline_tag=translation
analyzer = TranslationAnalyzer(
   model_name_or_path="Helsinki-NLP/opus-mt-hi-en",
   device = "auto"
)