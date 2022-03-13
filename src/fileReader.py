import json
import sys
class FileReader:
	"""
		Constructor method
	"""
	def __init__(self, filePath):
		try:
			self.fileContent = self.parseFile(filePath)
		except:
			print("File is not found")
			sys.exit(1)	
	"""
	 	Method to open existing file with questions and possible responses,
		and return the Object of this file.
	"""
	def parseFile(self, filePath):
		with open(filePath, "r") as file:
			data = json.loads(file.read())
		return data

	"""
		Return a content of the file parsed in parseFile method.
	"""
	def getFileContent(self):
		return self.fileContent