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
       Test case assures that if the file does not exist than the expected error is catched and handled.
    """
    def testNonExistingFile(self):
        with self.assertRaises(SystemExit) as ex:
            Bot("file.json")
            self.assertEqual(ex.exception, "Error")

    """
        Testing to see if the bot has an empty constructor if so an error is to be expected.
    """
    def testEmptyBotConstructor(self):
        with self.assertRaises(TypeError) as ex:
            Bot()
            self.assertEqual(ex.exception, "Error")

    """
        Tests if the user has entered an empty username, if so a -1 should be expected.
    """
    def testEmptyUsername(self):
        self.assertEqual(Bot("data.json").getUserName(), -1)

    """
        testing that the user has entered a non-empty username and setting that name to the NewUser variable
    """
    def testNonEmptyUsername(self):
        bot = Bot("data.json")
        bot.setUserName("NewUser")
        self.assertEqual(bot.getUserName(), "NewUser")

    """
        Displays a message with the user's name when they enter a non-empty string
    """
    def testNonEmptySetUsernameOutput(self):
        bot = Bot("data.json")

        username = "NewUser"

        self.assertEqual(bot.setUserName(username), f"> Bot: Hello {username}.\nI am glad to have you here today, How are you feeling?\n\n")

    """
        Testing if the user has entered an empty argument, If so an error is to be expected.
    """
    def testEmptyArgumentSetUsernameOutput(self):
        bot = Bot("data.json")
        with self.assertRaises(TypeError) as ex:
            bot.setUserName()
            self.assertEqual(ex.exception, "Error")

    """
        Test Case asserts that if the user provides only spaces than a -1 should be expected
    """
    def testSpaceInputSetUsernameOutput(self):
        bot = Bot("data.json")
        username = "      "
        self.assertEqual(bot.setUserName(username), -1)

    """
       Test Case asserts that if the user provides an empty input than a -1 should be expected
    """
    def testEmptyInputSetUsernameOutput(self):
        bot = Bot("data.json")
        self.assertEqual(bot.setUserName(""), -1)

    """
        Test case which tests a sentient polarity score of positive user responses which checks using the sentimentPolarityScore. If it is it will return a 1
        and then it will be checked using the assertEqual method if they do not match
    """
    def testGetSentimentPolarityScoreOfNegativeResponse(self):
        bot = Bot("data.json")
        self.assertNotEqual(bot.getSentimentPolarityScore(["tired", "sick", "anxiety"]), 1)

    """
        Test case which tests a sentient polarity score of negative user responses which checks using the sentimentPolarityScore. If it is then we ensure that a 1 will not be returned
        and then it will be checked using the assertEqual method 

    """
    def testGetSentimentPolarityScoreOfPositiveResponse(self):
        bot = Bot("data.json")
        self.assertEqual((bot.getSentimentPolarityScore(["lovely", "good", "well"])).get('pos'), 1)

    """
        Test case which tests a sentient polarity score of neutral user responces which checks using the sentimentPolarityScore. If it is it will return a 1
        and then it will be checked using the assertEqual method if they match
    """
    def testGetSentimentPolarityScoreOfNeutralResponse(self):
        bot = Bot("data.json")
        self.assertEqual((bot.getSentimentPolarityScore(["disinterested", "inactive"])).get('neu'), 1)

    """
        Test case which tests a sentient polarity score of mixew user responces which checks using the sentimentPolarityScore. If it is it will return a 1
        and then it will be checked using the assertNotEqual method if they do not match
    """
    def testGetSentimentPolarityScoreOfMixedResponse(self):
        bot = Bot("data.json")
        self.assertNotEqual((bot.getSentimentPolarityScore(["disinterested", "good", "sick"])).get('compound'), 1)

    """
        Test case for ensuring that the method will return a list of values such that the element at index 1 matches our output
    """
    def testGetWordNetSynsetResultWithNonEmptyResponse(self):
        bot = Bot("data.json")
        self.assertEqual(bot.getWordNetSynsetResult("exhausted")[1], "exhaust")

    """
        Test Case for getting the results from NetSynset with an empty response. If so expect a result of -1
    """
    def testGetWordNetSynsetResultWithEmptyResponse(self):
        bot = Bot("data.json")
        self.assertEqual(bot.getWordNetSynsetResult(""), -1)

    """
       Test case for getting the PosTag with a question response
    """
    def testGetPosTagWithQuestionResponse(self):
        bot = Bot("data.json")
        self.assertEqual(bot.getPosTag({ 'pos': ['VB', 'WP', 'WRB', 'WDT'] }, ["what", "should", "i", "do", "?"]), ['VB', 'WP'])

    """
       Test case for getting the PosTag with a modal response
    """
    def testGetPosTagWithModalResponse(self):
        bot = Bot("data.json")
        self.assertEqual(bot.getPosTag({ 'pos': ['VB', 'WP', 'WRB', 'MD'] }, ["could", "you", "help", "me", "?"]), ['VB', 'MD'])

    """
        Method to close the input and output stream
    """
    def tearDown(self):
        sys.stdout = sys.__stdout__   
        sys.stdin = sys.__stdin__

# Call the test class
if __name__ == '__main__':
    unittest.main()
