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
        Simple test to see if the file exists.
        If it does not an error will be displayed 
    """
    def testNonExistingFile(self):
        with self.assertRaises(SystemExit) as ex:
            Bot("file.json")
            self.assertEqual(ex.exception, "Error")

    """
        Testing to see if the bot has an empty constructor.
        Returns an error if it is empty
    """
    def testEmptyBotConstructor(self):
        with self.assertRaises(TypeError) as ex:
            Bot()
            self.assertEqual(ex.exception, "Error")

    """
        Testing if the user has entered an empty name 
    """
    def testEmptyUsername(self):
        self.assertEqual(Bot("data.json").getUserName(), -1)

    """
        Testing that the username the user has entered is 
        a non empty username and setting that to the newuser variable
    """
    def testNonEmptyUsername(self):
        bot = Bot("data.json")
        bot.setUserName("NewUser")
        self.assertEqual(bot.getUserName(), "NewUser")

    """
        Displays a message with the user's name when they enter a non empty string
    """
    def testNonEmptySetUsernameOutput(self):
        bot = Bot("data.json")

        username = "NewUser"

        self.assertEqual(bot.setUserName(username), f"> Bot: Hello {username}.\nI am glad to have you here today, How are you feeling?\n\n")

    """
            Whenever the user enters  an empty argument, the username is 
            set and an error is displayed 
    """
    def testEmptyArgumentSetUsernameOutput(self):
        bot = Bot("data.json")
        with self.assertRaises(TypeError) as ex:
            bot.setUserName()
            self.assertEqual(ex.exception, "Error")

    """
        Tests if the user has entered a space instead of actual text
        will return an error if there is only a space
    """
    def testSpaceInputSetUsernameOutput(self):
        bot = Bot("data.json")
        username = "      "
        self.assertEqual(bot.setUserName(username), -1)

    """
        Tests if the username is a single space and will return 
        an error 
    """
    def testEmptyInputSetUsernameOutput(self):
        bot = Bot("data.json")
        self.assertEqual(bot.setUserName(""), -1)

    def tearDown(self):
        sys.stdout = sys.__stdout__   
        sys.stdin = sys.__stdin__

if __name__ == '__main__':
    unittest.main()