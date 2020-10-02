# ACC-Swimming-Data

## CMSAC analysis and paper
CMSAC20_swimming.pdf - paper

improvementBoxPlot.py - produces boxplot used in paper

swimming.ipynb - analysis notebook


## heroku app 
main.py - this is the main python file used to run the interactive application at https://accswimming.herokuapp.com/

data - the four .csv files that are used in main.py

## data scraping
this folder has the scripts that can be used to download html files from swimcloud.com - the html files downloaded are then scraped in data.py which has three different csv files that can be produced - 

1. swimmers_male_info.csv and

   swimmers_female_info.csv - includes swimmer names, swimmer ID, team, and hometown
   
2. swimmers_male_data.csv and

   swimmers_female_data.csv - includes:information for the points contributed to their team by each swimmer, in each of their seasons
                            -          information about the  number of points each swimmer earned for  their  team  during  each  season (freshmen,sophomore, junior and senior) 
                            -          the number of events they participated in each of these seasons along with the points per event (PPE). 
                            -          the PowerIndex which is an indicator of their high school recruiting rank. 

3. swimmers_male_times.csv and

   swimmers_female_times.csv - includes the times of each swimmer at different events from the ACC finals (2013 - 2020)
   
-------------------------------------------------------------------------------------------------------------------------------

Steps to download the html files necessary to run data.py - these steps should be able to output the csv files specified above

1. Run, in the Roster html folder, roster_male.py (in the male folder) and roster_female.py (in the female folder). These scripts are currently hard coded to get, from swimcloud.com, the rosters from 2013 - present for the 12 ACC teams that currently participate in the ACC Swimming and Diving Finals each season. This will be updated in the future to take teams as an input so you can get data for any college swimming team

2. Run, in the Data html folder, getData_male.py (in the male folder) and getData_female.py (in the female folder). These scripts are currently hard coded with the same teams as in step 1, and they are also hardcoded with meet ids which correspond with the ACC Championship meets from 2013-2020 on swimcloud.com. This will also be updated in the future to take teams and meets as an input.

3. Run, in the Entries html folder, entries_male.py (in the male folder) and entries_female.py (in the female folder). These scripts are currently hard coded with team and meet ids. The scripts currently are hard coded to use the html files that were downloaded in step 2 from the Data html folder to get the data that is used to download the html files from swimcloud.com with entry data. 

4. Run, in the Recruiting html folder, recruiting_male.py (in the male folder) and recruiting_female.py (in the female folder). These scripts are currently hard coded to use the names in swimmers_male_info.csv and swimmers_female_info.csv to download the html files from swimcloud.com that include the data for a swimmer's high school power index. This will be updated to take teams as input.

5. Run data.py - this is currently hard coded to get the data from the female html folders (this will be updated to take gender as an input) - if you want to change the script to get male data you will have to change the lines of code at line 32, 133, 139, 179, 214, 343, 344, 350, 363, 374 (all you will have to change is the word female to the word male at these lines).
               - After you have chosen if you want to get male or female data, you should go the bottom of the script where there are three function calls - rosterToCsv(), rosterBasicDataToCsv(), and timesDataToCsv(). Comment and uncomment out which functions you want to run and do not want to run. These functions will output the three csv files specified earlier. 



