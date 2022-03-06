import unittest
import io
import sys
import os

"""
    Set the path to the src folder and import Bot class
"""
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")
from src.bot import Bot

class Test(unittest.TestCase):
    myStdOut = None

    def setUp(self):
        self.myStdOut = io.StringIO()  # Create StringIO object
        sys.stdout = self.myStdOut     # and redirect stdout.

    """
        Documentation goes here
    """
    def testNonExistingFile(self):
        with self.assertRaises(SystemExit) as ex:
            Bot("file.json")
            self.assertEqual(ex.exception, "Error")

    """
        Documentation goes here
    """
    def testEmptyBotConstructor(self):
        with self.assertRaises(TypeError) as ex:
            Bot()
            self.assertEqual(ex.exception, "Error")

    """
        Documentation goes here
    """
    def testEmptyUsername(self):
        self.assertEqual(Bot("data.json").getUserName(), -1)

    """
        Documentation goes here
    """
    def testNonEmptyUsername(self):
        bot = Bot("data.json")
        bot.setUserName("NewUser")
        self.assertEqual(bot.getUserName(), "NewUser")

    """
        Documentation goes here
    """
    def testNonEmptySetUsernameOutput(self):
        bot = Bot("data.json")

        username = "NewUser"

        self.assertEqual(bot.setUserName(username), f"> Bot: Hello {username}.\nI am glad to have you here today, How are you feeling?\n\n")

    """
        Documentation goes here
    """
    def testEmptyArgumentSetUsernameOutput(self):
        bot = Bot("data.json")
        with self.assertRaises(TypeError) as ex:
            bot.setUserName()
            self.assertEqual(ex.exception, "Error")

    """
        Documentation goes here
    """
    def testSpaceInputSetUsernameOutput(self):
        bot = Bot("data.json")
        username = "      "
        self.assertEqual(bot.setUserName(username), -1)

    """
        Documentation goes here
    """
    def testEmptyInputSetUsernameOutput(self):
        bot = Bot("data.json")
        self.assertEqual(bot.setUserName(""), -1)

    def tearDown(self):
        sys.stdout = sys.__stdout__   
        sys.stdin = sys.__stdin__

if __name__ == '__main__':
    unittest.main()