def append_to_text_file(user_text, generated_text, file, agree = "agree", length = "medium"):
    final_text = "\ncurrent_user: " + user_text + "\nagreeableness: " + agree + "\nreply_length_char: " + \
                 length + "\ncohere_user: " + generated_text + "\n--"
    with open(file, "a") as myfile:
        myfile.write(final_text)



lookback = 5

with open('history.txt') as f:
    history = f.readlines()[0:5*lookback]
    history =''.join(history)

print(history)