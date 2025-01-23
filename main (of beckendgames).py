from spellchecker import SpellChecker
import spacy
from deep_translator import PonsTranslator
from datetime import datetime
import random 
## spech recognaton https://github.com/raphaelradna/german_vocabulary_trainer/blob/main/german_vocabulary_trainer.py


db_file="user_inputs.txt"    
def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()

def save(word):
    data = read(db_file)
    data.append(word)
    with open(db_file, mode="a", encoding="utf-8") as write_file:
        write_file.write(word) 

def get_words():
    database_file = read("user_inputs.txt")
    word_list = []
    for line in database_file:
        line = line.strip()
        if line.startswith("word:"):
            word_list.append(line[6:].strip())
    return word_list

def spelling(word):
    germanspell = SpellChecker(language='de') 
    word = word.lower()
    misspelled = germanspell.unknown([word])
    # Check if the word is spelled correctly
    if word not in misspelled:
        return True
    else:
        candidates = list(germanspell.candidates(word))
        candidates.append("None of them macthes the word I wanted to right")
        return list(candidates)

nlp = spacy.load("de_core_news_sm")
def artikel(word):
    artikels = {
        "masculine": {
            "definite": "der",
            "indefinite": "ein"
        },
        "feminine": {
            "definite": "die",
            "indefinite": "eine"
        },
        "neuter": {
            "definite": "das",
            "indefinite": "ein"
        },
        "plural": {
            "definite": "die",
            "indefinite": None
        }
    }

    doc = nlp(word)
    token = doc[0]
    gender = token.morph.get("Gender")
    gender = gender[0]
    if gender == "Masc":
        return artikels["masculine"]["definite"]
    elif gender == "Fem":
        return artikels["feminine"]["definite"]
    elif gender == "Neut":
        return artikels["neuter"]["definite"]
    else:
        return "Maybe this is not a nounn "
        
# And now we also have the type writer
def get_type(word):
    doc = nlp(word)
    for token in doc:
        return token.pos_

# Translation checker 
def translation(word,meaning):
    meaning = meaning.lower()
    translation = PonsTranslator(source='german', target='english').translate(word, return_all=True)
    trans_list =[]
    trans_list = [i.lower().strip() for i in translation]
    if any(meaning in t for t in trans_list):
        return True
    else:
        return False

# Timer algorithm every 2, 3, 10, 17, 30 later user will make exercises 
def words_to_study(): 
    database_file = read("user_inputs.txt") 
    today = datetime.now().timetuple().tm_yday
    word_list = []
    for line in database_file:
        time_value = int(line.split("time:")[1].split(",")[0].strip())
        time_passed = today - time_value

        if time_passed in {2, 3, 10, 17, 30}:
            word_list.append(line)
    return word_list

# This part is for games. So we will take count from user 
def get_random(count):
    words = words_to_study()
    if len(words) < count:
        return f"Your list is not that much long maybe you could learn some A1 word"
    else:
        return random.sample(words, count)

