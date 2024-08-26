import sys
import csv
import time
from datetime import datetime
import requests
import json
import os
import re
from os import listdir
from os.path import join, dirname, isfile
from dotenv import load_dotenv
import codecs
sys.stdout.reconfigure(encoding='ISO-8859-1')

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

with open(sys.argv[1], 'r', encoding='iso-8859-1') as f:
    webpage = f.read()

soup = BeautifulSoup(webpage, 'html.parser')

content = soup.find("div", {"class": "content-area"})

table = content.find('table')

posts = table.find_all('tr', {'class': 'post-row'})

output = []
hobos = {}

if os.path.exists('public/hobos.csv'):
    with open('public/hobos.csv', 'r', encoding='iso-8859-1') as f:
        rows = csv.DictReader(f, delimiter=',', quotechar='|')

        for row in rows:
            hobos[row['ID'].strip()] = row['Name'].strip()

onlyfiles = [f for f in listdir('raw') if isfile(join('raw', f)) and 'memberstats' in f]
membership=sorted(onlyfiles, key=lambda f: datetime.strptime(f, 'memberstats-%m-%d-%y.csv'), reverse=True)
with open('raw/'+membership[0], 'r', encoding='iso-8859-1') as f:
    rows = csv.DictReader(f, delimiter=',', quotechar='|')

    for row in rows:
        hobos[row[' ID'].strip()] = row['Name']

with codecs.open('public/hobos.csv', 'w', 'ISO-8859-1') as f:
    f.write('ID,Name\n')
    for id, name in hobos.items():
        f.write(id + ',' + name + '\n')
with codecs.open('public/hobos.json', 'w', 'ISO-8859-1') as f:
    f.write('{')
    items = []
    for id, name in hobos.items():
        items.append('"' + id + '":"' + name + '"')
    f.write(',\n'.join(items))
    f.write('}')


# for p in posts:
#     name = p.find('span', {'class': 'player-name'})
#     link = name.parent.parent
#     parsed_url = urlparse(link['href'])
#     qs = parse_qs(parsed_url.query)
#     print('https://hobowars.com/game/' + link['href'])

#     id = qs['ID'][0]
#     # print(name.prettify('iso-8859-1'))
#     name_text = name.get_text(strip=True)
#     name_style = name["style"]
#     # print(name_text)
#     post_content = p.find('span', id=lambda x: x and x.startswith('post-content-')).get_text(strip=True)
#     # print(post_content.prettify())
#     # print(post_content.text.strip())

#     hobos[id] = name_text
#     output.append({ 'id': id, 'name': name_text, 'name_style': name_style, 'post': post_content})


# date = datetime.today().strftime('%Y-%m-%d')

# with codecs.open('public/' + date + '.json', 'w', 'ISO-8859-1') as f:
#     json.dump(output, f)

# cookies = {'substack.sid': os.environ.get("SESSION")}
# url = os.environ.get("DOMAIN") + '/api/v1/generate_image/generate_art'
# for post in output: 
#     full_dir = 'public/' + post['id'] + '/' + date
#     if not os.path.exists(full_dir):
#         os.makedirs(full_dir) 
#     if os.path.exists(full_dir + '/images.json'):
#         with open(full_dir + '/images.json', 'r', encoding='utf-8') as f:
#             images = f.read()
#             imageArrayString = json.loads(images)
#         should_wait = False
#     else :
#         print('getting imagse for id ' + post['id'])
#         myobj = {"prompt":post['post'],"style":"","num_images":4}
#         x = requests.post(url, json = myobj, cookies = cookies)
#         should_wait = True

#         print(x.text)
#         with open(full_dir + '/images.json', 'w') as f:
#             json.dump(x.text, f)

#         imageArrayString = x.text

#     imageArray = json.loads(imageArrayString)

#     print(imageArray)

#     for image in imageArray:
#         print(image)
#         image_name = image.rsplit('/', 1)[-1]

#         image_path = full_dir + '/' + image_name + '.jpg'
#         if not os.path.exists(image_path):
#             img_data = requests.get(image).content
#             with open(image_path, 'wb') as handler:
#                 handler.write(img_data)

#     if should_wait:
#         time.sleep(60/6)