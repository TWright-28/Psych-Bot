import unittest
import io
import sys
import os

"""
    Set the path to the src folder and import FileReader class
"""
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")
from src.fileReader import FileReader

class Test(unittest.TestCase):
    myStdOut = None

    def setUp(self):
        self.myStdOut = io.StringIO()  # Create StringIO object
        sys.stdout = self.myStdOut     # and redirect stdout.

    """
        Testing if the data does exist and has certain amount of objects in the file
    """
    def testExistingData(self):
        fileReader = FileReader("data.json")
        self.assertEqual(len(fileReader.getFileContent()), 2)

    """
        Testing each of the conditions from the data.json file that has certain amount of the content in the conditions
    """
    def testExistingDataConditions(self):
        fileReader = FileReader("data.json")
        self.assertEqual(len(fileReader.getFileContent()['conditions']), 5)

    """
        Testing the existing data nodes from data.json file
    """
    def testExistingDataNodes(self):
        fileReader = FileReader("data.json")
        self.assertEqual(len(fileReader.getFileContent()['nodes']), 50)

    """
        Method to close the input and output stream
    """
    def tearDown(self):
        sys.stdout = sys.__stdout__   
        sys.stdin = sys.__stdin__

# Call the test class
if __name__ == '__main__':
    unittest.main()