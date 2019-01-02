"""
Functions pertaining to loading NYC Airline data
"""

from bokeh.palettes import viridis
import collections
import csv
from datetime import datetime
import pandas as pd

def loadData():
	""" 
	Load NYC Airport data into dictionary
	The dictionary uses the airlines as keys
	Each Airline entry has a date, domestic, and internation entry
	"""
	dictionary = {}
	data = {}

	with open('../data-preprocess/NYCAirlineData.txt') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for row in csv_reader:
			if not row['Airline'] in dictionary:
				dictionary[row['Airline']] = {'date':[],'domestic':[],'international':[], 'airline': [], 'total':[]}

			dictionary[row['Airline']]['date'].append(datetime(int(row['Year']), int(row['Month']), 1))
			dictionary[row['Airline']]['domestic'].append(int(row['Domestic'])/1000000)
			dictionary[row['Airline']]['international'].append(int(row['International'])/1000000)
			dictionary[row['Airline']]['total'].append(int(row['Domestic'])/1000000 + int(row['International'])/1000000)
			dictionary[row['Airline']]['airline'].append(row['Airline'])

	#Create a dataframe from each dictionary and sort it by date
	for airline in dictionary:
		data[airline] = pd.DataFrame(data=dictionary[airline])
		data[airline] = data[airline].sort_values('date')

	#Create a dataframe to sort airlines alphabetically
	data = collections.OrderedDict(sorted(data.items()))

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

	return colors