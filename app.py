import sys
from tkinter import *
from src.bot import Bot

# Initialize Color & Font variables
BG_GRAY = "#ABB2B9"
BG_COLOR = "#1D1E2C"
TEXT_COLOR = "#EAECEE"

TITLE_FONT = "Helvetica 20 bold"
FONT = "Helvetica 14"
FONT_HEAD_DESC = "Helvetica 14"

class GUI:
    """
        Initialize tkinter constructor & setup the screen
    """
    def __init__(self):
        self.window = Tk()
        self.setup()

    """
        Run the app and display the screen
    """
    def run(self):
        self.window.mainloop()

    """
        Initialize screen properties & styles of the app window
    """
    def setup(self):
        # Define the app name and screen size
        self.window.title("Psych Bot v1.1")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=750, bg=BG_COLOR)
        
        # Set a head title of the app for the user display, and display it on the top left side of the app screen
        head_label = Label(self.window, bg=BG_COLOR, fg="#FFFFFF",
                           text="Psych Bot", font=TITLE_FONT, pady=10, padx=10, anchor="nw")
        head_label.place(relwidth=1)

        # Add divider between two text labels
        head_div = Label(self.window, width=450, bg=BG_GRAY)
        head_div.place(relwidth=1, rely=0.06, relheight=0.003)

        # Add a "Label" that decribes the purpose of the chatbot
        self.head_descr = Text(self.window, width=20, height=20, bg=BG_COLOR, font=FONT_HEAD_DESC, fg="#FFFFFF",
                                 padx=10, pady=1, takefocus=1)
        self.head_descr.place(relheight=0.25, relwidth=1, rely=0.08)
        self.head_descr.insert(END, "Psych Bot's goal is to give the user psychological advice*. \nThis bot serves as an interactive conversational agent that takes the user's input (a sentence) and outputs an appropriate response. As this assignment does not require Machine Learning implementation, the chatbot may provide a reply that may not relate to the user's prompt.\n\n\n*For legal reasons, neither the bot nor developers are certified to provide medical help.")
        self.head_descr.config(highlightthickness = 0, borderwidth=0, exportselection=0, state="disabled")
        self.head_descr.configure(state=DISABLED)

        # Add a divider between text labels
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.30, relheight=0.003)

        # Create a text widget where all conversation will be displayed
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.60, relwidth=1, rely=0.301)
        self.text_widget.config(highlightthickness = 0, borderwidth=0, exportselection=0, state="disabled")
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Add a scrollbar for the text widget
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # Add a divider between text labels
        bottom_label = Label(self.window, bg=BG_COLOR, height=60)
        bottom_label.place(relwidth=1, rely=0.90)
        
        # Add a textbox where user can enter the text, and bind the "RETURN" key, so it will send the message to the method submitResponse
        self.msg_entry = Entry(bottom_label, bg=BG_COLOR, fg="#FFFFFF", font=FONT)
        self.msg_entry.place(relwidth=0.75, relheight=0.06, rely=0.002, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.submitResponse)

        # Add button that will send a message from the textbox
        send_btn = Button(bottom_label, text="Send", font=FONT, width=20, bg=BG_GRAY,
                             command=lambda: self.submitResponse(None))
        send_btn.place(relx=0.77, rely=0.002, relheight=0.06, relwidth=0.22)

        # On the start, initialize reference variable of the bot by triggering the method
        self.initializeBot()

    """
        Initialize the Bot class and constructor, prompt the user to enter their name
    """
    def initializeBot(self):
        self.bot = Bot("data.json")
        msg2 = f"\n> Bot: Hello, I am Psych-Bot. What is your name?\n\n"
        self.renderMessage(msg2)

    """
        Binded method in the textbox and button, which is triggered by event. The information is send 
        to the method, where all logic and rendering will happen.
    """
    def submitResponse(self, event):
        message = self.msg_entry.get()
        self.addMessage(message)

    """
        Method where GUI class communicates with the Bot class to handle the proper conversation
    """
    def addMessage(self, msg):
        # Validate if the message input is not empty
        if len(msg.strip()) == 0:
            msg2 = f"> Bot: Sorry, what did you say?\n\n"
            self.renderMessage(msg2)
            return

        # Check if username is set in the bot class
        if self.bot.getUserName() == -1:
            # Set the user name, and render the response
            msg1 = f"> Unknown User: {msg}\n\n"
            self.renderMessage(msg1)
            self.renderMessage(self.bot.setUserName(msg))
        else:
            # if no more nodes in dialogue or user printed "quit" - exit the program
            try:
                response = self.bot.getResponse(msg)['text']
            except:
                sys.exit()

            # renders user's message
            msg1 = f"> {self.bot.getUserName()}: {msg}\n\n"
            self.renderMessage(msg1)

            # renders bot's message
            msg2 = f"> Bot: {response}\n\n"
            self.renderMessage(msg2)

        self.msg_entry.delete(0, END)

    """
        Renders the user's and bot's response on the app screen
    """
    def renderMessage(self, response):
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, response)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

if __name__ == "__main__":
    app = GUI()
    app.run()