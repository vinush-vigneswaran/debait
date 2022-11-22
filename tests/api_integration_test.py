import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils import helper, cohere_api
from dotenv import load_dotenv
'''
Tests:
    - Response from API
    - Invalid requests from API
    - RUN: pytest -s tests
'''
class TestCohereAPI:
    ## LOAD CONFIG ENV VARIABLES
    load_dotenv('config/config.env')

    API_KEY = os.getenv('API_KEY')

    TRAINING_DATA_DIR = 'prompt_data/training_data.txt'
    ARTICLE_DIR = 'prompt_data/article.txt'
    HISTORY_DIR = 'prompt_data/history.txt'

    training_data = helper.read_file_lines(TRAINING_DATA_DIR)
    article = helper.read_file_lines(ARTICLE_DIR)
    history = helper.read_file_lines(HISTORY_DIR, lookback=5) #only look back at 5 conversations

    @pytest.mark.api_integration
    def test_generate_return_string(self):
        # Test that string reply from API
        user_input = ["This is a test user input", "disagree", "short", ""]
        prompt = helper.generate_prompt(training_data=self.training_data,history=self.history,article=self.article, values_for_prompt=user_input)
        _,_,response = cohere_api.generate(prompt, TestCohereAPI.API_KEY)
        print(response)
        assert type(response) is str
        assert len(response) > 2

    @pytest.mark.api_integration
    def test_generate_invalid_request(self):
        # Test for invalid request - one token
        x = ""
        status, error_msg, response = cohere_api.generate(x, TestCohereAPI.API_KEY)
        print(status, error_msg, response)
        assert response == ""
        assert status == 400
        assert error_msg == "invalid request: prompt must be at least 1 token long"

    @pytest.mark.api_integration
    def test_classify_return_classification(self):
        # Test that classification works
        x = "This is a test input"
        _,_,response = cohere_api.classify(x, TestCohereAPI.API_KEY)
        print("test_classify_return_classification", response)
        assert response == "statement"

    @pytest.mark.api_integration
    def test_classify_invalid_request(self):
        # Test for invalid request
        x = ""
        status,error_msg,response = cohere_api.classify(x, TestCohereAPI.API_KEY)
        print("test_classify_return_classification", response)
        assert response == "Call to API failed"
        assert status == 400
        assert error_msg == "invalid request: inputs contains an element that is the empty string at index 0"

#TODO: add mocks and do proper API integration