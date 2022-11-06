from tkinter import *
import cohere_api as cohere
import helper
from PIL import ImageTk, Image

def main():
    ### GLOBAL VARIABLES
    DEBUG = True #print app status to console when True

    ### FILE DIRECTORY FOR PROMPT ENGINEERING
    TRAINING_DATA_DIR = 'prompt_data\\training_data.txt'
    ARTICLE_DIR = 'prompt_data\\article.txt'
    HISTORY_DIR ='prompt_data\\history.txt'

    training_data = helper.read_file(TRAINING_DATA_DIR)
    article = helper.read_file(ARTICLE_DIR)
    history = helper.read_file_lines(HISTORY_DIR, lookback=5) #only look back at 5 conversations

    log = helper.log("button pressed...", DEBUG)

    ### GUI DECORATION VARIABLES
    BG_GRAY = "#FFFFFF"
    BG_COLOR = "#FFFFFF"
    TEXT_COLOR = "#203864"
    FONT = "Helvetica 9"
    FONT_BOLD = "Helvetica 13 bold"
    HEADER_LOGO_IMG = "media/debait_logo.png"

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
        classification = cohere.classify(send)
        txt.insert(END, "(" + classification + ")\n", 'tag')
        txt.insert(END, "" + send)
        userInput = e.get()

        # PREPARE PROMPT
        helper.log("formatting for input...", DEBUG)
        input = [article, userInput, "disagree", "short", ""]
        prompt = helper.generatePrompt(training_data, history, input)

        # GENERATING AI RESPONSE USING PROMPT
        helper.log("generating response...", DEBUG)
        response = cohere.request(prompt)
        response_prep = response.replace("--", "")
        response_prep = response_prep.strip()
        helper.log(response_prep, DEBUG)
        helper.log("generating classification...", DEBUG)

        # DISPLAY GENERATED AI REPLY + CLASSIFICATION
        txt.insert(END, "\n\n" + "AI:\n")
        classification = cohere.classify(response_prep)
        helper.log(classification, DEBUG)
        txt.insert(END, "(" + classification + ")\n", 'tag')
        txt.insert(END, response+"\n\n")

        # ADD THIS INTERACTION TO HISTORY
        helper.log("adding to history logs...", DEBUG)
        helper.append_to_text_file(userInput, response, HISTORY_DIR, length=helper.length_classify(response), agree=classification)

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