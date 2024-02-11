#!/usr/bin/python3

# make sure you have these packages installed
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os

# choose whenever you want the crests/logos to be save inside your system
# BUT, make sure you create the directory before running this script.
logosDir = "***"

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
# RO2 stands for the second Romanian football division
# RO1 stands for the first division - SuperLiga.
page="https://www.transfermarkt.com/liga-1/startseite/wettbewerb/RO2/saison_id/2023"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
# inside the "Table" page, we are looking for all crests with "tiny_wappen" class
# inspect the page URL above to check it out
logos = pageSoup.findAll("img", {"class":"tiny_wappen"})

# Save images to local directory
for logo in logos:
    newLogoSource = logo.get('src').replace('tiny', 'normal')
    response = requests.get(newLogoSource)
    if response.status_code == 200:
        with open(logosDir + logo.get("title") + ".png", 'wb') as f:
            f.write(response.content)

# Resize the images
for logo in os.listdir(logosDir):
    # the prints inside are just for monitoring what is happening. feel free to remove them if you don't need them
    print(logosDir + logo)
    image = Image.open(logosDir + logo)
    image = image.resize((300, 352))
    image.save(logosDir + logo)
    print(image.size)
