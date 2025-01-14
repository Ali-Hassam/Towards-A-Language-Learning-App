import sys
import json
from spellchecker import SpellChecker
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QObject, pyqtSlot

class LanguageApp(QObject):
    def __init__(self):
        QObject.__init__(self)
        # JSON file path for the database
        self.DATABASE_FILE = "database.json"
        self._input_word = ""
        self.germanspell = SpellChecker(language='de') 
    # To get the input from front-end.
    @pyqtSlot(str)
    def set_input_word(self, word):
        self._input_word = word 

    #To check the spelling of imput 
    @pyqtSlot(str, result=bool)
    def spelling(self, word):
        word = word.lower()
        # Check if the word is spelled correctly
        if word in self.germanspell:
            save_format = {"word" : word}
            self.save(save_format)
            print("Word saved successfully.")
            return True
        else:
            print("Word is misspelled.")
            return False
    
    # This function is for saving the input word into the database.
    def save(self, data):
        try:
            with open(self.DATABASE_FILE, mode="r", encoding="utf-8") as read_file:
                existing_data = json.load(read_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.append({"word": data["word"]})
        with open(self.DATABASE_FILE, mode="w", encoding="utf-8") as write_file:
            json.dump(existing_data, write_file, ensure_ascii=False, indent=4)

    def bootUp(self):
        print("Application Booted Up.")

QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./main.qml')
back_end = LanguageApp()
engine.rootContext().setContextProperty("languageApp", back_end)
back_end.bootUp()
sys.exit(app.exec())