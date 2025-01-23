from deep_translator import PonsTranslator, GoogleTranslator
word = "damm"
pons_translation = PonsTranslator(source='de', target='en').translate(word)
google_translation = GoogleTranslator(source='de', target='en').translate(text=word)
if pons_translation != google_translation:
    pons_translation = [google_translation, google_translation]
print( pons_translation)
