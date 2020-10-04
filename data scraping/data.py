import requests
import csv
from bs4 import BeautifulSoup as bs
import time
import os

#DECLARATIONS ------------------------------------------------------------------

roster = list()
times = list()
gender = 'female' #either female or male
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

#adds every swimmer to roster list with season_id and team that are input
def getRoster(season_id,team):
	file_name = './Roster html/' + gender + '/team-' + team + '_' + 'season_id-' + str(season_id) + '.html' 

	with open(file_name, encoding = 'utf-8') as file:
		soup = bs(file, 'html.parser')

	team = team_names[team] #changes team from number to team name

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:] #finds table of player names

	for row in data:
		webName = row.find('a').text.strip()
		name = cleanName(webName)
		idArray = row.find_all('a') 				 #returns array of length 1 which contains swimmer ID 
		swimmer_id = getSwimmerID(idArray[0]['href'])	
		numbers = row.find_all('td')
		hometown = getState(numbers[2].text.strip())
		grade = numbers[3].text.strip()
		start = getStart(season_id,grade)
		power_index = getPowerIndex(name, swimmer_id)
		if(not containsPlayer(swimmer_id)):
			roster.append({'name': name, 'webName' : webName,'swimmer_id' : swimmer_id,'team' : team,'hometown' : hometown,'power_index' : power_index, 'start' : start, 'FR': '', 'Events-FR' : '', 'SO' : '', 'Events-SO' : '', 'JR' : '', 'Events-JR' : '', 'SR' : '', 'Events-SR' : ''})

#checks if swimmer is already in roster
def containsPlayer(swimmer_id):
	for i in range(len(roster)):
		if(roster[i]['swimmer_id'] == swimmer_id):
			return True
	return False

#extracts swimmer id from href
def getSwimmerID(href):
	return href.split('/')[-1]

#extracts state or country from hometown
def getState(hometown):
	home = hometown.split(',')[-1].strip()
	if(home.isalpha()):
		return home
	else:
		return 'NONE'

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last = nameList[0]
	first_middle = nameList[1].split(' ')
	first = first_middle[0]
	return first + ' ' + last

#finds index of swimmer in roster
def playerIndex(swimmer_id):
	for i in range(len(roster)):
		if(roster[i]['swimmer_id'] == swimmer_id):
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

#returns array (impIndex, eventTypeIndex) that has the correct indexes for where to find improvement percentage and event type in html table
def numbersIndexes(numbers):
	impIndex = -1
	eventTypeIndex = -1
	indexes = []

	for i in range(len(numbers)):
		if(numbers[i].find('span', attrs = {'class' : 'u-color-success'}) or numbers[i].find('span', attrs = {'class' : 'u-color-danger'})):
			impIndex = i
		if(numbers[i].text.strip() == 'Prelims' or numbers[i].text.strip() == 'Timed Finals' or numbers[i].text.strip() == 'Finals'):
			eventTypeIndex = i

	indexes.append(impIndex)
	indexes.append(eventTypeIndex)

	return indexes

#gets data for how many points swimmers scored in acc championship meet
def getData(team,meet):
	file_name = './Data html/' + gender + '/meet_id-' + meet + '_' + 'team-' + team + '.html'  

	getPoints(file_name)

	#check if page 2

	file_name = './Data html/' + gender + '/meet_id-' + meet + '_' + 'team-' + team + '-page2.html'  

	if(os.path.isfile(file_name)):
		#print('page 2')
		getPoints(file_name)
	else:
		#print('NO page 2')

def getPoints(file_name):
	with open(file_name, encoding = 'utf-8') as file:
		soup = bs(file, 'html.parser')

	data = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:]

	year = soup.find('title').text.strip()[0:4] 

	season_id = int(year) - 1997
	
	for row in data: 
		links = row.find_all('a')
		swimmer_id = getSwimmerID(links[0]['href'])

		numbers = row.find_all('td')
		points = numbers[5].text.strip()
		if(points == '–'): 
			points = '0'

		entries = findEntries(links[1]['href'], swimmer_id) #finds how many events a swimmer did on a different html page using the href from links[1]
		index = playerIndex(swimmer_id)
		grade = playerGrade(season_id, index)

		key = 'Events-' + grade

		roster[index][key] = entries
		roster[index][grade] = points


