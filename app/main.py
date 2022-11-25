import gradio as gr
from app.utils import helper, cohere_api as cohere
from dotenv import load_dotenv
import os

def main():

    ## FILEPATHS
    TRAINING_DATA_DIR = '../prompt_data/training_data.txt'
    ARTICLE_DIR = '../prompt_data/article.txt'
    HISTORY_DIR = '../prompt_data/history.txt'
    CONFIG_DIR = '../config/config.env'

    DEBUG = True  # print app status to console when True
    load_dotenv(CONFIG_DIR)
    API_KEY = os.getenv('API_KEY')

    ### FILE DIRECTORY FOR PROMPT ENGINEERING
    training_data = helper.read_file_lines(TRAINING_DATA_DIR)
    article = helper.read_file_lines(ARTICLE_DIR)
    history = helper.read_file_lines(HISTORY_DIR, lookback=8)  # only look back at 5 conversations


    def predict(article, user_input,answer_length, convo_history=[]):

        # prepare the prompt format
        values_for_prompt = [user_input, "disagree", answer_length, ""]
        prompt = helper.generate_prompt(training_data=training_data,
                                        history=history,
                                        article=article,
                                        values_for_prompt=values_for_prompt)

        # log for debugging
        helper.log("values_for_prompt: " + str(values_for_prompt), DEBUG)
        helper.log("user_input: " + user_input, DEBUG)


        # generate response from AI model
        status, error_msg, response = cohere.generate(prompt, API_KEY)
        response_prep = response.replace("--", "").strip()
        helper.log("generate(): \t status[{}] \n {}".format(status, error_msg,response_prep), DEBUG)

        # classify user input and ai response
        user_classify_status, user_error_msg, user_classification = cohere.classify(user_input, API_KEY)
        helper.log("classify(USER): \t status[{}] \n {}".format(user_classify_status,
                                                                user_error_msg,
                                                                user_classification), DEBUG)

        model_classify_status, model_error_msg, model_classification = cohere.classify(response_prep, API_KEY)
        helper.log("classify(MODEL): \t status[{}] \n {}".format(model_classify_status,
                                                                 model_error_msg,
                                                                 model_classification), DEBUG)

        # add to conversation history logs
        helper.append_to_text_file(user_input, response, HISTORY_DIR, length=helper.length_classify(response),
                                   agreeableness=model_classification)

        # UI Gradio conversation history
        convo_history.append("["+user_classification+"]\n"+user_input)
        convo_history.append("["+model_classification+"]\n"+response_prep)
        response = [(convo_history[i], convo_history[i+1]) for i in range(0, len(convo_history)-1, 2)]

        return response, convo_history


    #Gradio UI Components
    article_textbox = gr.Textbox(
                    label="Article of discussion:",
                    lines=1,
                    interactive=False,
                    value=str(article))

    textbox = gr.Textbox(
                    label="User:",
                    lines=3,
                    placeholder="Write message here.")

    chatbot = gr.Chatbot(
        label="debait"
    ).style(color_map=("black", "blue"))

    answer_length = gr.Radio(
        choices = ["long", "medium", "short"],
        value = "medium",
        label = "Length of the response")

    css = "#component-2, .overflow-y-auto.h-\[40vh\] {height: 500px}"
    #<style>  # component-2 > div.overflow-y-auto.h-\[40vh\] {height: 500px}</style>
    # component-2 > div.overflow-y-auto.h-\[40vh\]
    #".output-image, .input-image, .image-preview {height: 600px !important}"
    app = gr.Interface(fn=predict,
                       inputs=[article_textbox, textbox, answer_length, "state"],
                       outputs=[chatbot, "state"],
                       allow_flagging='manual',
                       title='debait',
                       css=css)

    app.launch(debug=DEBUG, share=False)

if __name__ == "__main__":
    main()