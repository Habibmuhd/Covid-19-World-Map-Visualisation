import json
import folium
import requests
import mimetypes
import http.client
import pandas as pd
from folium.plugins import HeatMap
from pandas.io.json import json_normalize
import webbrowser

conn = http.client.HTTPSConnection('api.covid19api.com')
payload = '' #to store incoming data
headers = {} #store
conn.request('GET',"/summary",payload,headers)
res = conn.getresponse()
data = res.read().decode('UTF-8')
covid1=json.loads(data)

pd.json_normalize(covid1['Countries'],sep=",") #json to pd dataframe
df = pd.DataFrame(covid1['Countries']) #create pandas dataframe
print (list(df.columns)) #check headers
covid2 = df.drop(columns=['CountryCode', 'Slug', 'Date', 'Premium'],axis =1) #drop columns that are not impt for this project
print(covid2)

#using folium to generate map
m=folium.Map(tiles="Stamen Terrain",min_zoom=1.5)
#m.save('covid.html')

def auto_open(path):   #to auto open map in your browser
    html_page = f'{path}'
    # open in browser.
    new = 2
    webbrowser.open(html_page, new=new)

    
auto_open('covid.html')


url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'

folium.Choropleth (geo_data= country_shapes,
                   min_zoom=2,
                   name='Covid-19 data',
                   data=covid2,
                   columns =["Country", 'TotalConfirmed'],
                   key_on='feature.properties.name',
                   fill_color='YlGn',
                   nan_fill_color='black',
                   legend_name='Total Confirmed Covid Cases',
                    ).add_to(m)

m.save('covid.html')