def input_word_and_save():
    input_word = input("Enter the German word that you want to learn: ")
    meaning = input("Enter the meaning of this German word: ")
    last_time = datetime.now().timetuple().tm_yday
    saved_words = get_words()
    word = input_word.lower()
    # For spelling checker we have to give one word so I tried to pars our input and give spellchecker the main word.
    if len(word.split()) == 1: # if it is just haus, erinnern 
        if word not in saved_words: 
            word_result = spelling(word) # check the spelling 
            if word_result == True:
                word_type = get_type(word)
                start = 0
                if word_type == "NOUN" and word_type: # if it is noun also look for artikel 
                    translation_correct = translation(word, meaning)
                    gender = artikel(word)
                    if translation_correct:
                        new_entry = f"word: {word}, translation: {meaning}, type: {word_type}, gender: {gender}, time: {last_time}, success: {start}\n"
                        save(new_entry)
                        print(f"Yes, the meaning of {word} is {meaning}. Congratssss, {word} has been saved!! Time to work")
                    else:
                        print(f"Translation is not correct. The correct translation of '{word}' is '{PonsTranslator(source='german', target='english').translate(word)}'.")
                else:
                    translation_correct = translation(word, meaning) # if it is not noun then save it without gender
                    if translation_correct:
                        new_entry = f"word: {word}, translation: {meaning}, type: {word_type}, time: {last_time}, success: {start}\n"
                        save(new_entry)
                        print(f"Yes, the meaning of {word} is {meaning}. Congratssss, {word} has been saved!! Time to work")
                    else:
                        print(f"Translation is not correct. The correct translation of '{word}' is '{PonsTranslator(source='german', target='english').translate(word)}'.")
            else:
                print("Woops you wrote wrong. Maybe you meant:")
                for suggestion in  word_result:
                    print(f"- {suggestion}")
        else:
            print(f"{word} is already in the database.")
    else:
        relevant = word.split()
        word_check = [token.text for token in nlp(word) if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'ADV']]
        main_word = word_check[0].lower()
        word_type = get_type(main_word)
        if word_type == "NOUN":
            if main_word not in saved_words:
                truefalse = []
                for wordpart in relevant:
                    truefalse.append(spelling(wordpart)) # check the spelling 
                if all(isinstance(result, bool) and result is True for result in truefalse):
                    word_check = [token.text for token in nlp(word) if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'ADV']]
                    word_type = get_type(main_word)
                    start = 0
                    translation_correct = translation(main_word,meaning)
                    if translation_correct:
                        gender = artikel(relevant[1])
                        if relevant[0] == gender:
                            new_entry = f"word: {main_word}, translation: {meaning}, type: {word_type}, gender: {gender}, time: {last_time}, success: {start} \n"
                            save(new_entry)
                            print(f"Yes, the meaning of {main_word} is {meaning}. Congratulations, {word} has been saved!! Time to work")
                        else:
                            new_entry = f"word: {main_word}, translation: {meaning}, type: {word_type}, gender: {gender}, time: {last_time}, success: {start} \n"
                            save(new_entry)
                            print(f"Woops we must study artikels.{main_word} artikel is not {relevant[0]} But there is no problem we saved the word correctlly")
                    else:
                        print(f"Translation is not correct. The correct translation of '{word}' is '{PonsTranslator(source='german', target='english').translate(main_word)}'.")          
                else:
                    for wordpart in relevant:
                        if spelling(wordpart) is not True:
                            print("Woops, you wrote it wrongly. Maybe you meant:")
                            for suggestion in spelling(wordpart):
                                print(f"- {suggestion}") 
            else:
                print(f"{main_word} is already in the database.")
        else:
            if word not in saved_words:
                truefalse = []
                for wordpart in relevant:
                    truefalse.append(spelling(wordpart)) # check the spelling 
                if all(isinstance(result, bool) and result is True for result in truefalse):
                    word_check = [token.text for token in nlp(word) if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'ADV']]
                    word_type = get_type(word_check[0])
                    start = 0
                    translation_correct = translation(word_check[0],meaning)
                    if translation_correct:
                            new_entry = f"word: {word}, translation: {meaning}, type: {word_type}, time: {last_time}, success: {start} \n"
                            save(new_entry)
                            print(f"Yes, the meaning of {word_check[0]} is {meaning}. Congratulations, {word} has been saved!! Time to work")
                    else:
                        print(f"Translation is not correct. The correct translation of '{word}' is '{PonsTranslator(source='german', target='english').translate(word)}'.")          
                else:
                    for wordpart in relevant:
                        if spelling(wordpart) is not True:
                            print("Woops, you wrote it wrongly. Maybe you meant:")
                            for suggestion in spelling(wordpart):
                                print(f"- {suggestion}") 
            else:
                print(f"{main_word} is already in the database.")

def der_die_das_game():
    print("Welcome to the Der/Die/Das Game!")
    count = int(input("How many words do you want to practice in one session"))
    practice_list = get_random(count)
    for element in practice_list:
        word_info = element.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("type:")][0]
        if word_type == "NOUN":
            noun = [info.split(": ")[1] for info in word_info if info.startswith("word:")][0]
            article = [info.split(": ")[1] for info in word_info if info.startswith("gender:")][0]
            user_guess = input(f"What is the correct article for '{noun}'? (der, die, das): ").lower()
            if user_guess == article:
                print("Correct! Well done.")
            else:
                print(f"Incorrect! The correct article is {article}.")

def spelling_game():
    print("Welcome to the Spelling Game!")
    count = int(input("How many words do you want to practice in one session "))
    practice_list = get_random(count)
    for element in practice_list:
        word_info = element.strip().split(", ")
        meaning = [info.split(": ")[1] for info in word_info if info.startswith("translation:")][0]
        word = [info.split(": ")[1] for info in word_info if info.startswith("word:")][0]
        user_spelling = input(f"What is the german word which means{meaning} ")
        if user_spelling == word:
            print(f"Yesss,{word} is spelled correctly!")
        else:
            print("Woops, you wrote it wrongly.")

def meaning_game():
    print("Welcome to the Meaning Matching Game!")
    count = int(input("How many words do you want to practice in one session? "))
    practice_list = get_random(count)
    meanings_list =[]
    for meanings in read("user_inputs.txt"):
        word_info = meanings.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("translation:")][0]
        meanings_list.append(word_type)
    for element in practice_list:
        word_info = element.strip().split(", ")
        meaning = [info.split(": ")[1] for info in word_info if info.startswith("translation:")][0]
        word = [info.split(": ")[1] for info in word_info if info.startswith("word:")][0]
        print(f"What is the meaning of '{word}'?")
        choices = random.sample(meanings_list, 3)  
        choices.append(meaning) 
        random.shuffle(choices) 
        for idx, option in enumerate(choices, 1):
            print(f"{idx}. {option}", end="  ")
        print() 
        choice = int(input("Choose the correct meaning (1-4): "))  
        if choices[choice - 1] == meaning:  
            print(f"Correct! The meaning of '{word}' is {meaning}.")
        else:
            print(f"Incorrect. The correct translation of '{word}' is '{meaning}'.")
    
if __name__ == "__main__":
    print("What do you want to do?")
    print("1: Input word and save")
    print("2: Der/Die/Das Game")
    print("3: Spelling Game")
    print("4: Meaning Matching Game")
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == "1":
        input_word_and_save()
    elif choice == "2":
        der_die_das_game()
    elif choice == "3":
        spelling_game()
    elif choice == "4":
        meaning_game()
    else:
        print("Invalid choice. Please try again.")