import json

class FileReader:
	"""
		Constructor method
	"""
	def __init__(self):
		self.fileContent = self.parseFile()

	"""
	 	Method to open existing file with questions and possible responses,
		and return the Object of this file.
	"""
	def parseFile(self):
		with open("data.json", "r") as file:
			data = json.loads(file.read())
		return data

	"""
		Return a content of the file parsed in parseFile method.
	"""
	def getFileContent(self):
		return self.fileContent