from deep_translator import PonsTranslator, GoogleTranslator
text = "damm"
pons_meaning = [PonsTranslator(source='de', target='en').translate(text)]
google_meaning =[GoogleTranslator(source='de', target='en').translate(text=text)]

all_meanings =  set(pons_meaning+google_meaning)

for i in all_meanings:
    print (i)





#
# if pons_translation != google_translation:
#     pons_translation = [google_translation, google_translation]
# print( pons_translation)
