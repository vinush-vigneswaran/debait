import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import cohere_api
from model import helper
from dotenv import load_dotenv
'''
Generate:
    - Test if we get reply from API
    - Test exception error
    
    CMD: pytest -s tests
'''
class TestCohereAPI:
    ## LOAD CONFIG ENV VARIABLES
    load_dotenv('config/config.env')

    API_KEY = os.getenv('API_KEY')

    TRAINING_DATA_DIR = 'prompt_data/training_data.txt'
    ARTICLE_DIR = 'prompt_data/article.txt'
    HISTORY_DIR = 'prompt_data/history.txt'

    training_data = helper.read_file(TRAINING_DATA_DIR)
    article = helper.read_file(ARTICLE_DIR)
    history = helper.read_file_lines(HISTORY_DIR, lookback=5) #only look back at 5 conversations

    def test_generate_return_string(self):
        # Test that string reply from API
        x = "This is a test input"
        user_input = [TestCohereAPI.article, x, "disagree", "short", ""]
        prompt = helper.generatePrompt(TestCohereAPI.training_data, TestCohereAPI.history, user_input)
        _,_,response = cohere_api.generate(prompt, TestCohereAPI.API_KEY)
        print(response)
        assert ((type(response) is str) and (len(response) > 2))

    def test_generate_invalid_request(self):
        # Test for invalid request - one token
        x = ""
        status, error_msg, response = cohere_api.generate(x, TestCohereAPI.API_KEY)
        print(status, error_msg, response)
        assert ((response == "") and (status==400) and (error_msg=="invalid request: prompt must be at least 1 token long"))