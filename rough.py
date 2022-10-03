'''
THIS IS A ROUGH SCRIPT - NOT USED IN MAIN

This is a rough python testing ground of the
generate prompt function.
'''
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

userInput = 'Space exploration has also led to many indirect benefits. The challenge and difficulty of the space ' \
            'programme, and its ability to draw on some of the finest minds, has brought about great leaps in technology.'
input = [article, userInput, "agree", "short", ""]
prompt = generatePrompt(training_data, input)
print(prompt)
response = cohere.request(prompt)

# print(article + "\n-----------------")
# print(userInput + "\n-----------------")
print(response)