#!/usr/bin/python3

# Author: Alexey Bogdanenko
# Contact: alexey@bogdanenko.com
# works with python 3.2 and older

"""Tests for parse_email_addr function from parseaddr module"""

import unittest
from parseaddr import parse_email_addr

class ParseValidEmailAddr(unittest.TestCase):
    """Test parse_email_addr function with valid email addresses."""

    def valid_email_addr_generator(self):
        """ Generates valid email addresses

        Yields:
            Finite number of strings, each representing a valid email address
        """

        # simple cases
        yield 'jsmith@example.com'
        yield 'john.smith@example.com'
        yield 'john.w.smith@example.com'
        yield 'jsmith@big.company.com'
        yield 'jsmith@big-company.com'

        # unusual domain part
        yield 'admin@mailserver'     # local domain name with no TLD
        yield 'jsmith@xyz'           # short domain part
        yield 'jsmith@' + 'x' * 256  # long domain part
        yield 'jsmith@___.com'
        yield 'jsmith@3.14.com'
        yield 'jsmith@17-4-5'

        # unusual local part
        yield 'x' * 128 + '@example.com'  # long local part
        yield '.@example.com'
        yield '_@example.com'
        yield '-@example.com'
        yield '7@example.com'
        yield '.dots.@example.com'
        yield '__under__scores__dots.dots.dash--dash--@example.com'

        # local part with quotes
        yield '""@example.com'
        yield '"quoted"@example.com'
        yield '"double"quotes@example.com'
        yield 'double"quotes"@example.com'
        yield '""""@example.com'
        yield '"double"_"quotes"@example.com'
        yield '"!"double","quotes"comma,colon:"@example.com'
        yield '","@example.com'

    def test_valid_email_addr(self):
        """Test with valid email addresses.
        
        Pass valid addresses to parse_email_addr function and check that
        it returns 0.
        """
        for text in self.valid_email_addr_generator():
            returned_value = parse_email_addr(text) 
            self.assertIsInstance(returned_value, int)
            msg = ('text <{}> should have been classified as a valid email'
                ' address').format(text)
            self.assertEqual(returned_value, 0, msg)

class ParseBadInput(unittest.TestCase):
    """Test parse_email_addr function with non-string objects."""

    def test_bad_input(self):
        """Test with non-string objects.

        Check that parse_email_addr function raises TypeError.
        """
        for obj in (None, list(), dict(), bytes()):
            self.assertRaises(TypeError, parse_email_addr, obj)

class ParseBadText(unittest.TestCase):
    """Test parse_email_addr function with bad input strings."""

    def bad_text_generator(self):
        """ Generates invalid email addresses

        Yields:
            Finite number of tuples (text, rule_number). text is a string that
            may or may not look like an email address, in any case, it is not a
            valid email address; rule_number is number of the first Rule text
            doesn't comply with.
        """
        cyrillic_letter_a = chr(0x0430)  # illegal character

        # either local part or domain part is missing
        yield '', 1
        yield ' ', 1
        yield '\n', 1
        yield 'jsmith-at-example.com', 1
        yield '@', 1
        yield 'jsmith@', 1
        yield '@example.com', 1

        yield 'jsmith@xy', 2            # domain part is too short
        yield 'jsmith@' + 'x' * 257, 2  # domain part is too long

        # illegal characters in domain part
        yield 'extra@at@sign.com', 2  
        yield 'jsmith@space space.com', 2
        yield 'jsmith@plus+plus.com', 2
        yield 'jsmith@back\\slash.com', 2
        yield 'jsmith@double"quote.com', 2
        yield 'jsmith@example.com\n', 2
        yield 'jsmith@capitalLetter.com', 2
        yield 'apetrov@y{}ndex.ru'.format(cyrillic_letter_a), 2

        # subdomain starts or ends with a dash
        yield 'jsmith@ends.with-.dash.com', 3
        yield 'jsmith@starts.with.-dash.com', 3

        yield 'x' * 129 + '@example.com', 4  # local part is too long
        
        # illegal characters in local part
        yield 'space space@example.com', 4
        yield '{}petrov@yandex.ru'.format(cyrillic_letter_a), 4
        yield 'capitalLetter@example.com', 4

        # consecutive dots in local part are not allowed
        yield 'double..dots@example.com', 5
        yield 'triple...dots@example.com', 5
        yield '..@example.com', 5

        # missing quote in local part
        yield 'missing"quote@example.com', 6
        yield '"@example.com', 6
        yield '"missing"quote"@example.com', 6
        yield '"""@example.com', 6

        # punctuation characters "!,:" must be inside quotes
        yield 'exclamation!point@example.com', 7
        yield 'comma,comma@example.com', 7

    def test_bad_text(self):
        """Test with a bad input strings.

        Check that parse_email_addr function returns correct error code.
        """
        for text, err_code in self.bad_text_generator():
            returned_value = parse_email_addr(text) 
            self.assertIsInstance(returned_value, int)
            if returned_value:
                msg = 'wrong rule number returned for bad text <{}>'
            else:
                msg = ('text <{}> was incorrectly classified as a valid email'
                    ' address')
            msg = msg.format(text)

            self.assertEqual(returned_value, err_code, msg)

if __name__ == '__main__':
    unittest.main()
