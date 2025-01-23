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
    for token in nlp(word):
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
def words_to_study(noun_filter=None):
    database_file = read("user_inputs.txt")
    gothe_file = read("buildindatabase.txt")
    today = datetime.now().timetuple().tm_yday
    priority_list = []
    normal_list = []
    gothe_list =[]
    for line in database_file:   
        time_value = int(line.split("time:")[1].split(",")[0].strip())
        time_passed = today - time_value
        word_info = line.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("type:")][0]
        if noun_filter == "noun" and word_type == "NOUN":
            if time_passed in {2, 3, 10, 17, 30}:
                priority_list.append(line)
            else:
                normal_list.append(line)
        elif noun_filter is None:
            if time_passed in {2, 3, 10, 17, 30}:
                priority_list.append(line)
            else:
                normal_list.append(line)
    return priority_list, normal_list, gothe_list

# This part is for games. So we will take count from user 
def get_random(count, priority_list, normal_list, gothe_list):
    selected_words = random.sample(priority_list, min(len(priority_list), count))
    # If there aren't enough in the priority list, fill with words from normal list
    remaining_count = count - len(selected_words)
    if remaining_count > 0:
        selected_words += random.sample(normal_list, remaining_count)
    return selected_words

def input_word_and_save():
    input_word = input("Enter the German word that you want to learn: ")
    meaning = input("Enter the meaning of this German word: ")
    last_time = datetime.now().timetuple().tm_yday
    saved_words = get_words()
    word = input_word.lower()
    # For spelling checker we have to give one word so I tried to pars our input and give spellchecker the main word.
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
    
def der_die_das_game():
    print("Welcome to the Der/Die/Das Game!")
    # Ask user for the number of words they want to practice
    count = int(input("How many words do you want to practice in one session? "))
    priority_list = words_to_study("noun")[0]  # Get only priority words
    normal_list = words_to_study("noun")[1]
    total_words = priority_list + normal_list
    while total_words:
        practice_list = get_random(min(count,len(total_words)), priority_list, normal_list)
        print(f"Total words selected for this session: {len(practice_list)}")
        for element in practice_list:
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            time_value = int (word_dict['time'])
            today = datetime.now().timetuple().tm_yday
            time_passed = today - time_value
            word = word_dict['word']
            article = word_dict['gender']
            user_guess = input(f"What is the correct article for '{word}'? (der, die, das): ").lower()
            if user_guess == article:
                print("Correct! Well done.")
                if time_passed in{2, 3, 10, 17, 30}:
                    total_words.remove(element)
                    priority_list.remove(element)
                else:
                    total_words.remove(element)
                    normal_list.remove(element)
            else:
                print(f"Incorrect! The correct article is {article}.")
        cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
        if cont != "y":
            print("Thanks for playing! Practice more to be pro!!")
            break
    else:
        print("You've practiced all available words! Great job.")

def spelling_game():
    print("Welcome to the Spelling Game!")
    count = int(input("How many words do you want to practice in one session? "))
    priority_list = words_to_study()[0] # Get only priority words
    normal_list = words_to_study()[1]  # Get teh rest fo the words
    total_words = priority_list + normal_list
    print(type(total_words))
    while total_words:
        practice_list = get_random(min(count,len(total_words)), priority_list, normal_list)
        print(type(practice_list))
        print(f"Total words selected for this session: {len(practice_list)}")
        for element in practice_list:
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            print(word_dict)
            time_value = int (word_dict['time'])
            today = datetime.now().timetuple().tm_yday
            time_passed = today - time_value
            word = word_dict['word']
            meaning = word_dict['translation']
            user_spelling = input(f"What is the german word which means {meaning} ").lower()
            if word_dict.get('gender'):  # Check if 'gender' exists
                user_spelling = user_spelling.split()
                if len(user_spelling) == 2 and user_spelling[1] == word and user_spelling[0] == word_dict['gender']:
                    print(f"Yesss, {word} is spelled correctly!")
                    if time_passed in {2, 3, 10, 17, 30}:
                        total_words.remove(element)
                        priority_list.remove(element)
                    else:
                        total_words.remove(element)
                        normal_list.remove(element)
                else:
                    if len(user_spelling) < 2:
                        print("Oops, please provide both the article and the word.")
                    else:
                        if user_spelling[0] != word_dict['gender']:
                            print(f"Oops, the correct article should be '{word_dict['gender']}'")
                        if user_spelling[1] != word:
                            print(f"Oops, the correct word should be '{word}'")
            else:
                if user_spelling == word:
                    print(f"Yesss, {word} is spelled correctly!")
                    if time_passed in {2, 3, 10, 17, 30}:
                        total_words.remove(element)
                        priority_list.remove(element)
                    else:
                        total_words.remove(element)
                        normal_list.remove(element)
                else:
                    print(f"Woops, you wrote it wrongly. The correct spelling is '{word}'")
        cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
        if cont != "y":
            print("Thanks for playing! Practice more to be pro!!")
            break
    else:
        print("You've practiced all available words! Great job.")

def meaning_game():
    count = int(input("How many words do you want to practice in one session? "))
    priority_list = words_to_study()[0] # Get only priority words
    normal_list = words_to_study()[1]  # Get teh rest fo the words
    total_words = priority_list + normal_list
    meanings_list = []
    for meanings in read("user_inputs.txt"):
        word_info = meanings.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("translation")][0]
        meanings_list.append(word_type)
    while total_words:
        practice_list = get_random(min(count,len(total_words)), priority_list, normal_list)
        print(f"Total words selected for this session: {len(practice_list)}")
        for element in practice_list:
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            time_value = int (word_dict['time'])
            today = datetime.now().timetuple().tm_yday
            time_passed = today - time_value
            word = word_dict['word']
            meaning = word_dict['translation']
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
                if time_passed in{2, 3, 10, 17, 30}:
                    total_words.remove(element)
                    priority_list.remove(element)
                else:
                    total_words.remove(element)
                    normal_list.remove(element)
            else:
                print(f"Incorrect. The correct translation of '{word}' is '{meaning}'.")
        cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
        if cont != "y":
            print("Thanks for playing! Practice more to be pro!!")
            break
    else:
        print("You've practiced all available words! Great job.")
        
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