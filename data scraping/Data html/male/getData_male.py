import requests
import csv
from bs4 import BeautifulSoup as bs

teams = ['228','280','77','34','394','425','60','53','405','73','336','174']
meets_male = ['22396','28738','51300','76429','104707','118535','166310']
page2check = list()

def callData(team, page):
	for index, meet in enumerate(meets_male):  
		if(page == '2' and page2check[index] == 0):
			print('NO PAGE 2')
		else:
			url = 'https://www.swimcloud.com/results/' + meet + '/team/' + team + '/swimmers/?page=' + page  
			if(team == '174' and meet == '22396'): 
				print('') #louisville was not in acc for this year
				page2check.append(0)
			else:
				saveData(url, meet, team, page)

def saveData(link, meet, team, page):
	if(page == '1'):
		url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

		url.encoding = 'utf-8'

		soup = bs(url.text, 'html.parser')

		name = 'meet_id-' + meet + '_' + 'team-' + team + '.html'

		if(soup.find('ul', attrs = {'class' : 'c-pagination'})): 
			page2check.append(1)
		else:
			page2check.append(0)

		with open(name, 'w', encoding = 'utf-8') as file:
			file.write(url.text)
	if(page == '2'):
		url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

		url.encoding = 'utf-8'

		name = 'meet_id-' + meet + '_' + 'team-' + team + '-page2.html'

		with open(name, 'w', encoding = 'utf-8') as file:
			file.write(url.text)

for team in teams:
	callData(team, '1')
	print(page2check)
	callData(team, '2')
	page2check.clear()



