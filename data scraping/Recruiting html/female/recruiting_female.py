import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs

def callData(name):	
	cleanName = name.replace(" ", "+")
	url = 'https://www.swimcloud.com/recruiting/rankings/?name=' + cleanName
	saveData(url, cleanName)


def saveData(link, cleanName):
	url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	name = cleanName + '.html'

	with open(name, 'w', encoding = 'utf-8') as file:
		file.write(url.text)


roster = pd.read_csv('../../swimmers_female_info.csv')
for index, row in roster.iterrows():
	name = row['Name']
	callData(name)




