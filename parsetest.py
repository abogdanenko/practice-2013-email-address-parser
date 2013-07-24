#!/usr/bin/python3

# Author: Alexey Bogdanenko
# Contact: alexey@bogdanenko.com
# works with python 3.2 and older

"""Tests for parse_email_addr function from parseaddr module"""

import unittest
from parseaddr import parse_email_addr

class ParseBadInput(unittest.TestCase):

    def test_bad_input(self):
        """Test with a non-string object."""
        for obj in (None, list(), dict(), bytes()):
            self.assertRaises(TypeError, parse_email_addr, obj)

class ParseBadText(unittest.TestCase):

    def generate_bad_text(self):
        cyrillic_letter_a = chr(0x0430) 

        yield '', 1
        yield ' ', 1
        yield '\n', 1
        yield 'jsmith-at-example.com', 1
        yield '@', 1
        yield 'jsmith@', 1
        yield '@example.com', 1

        yield 'jsmith@xy', 2
        yield 'jsmith@' + 'x' * 256, 2
        yield 'jsmith@space space.com', 2
        yield 'jsmith@plus+plus.com', 2
        yield 'jsmith@back\\slash.com', 2
        yield 'jsmith@double"quote.com', 2
        yield 'jsmith@example.com\n', 2
        yield 'apetrov@y{}ndex.ru'.format(cyrillic_letter_a), 2
        yield 'capitalLetter@example.com', 2

        yield 'jsmith@ends.with-.dash.com', 3
        yield 'jsmith@starts.with.-dash.com', 3

        yield 'x' * 129 + '@example.com', 4
        yield 'space space@example.com', 4
        yield '{}petrov@yandex.ru'.format(cyrillic_letter_a), 4
        yield 'jsmith@capitalLetter.com', 4

        yield 'double..dots@example.com', 5
        yield 'triple...dots@example.com', 5
        yield '..@example.com', 5

        yield 'missing"quote@example.com', 6
        yield '"@example.com', 6
        yield '"missing"quote"@example.com', 6
        yield '"""@example.com', 6
        yield 'exclamation!point@example.com', 7
        yield 'comma,comma@example.com', 7

    def test_bad_text(self):
        """Test with bad input string."""
        for text, err_code in self.generate_bad_text():
            returned_value = parse_email_addr(text) 
            self.assertIs(returned_value, int)
            if returned_value:
               msg = 'wrong rule number returned for bad text <{}>'
            else:
               msg = ('text <{}> was incorrectly classified as a valid email'
                   ' address')
            msg = msg.format(text)

            self.assertEqual(returned_value, err_code, msg)

class ParseValidEmailAddr(unittest.TestCase):

    def generate_valid_email_addr(self):
        yield 'jsmith@example.com', 0
        yield 'john.smith@example.com', 0
        yield 'john.w.smith@example.com', 0

        yield 'admin@mailserver', 0  # local domain name with no TLD
        yield 'jsmith@xyz', 0
        yield 'jsmith@' + 'x' * 255, 0
        yield 'jsmith@___.com', 0
        yield 'jsmith@3.14.com', 0
        yield 'jsmith@17-4-5', 0
        yield 'jsmith@big-company.com', 0
        yield 'jsmith@big.company.com', 0
        yield 'jsmith@big-company.com', 0

        yield 'x' * 128 + '@example.com', 0
        yield '.@example.com', 0
        yield '_@example.com', 0
        yield '-@example.com', 0
        yield '7@example.com', 0
        yield '.dots.@example.com', 0
        yield '__under__scores__dots.dots.dash--dash--@example.com', 0

        yield '""@example.com', 0
        yield '"double"quotes@example.com', 0
        yield '""""@example.com', 0
        yield '"double"_"quotes"@example.com', 0
        yield '"!"double","quotes"comma,colon:"@example.com', 0
        yield '","@example.com', 0

    def test_valid_email_addr(self):
        """Test with a valid email address."""
        for text, err_code in self.generate_valid_email_addr():
            returned_value = parse_email_addr(text) 
            self.assertIs(returned_value, int)
            msg = ('text <{}> should have been classified as a valid email'
                ' address').format(text)
            self.assertEqual(returned_value, err_code, msg)

if __name__ == '__main__':
    unittest.main()
