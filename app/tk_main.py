from tkinter import *
from app.utils import helper, cohere_api as cohere
from PIL import ImageTk, Image
from dotenv import load_dotenv
import os

def main():
    ## LOAD CONFIG ENV VARIABLES
    load_dotenv('../config/config.env')

    ### GLOBAL VARIABLES
    DEBUG = True #print app status to console when True
    API_KEY = os.getenv('API_KEY')

    ### FILE DIRECTORY FOR PROMPT ENGINEERING
    TRAINING_DATA_DIR = '../prompt_data/training_data.txt'
    ARTICLE_DIR = '../prompt_data/article.txt'
    HISTORY_DIR = '../prompt_data/history.txt'

    training_data = helper.read_file_lines(TRAINING_DATA_DIR)
    article = helper.read_file_lines(ARTICLE_DIR)
    history = helper.read_file_lines(HISTORY_DIR, lookback=5) #only look back at 5 conversations

    ### GUI DECORATION VARIABLES
    BG_GRAY = "#FFFFFF"
    BG_COLOR = "#FFFFFF"
    TEXT_COLOR = "#203864"
    FONT = "Helvetica 9"
    FONT_BOLD = "Helvetica 13 bold"
    HEADER_LOGO_IMG = "../media/debait_logo.png"

    ### TKINTER APPLICATION
    root = Tk()
    root.title("Debait")
    root.configure(bg=BG_GRAY)

    def send():
        # SEND BUTTON PRESSED
        helper.log("button pressed...", DEBUG)
        send = e.get()

        # USER TEXT ADDED + CLASSIFICATION
        txt.insert(END, "USER:\n")
        helper.log("generating classification...", DEBUG)
        helper.log(send, DEBUG)
        status, error_msg, classification = cohere.classify(send, API_KEY)
        helper.log("status: " + str(status) + error_msg, DEBUG)
        txt.insert(END, "(" + classification + ")\n", 'tag')
        txt.insert(END, "" + send)
        userInput = e.get()

        # PREPARE PROMPT
        helper.log("formatting for input...", DEBUG)
        values_for_prompt = [userInput, "disagree", "short", ""]
        prompt = helper.generate_prompt(training_data=training_data, history=history, article=article, values_for_prompt=values_for_prompt)

        # GENERATING AI RESPONSE USING PROMPT
        helper.log("generating response...", DEBUG)
        status, error_msg, response = cohere.generate(prompt, API_KEY)
        helper.log("status: " + str(status) + error_msg, DEBUG)
        response_prep = response.replace("--", "")
        response_prep = response_prep.strip()
        helper.log(response_prep, DEBUG)
        helper.log("generating classification...", DEBUG)

        # DISPLAY GENERATED AI REPLY + CLASSIFICATION
        txt.insert(END, "\n\n" + "AI:\n")
        status, error_msg, classification = cohere.classify(response_prep, API_KEY)
        helper.log("status: " + str(status) + error_msg, DEBUG)

        helper.log(classification, DEBUG)
        txt.insert(END, "(" + classification + ")\n", 'tag')
        txt.insert(END, response+"\n\n")

        # ADD THIS INTERACTION TO HISTORY
        helper.log("adding to history logs...", DEBUG)
        helper.append_to_text_file(userInput, response, HISTORY_DIR, length=helper.length_classify(response), agreeableness=classification)
        e.delete(0, END)

    ### LAYOUT

    # DEBAIT HEADER
    image1 = Image.open(HEADER_LOGO_IMG)
    img = image1.resize((450,124), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img)
    lable1 = Label(root, image=test, bg=BG_GRAY).grid(row=0, sticky='w')

    # RIGHT-SIDE ARTICLE DISPLAY
    txt2 = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=70, height=30, wrap=WORD)
    txt2.grid(row=1, column=0, columnspan=1, padx=5)
    txt2.insert(END, "----------------------\nTopic of debate\n----------------------\n" + article)

    # LEFT-SIDE CONVERSATION DISPLAY
    txt = Text(root, bg="#B4C7E7", fg=TEXT_COLOR, font=FONT, width=70, height=30, wrap=WORD)
    txt.grid(row=1, column=1, columnspan=1)
    txt.tag_config('tag', foreground="green")

    # TEXTBOX FOR USER ENTRY
    e = Entry(root, text="type here...", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=53)
    e.grid(row=2, column=1, sticky='w')

    # SEND BUTTON
    send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1, sticky='e')

    root.mainloop()

if __name__ == "__main__":
    main()