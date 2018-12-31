"""
Functions pertaining to loading NYC Airline data
"""

from bokeh.palettes import viridis
import csv
from datetime import datetime

def loadData():
	""" 
	Load NYC Airport data into dictionary
	The dictionary uses the airlines as keys
	Each Airline entry has a date, domestic, and internation entry
	"""
	data = {}

	loadFile(data, '../data-preprocess/Dec2017.txt', 12, 2017)
	loadFile(data, '../data-preprocess/Nov2017.txt', 11, 2017)
	loadFile(data, '../data-preprocess/Feb2000.txt', 2, 2000)

	return data

def getColors(data):
	"""
	Creates a dictionary of colors using the NYC Airport data dictionary
	"""
	colors = {}
	colorValues = viridis(len(data))

	color = 0
	for airline in data:
		colors[airline] = colorValues[color]
		color = color + 1
	
	print(colors)

	return colors

def loadFile(data, filename, month, year):
	"""
	Internal method to load individual file
	"""
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		i = 0
		for row in csv_reader:
			if i != 0:
				if not row[0] in data:
					data[row[0]] = {'date':[],'domestic':[],'international':[]}

				data[row[0]]['date'].append(datetime(year, month, 1))
				data[row[0]]['domestic'].append(int(row[1])/1000000)
				data[row[0]]['international'].append(int(row[2])/1000000)
			i = i + 1
