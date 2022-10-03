from tkinter import *
import cohere_api as cohere
import helper
from PIL import ImageTk, Image


# FILE DIRECTORY FOR PROMPT ENGINEERING
TRAINING_DATA_DIR = 'prompt_data\\training_data.txt'
ARTICLE_DIR = 'prompt_data\\article.txt'
HISTORY_DIR ='prompt_data\\history.txt'

# READ FILES
training_data = helper.read_file(TRAINING_DATA_DIR)
article = helper.read_file(ARTICLE_DIR)
history = helper.read_file_lines(HISTORY_DIR, lookback=5) #only look back at 5 conversations

# GUI VARIABLES
BG_GRAY = "#FFFFFF"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#203864"

FONT = "Helvetica 9"
FONT_BOLD = "Helvetica 13 bold"

# TKINTER APPLICATION
root = Tk()
root.title("Debait")
root.configure(bg=BG_GRAY)

def send():
    helper.log("button pressed...")
    send = e.get()

    txt.insert(END, "USER:\n")
    helper.log("generating classification...")
    helper.log(send)
    classification = cohere.classify(send)
    txt.insert(END, "(" + classification + ")\n", 'tag')
    txt.insert(END, "" + send)
    userInput = e.get()

    helper.log("formatting for input...")
    input = [article, userInput, "disagree", "short", ""]
    prompt = helper.generatePrompt(training_data, history, input)

    txt.tag_config('tag', foreground="green")
    txt.insert(END, "\n\n" + "AI:\n")

    helper.log("generating response...")
    response = cohere.request(prompt)
    response_prep = response.replace("--", "")
    response_prep = response_prep.strip()
    helper.log(response_prep)
    helper.log("generating classification...")
    classification = cohere.classify(response_prep)
    helper.log(classification)

    txt.insert(END, "(" + classification + ")\n", 'tag')
    txt.insert(END, response+"\n\n")

    # add to training data
    helper.log("adding to history.txt...")
    helper.append_to_text_file(userInput, response, HISTORY_DIR, length=helper.length_classify(response), agree=classification)
    e.delete(0, END)


image1 = Image.open("media/debait_logo.png")
img = image1.resize((450,124), Image.ANTIALIAS)
test = ImageTk.PhotoImage(img)
# label1 = Label(image=test)
# label1.image = test
# test = test.zoom((0.5, 0.5))

lable1 = Label(root, image=test, bg=BG_GRAY).grid(row=0, sticky='w')

txt = Text(root, bg="#B4C7E7", fg=TEXT_COLOR, font=FONT, width=70, height=30, wrap=WORD)
txt.grid(row=1, column=1, columnspan=1)

txt2 = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=70, height=30, wrap=WORD)
txt2.grid(row=1, column=0, columnspan=1, padx=5)
txt2.insert(END, "----------------------\nTopic of debate\n----------------------\n" + article)

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

# scrollbar2 = Scrollbar(txt2)
# scrollbar2.place(relheight=1, relx=0.974)

e = Entry(root, text="type here...", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=53)
e.grid(row=2, column=1, sticky='w')

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
              command=send).grid(row=2, column=1, sticky='e')

root.mainloop()
