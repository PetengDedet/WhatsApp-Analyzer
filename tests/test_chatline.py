# -*- coding: utf-8 -*-
"""
Test the Chatline class
"""

import datetime
from unittest import TestCase
from chatline import Chatline


class TestChatline(TestCase):
    def test_parse_ampm_lowercase(self):
        cl = Chatline('[23/10/2020, 5:00:00 pm] User: message')

        expected = datetime.datetime(2020, 10, 23, 17, 0, 0)

        self.assertEqual(cl.timestamp, expected)

    def test_parse_ampm_uppercase(self):
        cl = Chatline('[23/10/2020, 5:00:00 PM] User: message')

        expected = datetime.datetime(2020, 10, 23, 17, 0, 0)

        self.assertEqual(cl.timestamp, expected)

    def test_parse_ampm_lowercase_with_dots(self):
        cl = Chatline('[23/10/2020, 5:00:00 p.m.] User: message')

        expected = datetime.datetime(2020, 10, 23, 17, 0, 0)

        self.assertEqual(cl.timestamp, expected)

    def test_parse_ampm_uppercase_with_dots(self):
        cl = Chatline('[23/10/2020, 5:00:00 P.M.] User: message')

        expected = datetime.datetime(2020, 10, 23, 17, 0, 0)

        self.assertEqual(cl.timestamp, expected)

    def test_extract_emojis(self):
        cl = Chatline('[23/10/2020, 5:00:00 pm] User: message 🍆')

        expected = ['🍆']

        self.assertEqual(cl.emojis, expected)
