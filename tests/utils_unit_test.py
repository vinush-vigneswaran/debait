import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils import helper


class TestClass:
    '''
    pytest -s tests -v
    pytest -m <tag name>    e.g. pytest -m utils_unit
    pytest --cov=app
    pytest -s tests -v --cov=app
    '''

    @pytest.fixture(scope="class")
    def dummy_values_for_prompt(self):
        return ["sample current_user text", "agree", "medium", "sample cohere_user text"]

    @pytest.fixture(scope="class")
    def dummy_generate_prompt(self, dummy_values_for_prompt):
        return helper.generate_prompt(values_for_prompt=dummy_values_for_prompt)

    @pytest.fixture(scope="class")
    def dummy_values_for_prompt_data(self):
        return ["training_data "*20, "history "*20, "article "*20]

    @pytest.mark.utils_unit
    def test_append_to_text_file(self, tmpdir, dummy_values_for_prompt, dummy_generate_prompt):
        filepath = os.path.join(tmpdir, "test.txt") #created temp file to test function
        x = dummy_values_for_prompt
        helper.append_to_text_file(x[0], x[3], filepath, x[1], x[2])
        with open(filepath, 'r') as f:
            contents_in_file = f.read()
        assert contents_in_file == dummy_generate_prompt

    @pytest.mark.utils_unit
    def test_generate_prompt(self, dummy_values_for_prompt):
        actual = helper.generate_prompt(values_for_prompt=dummy_values_for_prompt)
        expected = "\ncurrent_user:" + dummy_values_for_prompt[0] + "\nagreeableness:" + dummy_values_for_prompt[1] \
                   + "\nreply_length:" + dummy_values_for_prompt[2] + "\ncohere_user:" + dummy_values_for_prompt[3]
        assert actual == expected

    @pytest.mark.utils_unit
    def test_generate_prompt_with_data(self, dummy_values_for_prompt, dummy_values_for_prompt_data):
        actual = helper.generate_prompt(training_data=dummy_values_for_prompt_data[0],
                                        history=dummy_values_for_prompt_data[1],
                                        article=dummy_values_for_prompt_data[2],
                                        values_for_prompt=dummy_values_for_prompt)
        expected = dummy_values_for_prompt_data[0] + dummy_values_for_prompt_data[1] + \
                   "\ncontent:" + dummy_values_for_prompt_data[2] + \
                   "\ncurrent_user:" + dummy_values_for_prompt[0] + \
                   "\nagreeableness:" + dummy_values_for_prompt[1] +\
                   "\nreply_length:" + dummy_values_for_prompt[2] + \
                   "\ncohere_user:" + dummy_values_for_prompt[3]

        assert actual == expected

    @pytest.mark.utils_unit
    @pytest.mark.parametrize("text, classification", [
        (" ", 'short'),
        ("blah "*4, 'short'),
        ("blah "*24, 'short'),
        ("blah "*50, 'medium'),
        ("blah "*51, 'long'),
    ], ids=["empty", "v_short_str","short_str", "medium_str","long_str"])
    def test_length_classify(self, text, classification):
        assert helper.length_classify(text) == classification

    @pytest.mark.utils_unit
    @pytest.mark.parametrize("lookback", [(1),(5),(100)])
    def test_read_file_lines_lookback(self, tmpdir, lookback):
        filepath = os.path.join(tmpdir, "test.txt")
        file_str = ""
        expected = ""
        num_lines = lookback*10 #arbitrary

        for i in range(0,num_lines):
            file_str += "This is line " + str(i) + "\n"
            if i >= (num_lines-(5*lookback)):
                expected += "This is line " + str(i) + "\n"

        with open(filepath, "a") as file:
            file.write(file_str)

        assert helper.read_file_lines(filepath, lookback) == expected

    @pytest.mark.utils_unit
    def test_read_file_lines_no_lookback(self, tmpdir):
        filepath = os.path.join(tmpdir, "test.txt")
        expected_str = ""

        for i in range(0, 500):
            expected_str += "This is line " + str(i) + "\n"

        with open(filepath, "a") as file:
            file.write(expected_str)

        assert helper.read_file_lines(filepath) == expected_str