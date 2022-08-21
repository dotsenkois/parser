#!/bin/python3

# Данный скрипт позволяет найти атраницы с видео на сайте kinescope.io

import requests
from bs4 import BeautifulSoup
import csv
import re
import os.path
import json

# файл для записи номера последней успешнообработаной страницы
log_file = '/home/dotsenkois/log.txt'
#Начальная страница для интервала опроса по-умолчанию
first_page = 201383976 

# Если существует файл лога, то номер первой страницы вычитывается из него
if os.path.exists(log_file):
    with open(log_file, 'r') as log:
        data = log.read()
        if data:
            first_page = int(data)

#Конечная страница для интервала опроса
last_page = 201600000
# Генерация списка для работы цикла
pages = [i for i in range(first_page, last_page)]
# Генерация имени файла для сохраннения результатов
export_filename = f'/home/dotsenkois/export.csv'
# Основной домен для перебора адресов
base_url = "https://kinescope.io/embed/"

# Формируем шаблон словаря для экспорта в csv
export = {
    'provider': '',
    'URL': '',
    'course': '',
    'webinar_date': '',
    'webinar_duration': '',
    'webinare_title': '',
    }

# Проверяем наличе файла для экспорта. Если отсуствует, то создаем
if not os.path.exists(export_filename):
    with open(export_filename, 'a', encoding='utf-8') as f:
        w = csv.DictWriter(f, export.keys(),delimiter='\t')
        w.writeheader()

# Основнйо цикл. Перебор адресов из списка
for page in pages:
    # Генерация полного адреса для запроса
    url = base_url + str(page)
    # Запрос
    response = requests.get(url)
    # Создаем пустой временный словарь или очищаем от данных при последующих итерациях
    tmp_dict = {}
    # Ищем в HTML совпадения для того, чтобы исключить обработку страниц
    retext = response.text.find("<title>Access forbidden</title>")
    tennchat = response.text.find("<title>tenchat-user-story</title>")
    # Проверяем статус код и наличие вхождений от поиска: Если статус код 200 и на странце нет вышеуказанного текста, то продолжаем обработку
    if response.status_code == 200 and retext == -1 and tennchat == -1:
        soup = BeautifulSoup(response.text, 'lxml')
        # ищем тег для обработки. Информация берется только из него
        tag_script = soup.find('script', {'type': 'application/ld+json'})
        if tag_script:
            tag_script = tag_script.text.replace('\n', '').replace('\r', '').replace('\t', '').replace('&quot;','').replace('\\','')
            loadedjson =json.loads(tag_script)
            # продолжаем обработку, если tag_script содержит данные
            if loadedjson:
                # Значение переменные provider и course по-умолчанию
                provider = 'Other'
                course = 'Other'
                # проверяем на соотвествие названия вебинара шаблону
                regexp_1 = re.match(r'^[(]?[^0-9]*[-_][a-zA-Z]?[a-zA-Z]?[-_]?\d{1,2}[)]?\b', loadedjson['name'])
                regexp_2 = re.match(r'^\d{4}[-]\d{2}[-]\d{2}[_]{1,2}[a-zA-Z]{2,7}[_]{1,2}\d{1,2}', loadedjson['name'] )

                # Если есть совпаденеи с маской, то менем значение переменных
                if regexp_1:
                    m = regexp_1.group()
                    provider = 'Netology'
                    course = m.replace('(','').replace(')','').replace('_','-')
                    regexp_1 = ''
                elif regexp_2:
                    m = regexp_2.group()
                    provider = 'Netology'
                    course = m[10:].lstrip('_').replace('_','-')
                    regexp_2 = ''

                # формируем словарь для экспорт в csv
                export = {
                    'provider': provider,
                    'URL': url,
                    'course': course,
                    'webinar_date': loadedjson['uploadDate'],
                    'webinar_duration': loadedjson['duration'],
                    'webinare_title': loadedjson['name'],
                    }
                # Дозаписываем данные в файл
                with open(export_filename, 'a', encoding='utf-8') as f:
                    w = csv.DictWriter(f, export.keys(),delimiter='\t')
                    w.writerow(export)
                # Записываем номер последней успешнообработанной страницы
                with open(log_file, 'w') as log:
                    log.write(str(page))