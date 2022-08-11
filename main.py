#!/bin/python3
import requests
from bs4 import BeautifulSoup
import csv
import re
import os.path

first_page = 201001539 #Начальная страница для интервала опроса
last_page = 201600000  #Конечная страница для интервала опроса
pages = [i for i in range(first_page, last_page)]
export_filename = f'export-{first_page}.csv'
base_url = "https://kinescope.io/embed/"
export = {
    'provider': '', 
    'URL': '',
    'course': '',
    'webinar_date': '',
    'webinar_duration': '',
    'webinare_title': '',
    }

if not os.path.exists(export_filename):
    with open(export_filename, 'a', encoding='utf-8') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, export.keys(),delimiter='\t')
        w.writeheader()

for page in pages:
    url = base_url + str(page)
    response = requests.get(url)
    tmp_dict = {}
    retext = response.text.find("<title>Access forbidden</title>") 
    tennchat = response.text.find("<title>tenchat-user-story</title>")
    if response.status_code == 200 and retext == -1 and tennchat == -1:    
        tmp_dict = {}
        soup = BeautifulSoup(response.text, 'lxml')
        tag_script = soup.find('script', {'type': 'application/ld+json'})
        if tag_script != None:
            description = str(tag_script.contents[0]).replace('\n','').replace('{','').replace('}','').lstrip()
            results = description.split(',  ')
            for result in results:
                a = result.split(': ')
                if len(a)>1:
                    tmp_dict.setdefault((a[0].rstrip()).lstrip().replace('"',''), (a[1].rstrip()).lstrip().replace('"',''))
                # else:
                #     tmp_dict.setdefault((a[0].rstrip()).lstrip().replace('"',''), (a[0].rstrip()).lstrip().replace('"',''))

            m = re.findall(r'\w*[-]\d\d?', tmp_dict['name'] )
            provider = 'Other'
            course = 'Other'
            if m:
                provider = 'Netology'
                course = m[0]

            export = {
                'provider': provider, 
                'URL': url,
                'course': course,
                'webinar_date': tmp_dict['uploadDate'],
                'webinar_duration': tmp_dict['duration'],
                'webinare_title': tmp_dict['name'],
                }

            with open(export_filename, 'a', encoding='utf-8') as f:  # You will need 'wb' mode in Python 2.x
                w = csv.DictWriter(f, export.keys(),delimiter='\t')
                w.writerow(export)
            print(url)

        