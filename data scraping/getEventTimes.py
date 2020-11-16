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
male_roster = pd.read_csv('https://raw.githubusercontent.com/maflancer/ACC-Swimming-Data/master/data%20scraping/swimmers_male_info.csv')

pitt_roster = male_roster[male_roster['Team'] == 'University of Pittsburgh'] #set to only Pitt swimmers

def addTimes(swimmer_ID, event_ID):

	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'
	dropdownCheck = True
	eventCheck = True

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	for tab in tabs:
		if(tab.text == 'Event'): 
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList')))
		event_dropdown.click()
	except TimeoutException: #if there is no event drop down
		dropdownCheck = False

	if dropdownCheck:

		swimmer_XPATH = '//a[@href="/swimmer/' + str(swimmer_ID)  + '/times/byevent/?event_id=' +  str(event_ID) + '"]'

		print(swimmer_XPATH)

		try: 
			event = wait.until(EC.presence_of_element_located((By.XPATH, swimmer_XPATH)))
			event.click()
		except TimeoutException: #if a swimmer does not have the event listed in the dropdown
			eventCheck = False
			print(swimmer_ID)

		if eventCheck:

			_time.sleep(1)

			html = driver.page_source

			soup = bs(html, 'html.parser')

			table = soup.find('table', attrs = {'class' : 'c-table-clean'})

			times = table.find_all('tr')[1:]

			for time in times:
				data = time.find_all('td')

				if(len(data) > 2):
					meet = data[2].text.strip()
				else:
					meet = 'NA'
				if(len(data) > 3):
					date = data[3].text.strip()
					year = data[3].text.strip().split(',')[-1].strip()
				else:
					date = 'NA'
					year = 'NA'
				if(len(data) > 4):
					imp = data[4].text.strip()
				else:
					imp = 'NA'

				time_list.append({'Swimmer_ID' : swimmer_ID, 'Time' : data[0].text.strip(), 'Meet' : meet, 'Year' : year, 'Date' : date, 'Imp' : imp})


#add times for all pitt swimmers 
for index, row in pitt_roster.iterrows():
	addTimes(row['Swimmer_ID'], 1100)     #1100 for 100 free

#test one swimmer 
#addTimes(172052, 1100)


file_name = 'PITT_100FREE_TIMES.csv'

file = open(file_name,'w', newline = '', encoding ='utf-8')  
	
writer = csv.writer(file)

writer.writerow(['Swimmer_ID','Time','Meet','Year','Date','Imp'])

for i in range(len(time_list)):
	writer.writerow([time_list[i]['Swimmer_ID'], time_list[i]['Time'], time_list[i]['Meet'], time_list[i]['Year'], time_list[i]['Date'], time_list[i]['Imp']])

file.close()