#returns power index for a swimmer
def getPowerIndex(name, swimmer_id):
	cleanName = name.replace(' ', '+')
	file_name = './Recruiting html/' + gender + "/" + cleanName + '.html'  

	with open(file_name, encoding ='utf-8') as file:
		soup = bs(file, 'html.parser')

	powerIndexArray = soup.find_all('td', attrs = {'class' : 'u-text-end'})  
	swimmerIdArray = soup.find_all('a', attrs = {'class' : 'u-text-semi'})
	swimmerIndex = -1
	index = 0
	swimmerCheck = False

	if(len(swimmerIdArray) == 0):  #if no data
		return '-1'

	for swimmer in swimmerIdArray:
		if getSwimmerID(swimmer['href']) == swimmer_id:
			swimmerIndex = index
			swimmerCheck = True   #if still false then there is no data for swimmer
		else:
			index += 1

	if(swimmerCheck == False):
		return '-1'

	if(swimmerIndex != -1):
		return powerIndexArray[swimmerIndex].text.strip()

#returns number of events a swimmer participated in  ;  adds to times list 
def findEntries(link, swimmer_id):
	index = playerIndex(swimmer_id)
	team = roster[index]['team']
	name = roster[index]['name']
	
	link = link.replace('/', '-')

	file_name = './Entries html/' + gender + "/" + link + '.html'  

	with open(file_name, encoding ='utf-8') as file:
		soup = bs(file,'html.parser')

	data = soup.find('ul', attrs = {'class' : 'c-splash-stats'}).find_all('div')

	events = soup.find('table', attrs = {'class' : 'c-table-clean c-table-clean--middle table table-hover'}).find_all('tr')[1:] 

	year = soup.find('title').text.strip()[0:4] 

	for row in events:
		numbers = row.find_all('td')
		swim_type = 'swim'               #set to either swim or dive
		event = numbers[0].text.strip()
		time = numbers[1].find('a').text.strip()

		if(event[-6:] == 'Diving' or event[-6:] == 'dives)'):            #if diving event 
			event_type = numbers[3].text.strip()
			swim_type = 'dive'
			imp = 'NA'

		indexes = numbersIndexes(numbers)

		if(indexes[0] != -1):
			imp = numbers[indexes[0]].find('span').text.strip()
		else:
			imp = 'NA'

		if(indexes[1] != -1):
			event_type = numbers[indexes[1]].text.strip()
		else:
			event_type = 'NA'
		
		times.append({'name' : name, 'swimmer_id' : swimmer_id, 'team' : team, 'year': year, 'event' : event, 'event_type' : event_type, 'swim_type' : swim_type, 'time' : time, 'improvement' : imp})

	if(data[5].text.strip() != '0'):
		return data[5].text.strip()
	else:  
		entries = 0 
		for row in events:
			numbers = row.find_all('td')				#gets correct number of entries for divers who are listed with 0 entries
			if(numbers[3].text.strip() == 'Prelims'):   #not 100% sure yet if this gets the correct number of entries for a swimmer when it is not listed on swimcloud 
				entries += 1
		return entries

#returns array of swimmer's points per event (ppe) for each year- [freshman ppe, sophomore ppe, junior ppe, senior ppe, total points, total events,total ppe]
def getPPE(i):
	ppe = []
	freshman_points = 0
	freshman_events = 0
	freshman_ppe = 0
	sophomore_points = 0
	sophomore_events = 0
	sophomore_ppe = 0
	junior_points = 0
	junior_events = 0
	junior_ppe = 0
	senior_points = 0
	senior_events = 0
	senior_ppe = 0
	total_points = 0
	total_events = 0
	total_ppe = 0
 

	if(roster[i]['FR'].isdigit()):
		total_points += int(roster[i]['FR'])
		total_events += int(roster[i]['Events-FR'])
		freshman_points += int(roster[i]['FR'])
		freshman_events += int(roster[i]['Events-FR'])
	if(roster[i]['SO'].isdigit()):
		total_points += int(roster[i]['SO'])  
		total_events += int(roster[i]['Events-SO'])
		sophomore_points += int(roster[i]['SO'])
		sophomore_events += int(roster[i]['Events-SO'])       
	if(roster[i]['JR'].isdigit()):
		total_points += int(roster[i]['JR'])
		total_events += int(roster[i]['Events-JR'])
		junior_points += int(roster[i]['JR'])
		junior_events += int(roster[i]['Events-JR'])
	if(roster[i]['SR'].isdigit()):
		total_points += int(roster[i]['SR'])
		total_events += int(roster[i]['Events-SR'])
		senior_points += int(roster[i]['SR'])
		senior_events += int(roster[i]['Events-SR'])

	if(freshman_events != 0):
		freshman_ppe = freshman_points / freshman_events 
	else: 
		freshman_ppe = 0

	if(sophomore_events != 0):
		sophomore_ppe = sophomore_points / sophomore_events 
	else: 
		sophomore_ppe = 0

	if(junior_events != 0):
		junior_ppe = junior_points / junior_events 
	else: 
		junior_ppe = 0

	if(senior_events != 0):
		senior_ppe = senior_points / senior_events 
	else: 
		senior_ppe = 0

	if(total_events != 0):
		total_ppe = total_points / total_events
	else :	
		total_ppe = 0

	ppe.append(freshman_ppe)
	ppe.append(sophomore_ppe)
	ppe.append(junior_ppe)
	ppe.append(senior_ppe)
	ppe.append(total_points)
	ppe.append(total_events)
	ppe.append(total_ppe)

	return ppe


