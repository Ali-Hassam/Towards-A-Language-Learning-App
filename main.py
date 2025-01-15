import json
from spellchecker import SpellChecker
word = input("Enter the German Word that you want to learn")
meaning = input("Enter the meaning of this german word")

# database handler
class database:
    db_file="database.json"    
    def read():
        with open(database.db_file, mode="r", encoding="utf-8") as read_file:
            return json.load(read_file)

    def save(word):
        data = database.read()
        data["user_inputs"].append(word)
        with open(database.db_file, mode="w", encoding="utf-8") as write_file:
            json.dump(data, write_file, ensure_ascii=False, indent=4)

    def get_words():
        database_file = database.read()
        word_list = []
        for i in database_file["user_inputs"]:
            word_list.append(i['word'])
        return word_list

# This class is responsible for input checking
class inputcontroller:
    # So when we put also the artikel somehow it was failing in the spelling checker, so I put this part the pars out input
    def input_parser(word):
        return word.split()

    #This part is for spelling checker
    def spelling(word):
        germanspell = SpellChecker(language='de') 
        word = word.lower()
        # Check if the word is spelled correctly
        if word in germanspell:
            return True
        else:
            candidates = list(germanspell.candidates(word))
            candidates.append("None of them macthes the word I wanted to right")
            if candidates:
                return list(candidates)
            else:  
                return ["Woopss we couldn't find any suggestions"]

saved_words = database.get_words()
db = database.read()
if word not in saved_words:
    result = inputcontroller.spelling(word)
    if  result == True:
        new_entry = {
                    "word": word,
                    "translation": meaning
                    }
        database.save(new_entry)
        print(f"{word} has been saved!")
    else:
        print("Incorrect spelling. Did you mean:")
        for suggestion in result:
            print(f"- {suggestion}")
else:
    print(f"{word} is already in the database.")
