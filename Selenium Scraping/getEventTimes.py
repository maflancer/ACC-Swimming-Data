import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import time as _time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

#set driver options
chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver.exe', options = chrome_options)

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

time_list = list() 

#list of all acc swimmer names 
male_roster = pd.read_csv('https://raw.githubusercontent.com/maflancer/ACC-Swimming-Data/master/data%20scraping/swimmers_male_info.csv')
#set to only Pitt swimmers
pitt_roster = male_roster[male_roster['Team'] == 'University of Pittsburgh'] 

#for data from a html table (data), find the indexes where meet name, date, year, and improvement are
#returns an array [meet_name_index, date_index, imp_index]
def getIndexes(data):
	meet_name_index = -1;
	date_index = -1;
	imp_index = -1;
	indexes = []

	i = 0
	for td in data:
		if td.has_attr('class') and td['class'][0] == 'hidden-xs':
			meet_name_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-truncate':
			date_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-end':
			imp_index = i

		i = i + 1

	indexes.append(meet_name_index);
	indexes.append(date_index);
	indexes.append(imp_index);

	return indexes;


#For a specified swimmer (swimmer_ID), adds all of their individual times for a specified event (event_ID) to the time_list
def addTimes(swimmer_ID, event_ID):

	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'
	dropdownCheck = True
	eventCheck = True

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website 

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'Event'): 
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList'))) #waits for the event drop down list to show up
		event_dropdown.click()
	except TimeoutException: #if there is no event drop down
		dropdownCheck = False

	if dropdownCheck:

		swimmer_XPATH = '//a[@href="/swimmer/' + str(swimmer_ID)  + '/times/byevent/?event_id=' +  str(event_ID) + '"]'

		print(swimmer_XPATH) #debug

		try: 
			event = wait.until(EC.presence_of_element_located((By.XPATH, swimmer_XPATH)))
			event.click()
		except TimeoutException: #if a swimmer does not have the event listed in the dropdown
			eventCheck = False
			print(swimmer_ID)

		if eventCheck: #if the event is listed

			_time.sleep(1)

			html = driver.page_source

			soup = bs(html, 'html.parser')

			table = soup.find('table', attrs = {'class' : 'c-table-clean'})

			try:
				times = table.find_all('tr')[1:]
			except AttributeError:
				times = []

			for time in times:
				data = time.find_all('td')

				indexes = getIndexes(data) #this function finds the correct indexes for the meet name, date, year, and improvement, as they are different for some swimmers

				time = data[0].text.strip() 

				if(indexes[0] == -1): #if no meet name was found
					meet = 'NA'
				else:
					meet = data[indexes[0]].text.strip()

				if(indexes[1] == -1): #if no date was found
					date = 'NA'
					year = 'NA'
				else:
					date = data[indexes[1]].text.strip()
					year = date.split(',')[-1]
				
				if(indexes[2] == -1): #if no imp was found
					imp = 'NA'
				else:
					imp = data[indexes[2]].text.strip()

				if(imp == '–'): #this character gets encoded weird in an excel doc so just set to NA
					imp = 'NA'

				time_list.append({'Swimmer_ID' : swimmer_ID, 'Time' : time, 'Meet' : meet, 'Year' : year, 'Date' : date, 'Imp' : imp})



#_______________________________________MAIN__________________________________________________________________________


#add times for all pitt swimmers 
for index, row in pitt_roster.iterrows():
	addTimes(row['Swimmer_ID'], 1100)     #1100 for 100 free

#test swimmers
#addTimes(172052, 1100)
#addTimes(362091, 1100)

file_name = 'PITT_100_FREE.csv'  

file = open(file_name,'w', newline = '', encoding ='utf-8')  
	
writer = csv.writer(file)

writer.writerow(['Swimmer_ID','Time','Meet','Year','Date','Imp'])

for i in range(len(time_list)):
	writer.writerow([time_list[i]['Swimmer_ID'], time_list[i]['Time'], time_list[i]['Meet'], time_list[i]['Year'], time_list[i]['Date'], time_list[i]['Imp']])

file.close()