def callRoster(team):
	for i in range(7):
		start = 17 + i  #starts at 17 which corresponds to the season_id on swimcloud for the 2013-14 season
		getRoster(start,team) 

def callData(team):
	for meet in meetsToUse: 
		if((team == '174' and meet == '22373') or (team == '174' and meet == '22396')):
			print('') #louisville was not in acc for this year
		else:	
			getData(team,meet)

def rosterToCsv():
	file_name = 'swimmers_' + gender + '_data.csv'
	file = open(file_name,'w', newline = '', encoding ='utf-8')  
	writer = csv.writer(file)

	writer.writerow(['Name','Team','Swimmer_ID','hometown','Starting season','Power_Index','FR','Events-FR','Freshman_PPE', 'SO','Events-SO','Sophomore_PPE','JR','Events-JR','Junior_PPE','SR','Events-SR','Senior_PPE','Total_Points','Total_Events','Total_ppe']) #TOP ROW ON EXCEL SHEET

	for i in range(len(roster)):
		ppeArray = getPPE(i)  #ppeArray[freshman_ppe, sophomore_ppe, junior_ppe, senior_ppe, total_points, total_events, total_ppe]

		writer.writerow([roster[i]['name'], roster[i]['team'], roster[i]['swimmer_id'], roster[i]['hometown'], roster[i]['start'],roster[i]['power_index'],roster[i]['FR'],roster[i]['Events-FR'],ppeArray[0],roster[i]['SO'],roster[i]['Events-SO'],ppeArray[1],roster[i]['JR'],roster[i]['Events-JR'],ppeArray[2],roster[i]['SR'],roster[i]['Events-SR'],ppeArray[3],ppeArray[4], ppeArray[5],ppeArray[6]])

	file.close()

def rosterBasicDataToCsv():
	file_name = 'swimmers_' + gender + '_infoNEW.csv'
	file = open(file_name,'w', newline = '', encoding ='utf-8')  
	writer = csv.writer(file)

	writer.writerow(['Name','Team','Swimmer_ID','Hometown'])

	for i in range(len(roster)):
		writer.writerow([roster[i]['name'], roster[i]['team'], roster[i]['swimmer_id'], roster[i]['hometown']])

	file.close()

def timesDataToCsv():
	file_name = 'swimmers_' + gender + '_times.csv'
	file = open('swimmers_female_times.csv', 'w', newline ='', encoding = 'utf-8')

	writer = csv.writer(file)

	writer.writerow(['Name', 'Swimmer_ID', 'Team', 'Year', 'Event', 'Event_Type', 'swim_type', 'Time', 'Improvement'])

	for i in range(len(times)):
		writer.writerow([times[i]['name'], times[i]['swimmer_id'], times[i]['team'], times[i]['year'], times[i]['event'], times[i]['event_type'], times[i]['swim_type'], times[i]['time'], times[i]['improvement']])

	file.close()



#MAIN --------------------------------------------------------------------------------------
if(gender == 'female'):
	meetsToUse = meets_female
else:
	meetsToUse = meets_male

for team in teams:
	callRoster(team)

for team in teams:
	callData(team)

#only call one at a time ------------------------------------------------------

#rosterToCsv()         			#call this for basic swimmer info as well as power index, points scored and number of events at the ACC championship meet
rosterBasicDataToCsv()     	#call this for basic swimmer info (name, team, swimmer_id, hometown)
#timesDataToCsv() 			    #call this for info on swimmers times and how they improved their times at the ACC championship meet (improvement(%))



