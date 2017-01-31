import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.basketball-reference.com/leagues/NBA_2017_games.html'
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

with open("./octoberGames.csv", "wb") as outfile:
	writer = csv.writer(outfile)
	writer.writerows(list_of_rows2)