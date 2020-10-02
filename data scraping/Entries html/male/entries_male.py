import requests
import csv
from bs4 import BeautifulSoup as bs
import os

teams = ['228','280','77','34','394','425','60','53','405','73','336','174']
meets_male = ['22396','28738','51300','76429','104707','118535','166310']


def callData(team):
	for meet in meets_male:  #meets_male or meets_female
		if(team == '174' and meet == '22396'): #for male put meet = 22396, for female meet = 22373
			print('') #louisville was not in acc for this year
		else:
			getData(team,meet)

def getData(team,meet):
	file_name = '../../Data html/male/meet_id-' + meet + '_' + 'team-' + team + '.html' 

	with open(file_name, encoding = 'utf-8') as file:
		soup = bs(file, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

	year = soup.find('title').text.strip()[0:4] 

	season_id = int(year) - 1997
	
	for row in data:
		links = row.find_all('a')

		saveEntries(links[1]['href'])

	#if team has second page of players

	file_name = '../../Data html/male/meet_id-' + meet + '_' + 'team-' + team + '-page2.html' 
	
	if(os.path.isfile(file_name)):

		with open(file_name, encoding = 'utf-8') as file:
			soup = bs(file, 'html.parser')

		data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

		year = soup.find('title').text.strip()[0:4] 

		season_id = int(year) - 1997
	
		for row in data:
			links = row.find_all('a')

			saveEntries(links[1]['href'])
	else:
		print('no page 2')


def saveEntries(player_link):
	link = 'https://www.swimcloud.com' + player_link

	url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	player_link = player_link.replace('/','-')
	player_link += '.html'

	with open(player_link, 'w', encoding='utf-8') as file:
		file.write(url.text)

for team in teams:
	callData(team)