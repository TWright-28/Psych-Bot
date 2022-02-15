from nltk.stem.porter import PorterStemmer
import json

stemmer = PorterStemmer()

with open("data.json", "r") as file:
	data = json.loads(file.read())

conditions = {}
nodes = data['nodes']

for key in data['conditions'].keys():
	words = [stemmer.stem(word) for word in data['conditions'][key]]
	conditions[key] = words

def find_node(id):
	if id is None:
		return None
	for node in nodes:
		if node['id'] == id:
			return node
	return None

name = input("Hello, I am Psych-Bot. What is your name?")

input(f"Hello {name}, how are you feeling today?")
current = nodes[0]

while current != None:
	if 'print' in current:
		print(current['text'])
		current = find_node(current['children'][0])
		continue
	answer = input(current['text'])
	if len(current['children']) == 1:
		current = find_node(current['children'][0])
	else:
		answer_words = [stemmer.stem(word) for word in answer.lower().split(" ")]
		for child in current['children']:
			child = find_node(child)
			if 'default' in child:
				current = child
				break
			for word in conditions[child['condition']]:
				if word in answer_words:
					current = child
			if current == child:
				break