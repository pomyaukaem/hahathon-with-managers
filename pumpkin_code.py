# -*- coding: utf-8 -*-
"""pumpkin_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17k2z1dmm7-imVo-r7gUA_ObA6CtVSr41
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

pmpkn_data = pd.read_csv('pumpkins.csv')

for n in pmpkn_data.index:
  if "Entries" in pmpkn_data['weight_lbs'][n]:
    pmpkn_data = pmpkn_data.drop([n])

for n in pmpkn_data.index:
  if "," in pmpkn_data['weight_lbs'][n]:
    pmpkn_data = pmpkn_data.drop([n])

pmpkn_data['weight_lbs'] = pmpkn_data['weight_lbs'].apply(lambda x: float(x))

data_countries = pmpkn_data['country'].value_counts().reset_index(name='Counts')
average_countries = []
for index_country in list(data_countries['index']):
  average_countries.append(sum(list(pmpkn_data[pmpkn_data['country'] == index_country]['weight_lbs']))/len(list(pmpkn_data[pmpkn_data['country'] == index_country]['weight_lbs'])))
data_countries['average'] = average_countries
data_countries.rename(columns = {'index' : 'Country', 'Counts' : 'Number of pumpkins'}, inplace = True)

sns.set(font_scale=1, font = 'serif') 
sns.barplot(data = data_countries, y='Country', x='Number of pumpkins')
plt.savefig('table1.png', bbox_inches = 'tight')

us_geo = pd.read_csv('US.zip', delimiter='\t')

us = pmpkn_data[pmpkn_data['country'] == 'United States']
us['city'] = us['city'].apply(lambda x: str(x))
us['city'] = us['city'].apply(lambda x: x.title())
us_cities = us['city'].value_counts().reset_index(name='Counts')
us_cities_latitude = dict.fromkeys(us_cities['index'], '')

for n in us_geo.index:
  if us_geo['Middle Reef'][n] in us_cities_latitude:
    us_cities_latitude[us_geo['Middle Reef'][n]] = us_geo['51.98414'][n]

us_cities['latitude'] = list(us_cities_latitude.values())
average_us_cities = []
for n in us_cities.index:
  average_us_cities.append(sum(list(us[us['city'] == us_cities['index'][n]]['weight_lbs']))/len(list(us[us['city'] == us_cities['index'][n]]['weight_lbs'])))
us_cities['average'] = average_us_cities

us_cities['country'] = 'US'

ca_geo = pd.read_csv('CA.zip', delimiter='\t')
ca = pmpkn_data[pmpkn_data['country'] == 'Canada']
ca['city'] = ca['city'].apply(lambda x: str(x))
ca['city'] = ca['city'].apply(lambda x: x.title())
ca_cities = ca['city'].value_counts().reset_index(name='Counts')
ca_cities_latitude = dict.fromkeys(ca_cities['index'], '')

for n in ca_geo.index:
  if ca_geo['Virgin Rocks'][n] in ca_cities_latitude:
    ca_cities_latitude[ca_geo['Virgin Rocks'][n]] = ca_geo['46.42886'][n]

ca_cities['latitude'] = list(ca_cities_latitude.values())
average_ca_cities = []
for n in ca_cities.index:
  average_ca_cities.append(sum(list(ca[ca['city'] == ca_cities['index'][n]]['weight_lbs']))/len(list(ca[ca['city'] == ca_cities['index'][n]]['weight_lbs'])))
ca_cities['average'] = average_ca_cities
ca_cities['country'] = 'Canada'

cities = pd.concat([ca_cities, us_cities], axis=0)
cities = cities.reset_index()
for n in cities.index:
  if cities['latitude'][n] == '':
    cities = cities.drop([n])

plt.rcParams.update({'font.family':'serif'})
fig = plt.figure(figsize=(16, 10), dpi= 80)
grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)
ax_main = fig.add_subplot(grid[:-1, :-1])

ax_main.scatter('average', 'latitude', alpha=.9, data=cities, cmap="tab10", edgecolors='gray', color='orange', linewidths=.5)

ax_main.set(title='''The average weight of BIG pumpkins per city in the USA and Canada\n depending on city's geographical latitude''', xlabel='The average weight per city', ylabel='Geographical latitude in the northern hemisphere\n (larger number = more nourthern city)')
ax_main.title.set_fontsize(18)
for item in ([ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
    item.set_fontsize(12)

plt.savefig('table2.png')