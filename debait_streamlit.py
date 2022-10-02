import streamlit as st
import cohere_api as cohere

import streamlit as st
import cohere_api as cohere

with open('training_data.txt', 'r') as f:
    training_data = f.read()

with open('article.txt') as f:
    article = f.read()

def generatePrompt(training_data,varInput):
    # Variables
    content = "\ncontent:" + varInput[0]
    current_user = "\ncurrent_user:" + varInput[1]
    agreeableness = "\nagreeableness:" + varInput[2]
    reply_length = "\nreply_length:" + varInput[3]
    cohere_user = "\ncohere_user:" + varInput[4]

    prompt = training_data + content + current_user + \
             agreeableness + reply_length + cohere_user

    return prompt

#design
st.header('Debait')

st.write(st.write(article))
uniKey1 = 1
uniKey2 = 2

userInput = st.text_input('Your statement', key=uniKey1)
if st.button('Answer', key=uniKey2):
    st.write(st.write("User: " + userInput))
    input = [article, userInput, "agree", "medium", ""]
    prompt = generatePrompt(training_data, input)
    response = cohere.request(prompt)
    st.write(st.write("AI: " + response))

