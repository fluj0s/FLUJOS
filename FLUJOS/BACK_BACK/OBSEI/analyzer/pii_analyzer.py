from obsei.analyzer.pii_analyzer import PresidioEngineConfig, PresidioModelConfig, \
   PresidioPIIAnalyzer, PresidioPIIAnalyzerConfig

# initialize pii analyzer's config
analyzer_config = PresidioPIIAnalyzerConfig(
   # Whether to return only pii analysis or anonymize text
   analyze_only=False,
   # Whether to return detail information about anonymization decision
   return_decision_process=True
)

# initialize pii analyzer
analyzer = PresidioPIIAnalyzer(
   engine_config=PresidioEngineConfig(
       # spacy and stanza nlp engines are supported
       # For more info refer
       # https://microsoft.github.io/presidio/analyzer/developing_recognizers/#utilize-spacy-or-stanza
       nlp_engine_name="spacy",
       # Update desired spacy model and language
       models=[PresidioModelConfig(model_name="en_core_web_lg", lang_code="en")]
   )
)