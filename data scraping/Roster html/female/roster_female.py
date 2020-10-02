import requests
import csv
from bs4 import BeautifulSoup as bs

teams = ['228','280','77','34','394','425','60','53','405','73','336','174']


def callRoster(team):
	for i in range(7):
		start = str(17 + i)   #starts at 17 which corresponds to the season_id on swimcloud for the 2013-14 season
		url = 'https://www.swimcloud.com/team/' + team + '/roster/?page=1&gender=F&season_id=' + start #for male change gender=M or for female, gender=F
		saveRoster(url,start,team) 

def saveRoster(link,season_id,team):
	url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	name = 'team-' + team + '_' + 'season_id-' + season_id + '.html'
	with open(name,'w',encoding='utf-8') as file:
		file.write(url.text)

for team in teams:
	callRoster(team)