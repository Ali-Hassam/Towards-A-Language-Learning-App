
from tkinter import *
  
# Create object 
root = Tk() 
  
# Adjust size 
root.geometry( "200x200" ) 
  
# Dropdown menu options 
options = [ 
    "10", 
    "15", 
    "20", 
    "25"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "10" ) 
  
# Create Dropdown menu 
drop = OptionMenu( root , clicked , *options ) 
drop.pack() 
  
text = clicked.get()
print(text)
# Execute tkinter 
root.mainloop() 
