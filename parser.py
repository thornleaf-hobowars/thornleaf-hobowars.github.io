import sys
import time
from datetime import datetime
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

with open(sys.argv[1], 'r', encoding='iso-8859-1') as f:
    webpage = f.read()

soup = BeautifulSoup(webpage, 'html.parser')

content = soup.find("div", {"class": "content-area"})

table = content.find('table')

posts = table.find_all('tr', {'class': 'post-row'})

output = []

for p in posts:
    name = p.find('span', {'class': 'player-name'})
    link = name.parent.parent
    parsed_url = urlparse(link['href'])
    qs = parse_qs(parsed_url.query)
    print('https://hobowars.com/game/' + link['href'])

    id = qs['ID'][0]
    name_text = name.text.strip()
    name_style = name["style"]
    # print(name_text)
    post_content = p.find('span', id=lambda x: x and x.startswith('post-content-')).text.strip()
    # print(post_content.prettify())
    # print(post_content.text.strip())

    output.append({ 'id': id, 'name': name_text, 'name_style': name_style, 'post': post_content})

print(output)

dir = datetime.today().strftime('%Y-%m-%d')
if not os.path.exists(dir):
    os.makedirs(dir) 

with open(dir + '/data.json', 'w') as f:
    json.dump(output, f)


cookies = {'substack.sid': os.environ.get("SESSION")}
url = os.environ.get("DOMAIN") + '/api/v1/generate_image/generate_art'
for post in output: 
    full_dir = 'images/' + post['id'] + '/' + dir
    if not os.path.exists(full_dir):
        os.makedirs(full_dir) 
    if os.path.exists(full_dir + '/images.json'):
        with open(full_dir + '/images.json', 'r', encoding='utf-8') as f:
            images = f.read()
            imageArrayString = json.loads(images)
        should_wait = False
    else :
        print('getting imagse for id ' + post['id'])
        myobj = {"prompt":post['post'],"style":"","num_images":4}
        x = requests.post(url, json = myobj, cookies = cookies)
        should_wait = True

        print(x.text)
        with open(full_dir + '/images.json', 'w') as f:
            json.dump(x.text, f)

        imageArrayString = x.text

    imageArray = json.loads(imageArrayString)

    print(imageArray)

    for image in imageArray:
        print(image)
        image_name = image.rsplit('/', 1)[-1]

        image_path = full_dir + '/' + image_name + '.jpg'
        if not os.path.exists(image_path):
            img_data = requests.get(image).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)

    if should_wait:
        time.sleep(60/6)