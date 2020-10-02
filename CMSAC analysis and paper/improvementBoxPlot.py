import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import warnings
import statistics

warnings.simplefilter(action='ignore', category=FutureWarning)

data = pd.read_csv('../data scraping/swimmers_female_times.csv') #male or female

BC = []
DU = []
FSU = []
GIT = []
NCST = []
UM = []
UNC = []
UND = []
UP = []
UV =[]
VT = []
UL = []

def addImprovement(Team, imp):
	if(Team == 'Boston College'):
		BC.append(imp)
	elif(Team == 'Duke University'):
		DU.append(imp)
	elif(Team == 'Florida State University'):
		FSU.append(imp)
	elif(Team == 'Georgia Institute of Technology'):
		GIT.append(imp)
	elif(Team == 'North Carolina State University'):
		NCST.append(imp)
	elif(Team == 'University of Miami (Florida)'):
		UM.append(imp)
	elif(Team == 'University of North Carolina, Chapel Hill'):
		UNC.append(imp)
	elif(Team == 'University of Notre Dame'):
		UND.append(imp)
	elif(Team == 'University of Pittsburgh'):
		UP.append(imp)
	elif(Team == 'University of Virginia'):
		UV.append(imp)
	elif(Team == 'Virginia Tech'):
		VT.append(imp)
	elif(Team == 'University of Louisville'):
		UL.append(imp)
	else: 
		print('Error: no team')

def playerImprovement(swimmer_id):
	imps = []
	events = []
	colors = []
	diveCheck = False
	dive = ''
	#title = 'Swimmer ID: ' + str(swimmer_id)

	for index, row in data.iterrows():
		if row['Swimmer_ID'] == swimmer_id:
			name = row['Name']
			if(row['swim_type'] == 'dive' and diveCheck == False):
				dive = ' - Diver'
				diveCheck = True
			if(isinstance(row['Improvement'],float)):
				print('NA')
			else:
				imp = float(row['Improvement'][:-1])

				if(imp > 0):
					colors.append('g')
				else:
					colors.append('r')

				imps.append(imp)
				ev = str(row['Year']) + ' ' + row['Event'] + ' ' + row['Event_Type']
				events.append(ev)

	title = 'Name: ' + name + dive

	plt.title(title)
	plt.bar(events, imps, color = colors)
	plt.ylabel('Percent Improvement')
	plt.xticks(rotation = 20)
	plt.show()

def compareTeamBoxPlot():
	for index, row in data.iterrows():
		if(isinstance(row['Improvement'],float)):
			print('')
		else:
			imp = float((row['Improvement'][:-1])) 		#removes % from number 
			addImprovement(row['Team'], imp)

	plt.boxplot([BC,DU,FSU,GIT,NCST,UM,UNC,UND,UP,UV,VT,UL], vert = False)
	plt.title('ACC improvement - Female')
	plt.xlabel('Improvement by percentage')
	plt.yticks([1,2,3,4,5,6,7,8,9,10,11,12],['Boston College','Duke University','Florida State University', 'Georgia Institute of Technology', 'NC State', 'University of Miami', 'University of North Carolina', 'University of Notre Dame','University of Pittsburgh','University of Virginia','Virginia Tech','University of Louisville'], rotation = 40)
	plt.show()


compareTeamBoxPlot()
#playerImprovement(433591) #put in swimmer_id of desired swimmer 