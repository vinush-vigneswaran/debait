from tkinter import *
import cohere_api as cohere
from PIL import ImageTk, Image

# GLOBAL VARIABLES
lookback = 5  # How many history examples to consider when answering.

with open('training_data.txt', 'r') as f:
    training_data = f.read()

with open('article.txt') as f:
    article = f.read()

with open('history.txt') as f:
    history = f.readlines()[0:5 * lookback]
    history = ''.join(history)


def generatePrompt(training_data, history, varInput):
    # Variables
    content = "\ncontent:" + varInput[0]
    current_user = "\ncurrent_user:" + varInput[1]
    agreeableness = "\nagreeableness:" + varInput[2]
    reply_length = "\nreply_length:" + varInput[3]
    cohere_user = "\ncohere_user:" + varInput[4]

    prompt = training_data + history + content + current_user + \
             agreeableness + reply_length + cohere_user
    return prompt

def log(txt):
    print(txt)

def append_to_text_file(user_text, generated_text, file, agree="disagree", length="medium"):
    final_text = "\ncurrent_user: " + user_text + "\nagreeableness: " + agree + "\nreply_length_char: " + \
                 length + "\ncohere_user: " + generated_text
    with open(file, "a") as myfile:
        myfile.write(final_text)


def length_classify(text):
    words = len(text.split())
    if words <= 25:
        return "short"
    elif words <= 50:
        return "medium"
    elif words > 50:
        return "long"


# GUI
BG_GRAY = "#FFFFFF"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#203864"

FONT = "Helvetica 9"
FONT_BOLD = "Helvetica 13 bold"

root = Tk()
root.title("Debait")
root.configure(bg=BG_GRAY)




# Send function
def send():
    log("button pressed...")
    send = e.get()

    txt.insert(END, "USER:\n")
    log("generating classification...")
    log(send)
    classification = cohere.classify(send)
    txt.insert(END, "(" + classification + ")\n", 'tag')
    txt.insert(END, "" + send)
    userInput = e.get()



    log("formatting for input...")
    input = [article, userInput, "disagree", "short", ""]
    prompt = generatePrompt(training_data, history, input)

    txt.tag_config('tag', foreground="green")
    txt.insert(END, "\n\n" + "AI:\n")

    log("generating response...")
    response = cohere.request(prompt)
    response_prep = response.replace("--", "")
    response_prep = response_prep.strip()
    log(response_prep)
    log("generating classification...")
    classification = cohere.classify(response_prep)
    log(classification)

    txt.insert(END, "(" + classification + ")\n", 'tag')
    txt.insert(END, response+"\n\n")

    # add to training data
    log("adding to history.txt...")
    append_to_text_file(userInput, response, 'history.txt', length=length_classify(response), agree=classification)
    e.delete(0, END)


image1 = Image.open("debait_logo.png")
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
