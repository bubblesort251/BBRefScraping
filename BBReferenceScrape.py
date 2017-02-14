import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from collections import OrderedDict

# Quick directories work
path = 'NBA_Monthly_Schedules'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

# Find a base form of the url to use
baseurl = 'http://www.basketball-reference.com/leagues/NBA_2017_'

# Create a dictory of keys and values to use with a for loop to create the url
# that you want to get data from
months = OrderedDict([('oct', 'games.html'), ('nov', 'games-november.html'), 
                      ('dec', 'games-december.html'), ('jan', 'games-january.html'), 
                      ('feb', 'games-february.html'), ('mar', 'games-march.html'), 
                      ('apr', 'games-april.html')])

os.chdir(path)

# Use the xlsxwriter to create an excel file with each sheet being a month
writer = pd.ExcelWriter('NBA_Schedule_16-17.xlsx', engine='xlsxwriter')

# Create a for loop that iterates over the months dictionary and gets schedules
for key, value in months.items():
    url = baseurl + value    
    response = requests.get(url)
    html = response.content
    
    soup = BeautifulSoup(html,"lxml")
    
    table = soup.find('table', attrs={'class': "suppress_glossary sortable stats_table"})
    
    list_of_rows = []
    for row in table.findAll('tr'):
    	list_of_cells = []
    	for cell in row.findAll('th'):
    		text = cell.text
    		list_of_cells.append(text)
    	for cell in row.findAll('td'):
    		text = cell.text
    		list_of_cells.append(text)
    	list_of_rows.append(list_of_cells)
    
    list_of_rows2 = []
    for row in list_of_rows:
    	r = row[:6]
    	list_of_rows2.append(r)
        
    
    frames = {}
    monthslist = list(months.keys())
    m = key
    df = pd.DataFrame(data=list_of_rows2, dtype=str)
    df.to_csv('nba_' + key + '_schedule.csv', header=None, index=False)
    frames[m] = df
    
    for sheet, frame in frames.items():
        frame.to_excel(writer, sheet_name = sheet, header=None, index=False)

writer.save()
