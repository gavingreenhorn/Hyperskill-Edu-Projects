import unittest

import regex


class TestRegex(unittest.TestCase):
    def test_regular_match(self):
        self.assertTrue(regex.regex_engine('apple', 'pineapple pie'))
        self.assertFalse(regex.regex_engine('apple', 'orange'))

    def test_wildcard_match(self):
        self.assertTrue(regex.regex_engine('a..le', 'apple'))
        self.assertFalse(regex.regex_engine('.apple', 'apple'))

    def test_begin_match(self):
        self.assertTrue(regex.regex_engine('^apple', 'apple pie'))
        self.assertFalse(regex.regex_engine('^apple', 'pineapple'))

    def test_end_match(self):
        self.assertTrue(regex.regex_engine('apple$', 'pineapple'))
        self.assertFalse(regex.regex_engine('apple$', 'apple pie'))

    def test_full_match(self):
        self.assertTrue(regex.regex_engine('^apple$', 'apple'))
        self.assertFalse(regex.regex_engine('^apple$', 'apple pie'))

    def test_optional_char(self):
        self.assertTrue(regex.regex_engine('?color', 'ccolor'))
        self.assertTrue(regex.regex_engine('colo?r', 'color'))
        self.assertTrue(regex.regex_engine('color?', 'color'))
        self.assertTrue(regex.regex_engine('colou?r', 'color'))
        self.assertFalse(regex.regex_engine('coloo?r', 'colour'))
        self.assertFalse(regex.regex_engine('colou?r', 'colouur'))

    def test_optional_rep(self):
        self.assertTrue(regex.regex_engine('*color', 'color'))
        self.assertTrue(regex.regex_engine('colou*r', 'color'))
        self.assertTrue(regex.regex_engine('colou*r', 'colour'))
        self.assertTrue(regex.regex_engine('colou*r', 'colouur'))
        self.assertTrue(regex.regex_engine('colour*', 'colour'))
        self.assertTrue(regex.regex_engine('colour*', 'colourr'))

    def test_repeating_char(self):
        self.assertTrue(regex.regex_engine('+color', 'ccolor'))
        self.assertTrue(regex.regex_engine('colou+r', 'colouuur'))
        self.assertTrue(regex.regex_engine('color+', 'colorr'))
        self.assertTrue(regex.regex_engine('+color', 'color'))
        self.assertFalse(regex.regex_engine('colou+r', 'color'))
        self.assertFalse(regex.regex_engine('color+', 'colour'))

    def test_wildcard_rep(self):
        self.assertTrue(regex.regex_engine('colo.?r', 'color'))
        self.assertTrue(regex.regex_engine('colo.*r', 'colouur'))
        self.assertTrue(regex.regex_engine('colo.+r', 'colouur'))
        self.assertTrue(regex.regex_engine('colo.*r', 'colorr'))
        self.assertFalse(regex.regex_engine('colo.?r', 'colooor'))
        self.assertFalse(regex.regex_engine('colo.+r', 'color'))

    def test_escape_sequences(self):
        self.assertTrue(regex.regex_engine('\.$', 'end.'))
        self.assertTrue(regex.regex_engine('3\+3', '3+3=6'))
        self.assertTrue(regex.regex_engine('\?', 'Is this working?'))
        self.assertTrue(regex.regex_engine('\\\\', '\\'))
        self.assertFalse(regex.regex_engine('colou\?r', 'color'))
        self.assertFalse(regex.regex_engine('colou\?r', 'colour'))

    def test_edge_cases(self):
        self.assertTrue(regex.regex_engine('^no+pe$', 'noooooooope'))
        self.assertTrue(regex.regex_engine('.?', 'aaa'))


if __name__ == '__main__':
    unittest.main()
