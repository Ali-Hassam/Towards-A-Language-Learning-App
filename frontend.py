import tkinter as tk
from tkinter import messagebox


# Main app window, which will open exactly at the middle of the screen
# source: https://coderslegacy.com/tkinter-center-window-on-screen/
root = tk.Tk() #The main window
root.title('Language Learning App')

w = 1000  # Width of window
h = 600  # Height of window
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen
# Calculate Start X and Y coordinates for  MainWindow
x = (screen_width / 2) - (w / 2)
y = (screen_height / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # the geometry function takes ('widthxHeight+StartX+StartY')

messagebox.showinfo('Greetings!', 'Hello World', parent=root)

root.mainloop() #The main infinite loop that will keep the main window open until closed by user