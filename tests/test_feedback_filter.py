import unittest
from .decorators import measure_time
from app.utils.feedback_filter import filter_feedback_stream

class TestFeedbackFilter(unittest.TestCase):

    @measure_time
    def test_no_separator(self):
        input_stream = (chunk for chunk in ["This is ", "a test ", "without separator"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["This is ", "a test ", "without separator"])

    @measure_time
    def test_with_separator(self):
        input_stream = (chunk for chunk in ["This is ", "a test ### with ", "separator ", "and more"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["This is ", "a test "])

    @measure_time
    def test_separator_in_first_chunk(self):
        input_stream = (chunk for chunk in ["Test ### separator", " in first chunk"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["Test "])

    @measure_time
    def test_empty_input(self):
        input_stream = (chunk for chunk in [])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, [])

    @measure_time
    def test_separator_split_across_chunks(self):
        input_stream = (chunk for chunk in ["This is a ", "test #", "#", "# with ", "separator split"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["This is a ", "test "])

    @measure_time
    def test_partial_separator_at_end(self):
        input_stream = (chunk for chunk in ["This is a test #", "# but not quite"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["This is a test ## but not quite"])

    @measure_time
    def test_multiple_separators(self):
        input_stream = (chunk for chunk in ["First ### Second ", "### Third"])
        filtered = list(filter_feedback_stream(input_stream))
        self.assertEqual(filtered, ["First "])

    @measure_time
    def test_exception_in_stream(self):
        def exception_generator():
            yield "This is the first chunk"
