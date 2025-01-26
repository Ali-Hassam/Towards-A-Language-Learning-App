from deep_translator import PonsTranslator
import random

def get_synonyms(word, meaning):
    translator = PonsTranslator(source='de', target='en')
    result = translator.translate(word)
    synonyms = PonsTranslator(source='de', target='en').translate(word, return_all=True)
    if len(synonyms) > 5:
        synonyms = synonyms[:4]
    if meaning not in synonyms:
        if len(synonyms) > 0:
            # Remove the longest synonym if there are more than 5 synonyms
            longest_synonym = max(synonyms, key=len)
            synonyms.remove(longest_synonym)
        synonyms.append(meaning)
    # Shuffle the list of synonyms
    random.shuffle(synonyms)
    # If the list doesn't have exactly 4 synonyms, return the list and False flag
    if len(synonyms) != 4:
        return synonyms, False
    # El return the list and True flag
    return synonyms, True





if __name__ == "__main__":

    #They could be more than one and then change teh Qs as pick the Odds one out

    #generate a random word using
    #random_word = random.choice(word_list)
    random_word = "bcfb"

    syn, tok = get_synonyms('bild', 'post')
    syn1, tok1 = get_synonyms('bis', 'tilt')
    syn2, tok2 = get_synonyms('Absender', 'rent')

    print(f" Pick the Odd One Out :{syn} \n")

    print(f" Pick the Odd One Out :{syn1} \n")

    print(f" Pick the Odd One Out :{syn2} \n")
