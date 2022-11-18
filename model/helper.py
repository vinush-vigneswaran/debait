def append_to_text_file(user_text, generated_text, file, agree="disagree", length="medium"):
    '''
    This function appends the given in the correct text format for the co:here API
    prompt format. The text gets stored in a text file.
    Check whether the connection timed out - if so, do nothing.
    '''
    if (agree != "connection timed out!") and (generated_text != "connection timed out!"):

        final_text = "\ncurrent_user: " + user_text + "\nagreeableness: " + agree + "\nreply_length_char: " + \
                     length + "\ncohere_user: " + generated_text
        with open(file, "a") as myfile:
            myfile.write(final_text)

def generatePrompt(training_data, history, varInput):
    '''
    Generates the format required for the prompt
    '''
    content = "\ncontent:" + varInput[0]
    current_user = "\ncurrent_user:" + varInput[1]
    agreeableness = "\nagreeableness:" + varInput[2]
    reply_length = "\nreply_length:" + varInput[3]
    cohere_user = "\ncohere_user:" + varInput[4]

    prompt = training_data + history + content + current_user + \
             agreeableness + reply_length + cohere_user
    return prompt

def length_classify(text):
    '''
    Classifies the length of the given text
    (this is to add to the train data)
    '''
    words = len(text.split())
    if words <= 25:
        return "short"
    elif words <= 50:
        return "medium"
    elif words > 50:
        return "long"

def log(txt, DEBUG=True):
    '''
    Logging on console for debugging
    '''
    if (DEBUG):
        print(txt)

def read_file(DIR):
    '''
    read a file given a DIR
    '''
    with open(DIR, 'r') as f:
        content = f.read()
    return content

def read_file_lines(DIR, lookback):
    '''
    given directory read a specific number of lines in a file
    lookback: allows to see n number of most recent conversations
    '''
    with open(DIR) as f:
        content = f.readlines()[-5*lookback:]
        content = ''.join(content)
    return content