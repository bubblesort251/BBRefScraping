import pandas as pd
import requests
from bs4 import BeautifulSoup

baseurl = 'http://www.basketball-reference.com/leagues/NBA_2017_'
months = {'oct': 'games.html', 'nov': 'games-november.html', 'dec': 'games-december.html',
          'jan': 'games-january.html', 'feb': 'games-february.html',
          'mar': 'games-march.html', 'apr': 'games-april.html'}

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
        
    df = pd.DataFrame(data=list_of_rows2, dtype=str)
    df.to_csv('nba_' + key + '_schedule.csv', header=None, index=False)
