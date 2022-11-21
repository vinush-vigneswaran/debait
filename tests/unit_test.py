import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils import helper


class TestClass:

    def test_length_classify_1(self):
        # Test short output (<=25)
        x = 'You are correct'
        assert helper.length_classify(x) == 'short'

    def test_length_classify_2(self):
        # Test short output (<=50)
        x = 'You are correct, the principles of thermodynamics indicate that perpetual motion is a ruse'
        assert helper.length_classify(x) == 'short'

    def test_length_classify_3(self):
        # Test medium output (<=50)
        x = "Space is the boundless three-dimensional extent in which objects and events have relative position and direction. In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime. Blah Blah"
        assert helper.length_classify(x) == 'medium'

    def test_length_classify_4(self):
        # Test long output (>50) - 50 words
        x = "Space is the boundless three-dimensional extent in which objects and events have relative position and direction. In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime. Blah Blah Blah Blah"
        assert helper.length_classify(x) == 'long'