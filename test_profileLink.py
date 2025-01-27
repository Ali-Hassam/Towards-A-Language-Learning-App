import tkinter as tk
import webbrowser  # To open the link in the default web browser


def open_link(event, url):
    # Open the URL when the link is clicked
    webbrowser.open(url)


def create_app():
    root = tk.Tk()
    root.title("Application Info")

    # Create a Text widget for the description with more control
    description_text = (
        "This application was created by John Doe ("
        "attached a link here as well).\n\n"  # Added extra newline for more space
        "As a part of his learning journey to develop useful tools "
        "for the community."
    )

    text_widget = tk.Text(root, wrap="word", font=("Arial", 12), height=6, width=50)
    text_widget.insert(tk.END, description_text)
    text_widget.config(state=tk.DISABLED)  # Make the text non-editable

    # Adjust line spacing (spacing1 is before each line, spacing2 is between lines)
    text_widget.config(spacing1=5, spacing2=5)

    text_widget.pack(pady=20)

    # Create a clickable label for the link on your name, with bold font
    name_label = tk.Label(root, text="From Vienna with Love: John Doe", fg="blue", cursor="hand2",
                          font=("Arial", 14, "bold"))
    name_label.pack(pady=10)

    # Bind the click event for the name label to open your link
    name_label.bind("<Button-1>", lambda event: open_link(event,
                                                          "https://www.yourprofilelink.com"))  # Replace with your actual profile link

    root.mainloop()


# Run the application
create_app()
