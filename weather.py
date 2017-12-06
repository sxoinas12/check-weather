# -*- coding: utf-8 -*-
import os.path
import re
import urllib.request
import urllib.error
import time



url = "http://www.meteo.gr/rss/news.cfm"
dir_name = 'my_forecasts'
forecast_dir = os.path.join(os.getcwd(),dir_name)

if not os.path.isdir(forecast_dir):
    os.mkdir(forecast_dir)

def find_tags(tag,st):
    tags = re.findall(r'<' +tag + r'\b[^>]*>(.*?)</'+ tag + r'>' ,st ,re.I)
    return tags

def extract_date(st):
    date = st.split()[-1]
    if re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}',date):
        date = date.split('/')
        date.reverse()
        date = '_'.join(date)
        print(date)
        return date



###main program

    
if not os.path.isdir(forecast_dir):
    os.mkdir(forecast_dir)

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        char_set = response.headers.get_content_charset()
        rss = response.read().decode(char_set)
        print(rss)
except urllib.error.URLError as e:
    print("cant connect to the server")
    print("Reason:" , e.reason)
except urllib.error.HTTPError as e:
    print("HTTP error",e.code)



else:
    rss = rss.replace('\n', '')
    items = find_tags('item',rss)
    for i in items:
        if 'ΓΕΝΙΚΗ ΠΡΟΓΝΩΣΗ ΓΙΑ:' in i:
            title = find_tags('title',i)[0]
            file_name = extract_date(title)+'.txt'
            forecast = find_tags('description',i)
            print(title, '\n',forecast)
            try:
                with open(os.path.join(forecast_dir,file_name),'w',encoding = 'utf-8') as f:
                    f.write(title+'\n'+forecast[0])
            except IOError as e:
                print(e)
            

