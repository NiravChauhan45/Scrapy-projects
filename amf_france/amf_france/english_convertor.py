from googletrans import Translator

translator = Translator()

# Translate from French to English
text_to_translate = "OPCVM : quand la surperformance du fonds entraine une hausse significative des frais"
translated_text = translator.translate(text_to_translate, src='fr', dest='en')

print(f"Original (French): {text_to_translate}")
print(f"Translated (English): {translated_text.text}")
