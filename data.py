import requests
import csv
from bs4 import BeautifulSoup as bs
import time

#DECLARATIONS ------------------------------------------------------------------

roster = list()
teams = ['228','280','77','34','394','425','60','53','405','73','336','174']
meets_male = ['22396','28738','51300','76429','104707','118535','166310']
meets_female = ['22373','28737','51800','76431','104673','118536','166285']

team_names = {'228' : 'Boston College', 
			  '280' : 'Duke University',
			  '77' : 'Florida State University',
			  '34' : 'Georgia Institute of Technology',
			  '394' : 'North Carolina State University',
			  '425' : 'University of Miami (Florida)',
			  '60' : 'University of North Carolina, Chapel Hill',
			  '53' : 'University of Notre Dame',
			  '405' : 'University of Pittsburgh',
			  '73' : 'University of Virginia', 
			  '336' : 'Virginia Tech',
			  '174' : 'University of Louisville'}

#FUNCTIONS ----------------------------------------------------------------------

#adds every swimmer to roster list
def getRoster(season_id,team):
	file_name = './Roster html/female/team-' + team + '_' + 'season_id-' + str(season_id) + '.html' #/male/ or /female/

	with open(file_name, encoding = 'utf-8') as file:
		soup = bs(file, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

	for row in data:
		webName = row.find('a').text.strip()
		name = cleanName(webName)
		numbers = row.find_all('td')
		grade = numbers[3].text.strip()
		start = getStart(season_id,grade)
		if(not containsPlayer(name)):
			roster.append({'name': name, 'webName' : webName, 'team' : team, 'start' : start, 'FR': '', 'Events-FR' : '', 'SO' : '', 'Events-SO' : '', 'JR' : '', 'Events-JR' : '', 'SR' : '', 'Events-SR' : ''})

#checks if swimmer is already in roster
def containsPlayer(name):
	for i in range(len(roster)):
		if(roster[i]['name'] == name):
			return True
	return False

def cleanName(webName):
	nameList = webName.split(', ')
	last = nameList[0]
	first_middle = nameList[1].split(' ')
	first = first_middle[0]
	return first + ' ' + last

#finds index of swimmer in roster
def playerIndex(name):
	for i in range(len(roster)):
		if(roster[i]['name'] == name):
			return i
	return 0

#returns what grade the swimmer is 
def playerGrade(season_id, index):
	start = roster[index]['start']

	if(season_id == start):
		return 'FR'
	elif(season_id - 1 == start):
		return 'SO'
	elif(season_id - 2 == start):
		return 'JR'
	else:
		return 'SR'

#returns season_id for when swimmer was a freshman
def getStart(season_id, grade):
	if(grade == 'FR'):
		return season_id
	elif(grade == 'SO'):
		return season_id - 1
	elif(grade == 'JR'):
		return season_id - 2
	else:
		return season_id - 3

def getData(team,meet):
	file_name = './Data html/female/meet_id-' + meet + '_' + 'team-' + team + '.html'  #/male/ or /female/

	with open(file_name, encoding = 'utf-8') as file:
		soup = bs(file, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

	year = soup.find('title').text.strip()[0:4] 

	season_id = int(year) - 1997
	
	for row in data:
		links = row.find_all('a')
		name = links[0].text.strip()

		numbers = row.find_all('td')
		points = numbers[5].text.strip()
		if(points == '–'):
			points = '0'

		entries = findEntries(links[1]['href'])
		index = playerIndex(name)
		grade = playerGrade(season_id, index)

		key = 'Events-' + grade

		roster[index][key] = entries
		roster[index][grade] = points

def findEntries(link):
	link = link.replace('/', '-')

	file_name = './Entries html/female/' + link + '.html'  #/male/ or /female/

	with open(file_name, encoding ='utf-8') as file:
		soup = bs(file,'html.parser')

	data = soup.find('ul', attrs = {'class' : 'c-splash-stats'}).find_all('div')

	if(data[5].text.strip() != '0'):
		return data[5].text.strip()
	else: 
		entries = 0
		events = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

		for row in events:
			numbers = row.find_all('td')
			if(numbers[3].text.strip() == 'Prelims'):
				entries += 1
		return entries

def callRoster(team):
	for i in range(7):
		start = 17 + i  #starts at 17 which corresponds to the season_id on swimcloud for the 2013-14 season
		getRoster(start,team) 

def callData(team):
	for meet in meets_female:  #meets_male or meets_female
		if(team == '174' and meet == '22373'): #for male put meet = 22396, for female meet = 22373
			print('') #louisville was not in acc for this year
		else:
			getData(team,meet)

#MAIN --------------------------------------------------------------------------------------

for team in teams:
	callRoster(team)

for team in teams:
	callData(team)

file = open('swimmers_female.csv','w', newline = '', encoding ='utf-8')  #swimmers_male or swimmers_female
writer = csv.writer(file)

writer.writerow(['Name','Team','FR','Events-FR','SO','Events-SO','JR','Events-JR','SR','Events-SR','Total Points'])

for i in range(len(roster)):
	roster[i]['team'] = team_names[roster[i]['team']]
	total_points = 0

	if(roster[i]['FR'].isdigit()):
		total_points += int(roster[i]['FR'])
	if(roster[i]['SO'].isdigit()):
		total_points += int(roster[i]['SO']) 
	if(roster[i]['JR'].isdigit()):
		total_points += int(roster[i]['JR'])
	if(roster[i]['SR'].isdigit()):
		total_points += int(roster[i]['SR'])

	writer.writerow([roster[i]['name'], roster[i]['team'],roster[i]['FR'],roster[i]['Events-FR'],roster[i]['SO'],roster[i]['Events-SO'],roster[i]['JR'],roster[i]['Events-JR'],roster[i]['SR'],roster[i]['Events-SR'],total_points])

file.close()



