import urllib.request
import requests as req
from bs4 import BeautifulSoup as soup
import os
import math
import time
from colorama import Fore,Back,init
init(autoreset=True)
# ----------------------------setting up working directories---------------------------------------
if not (os.path.isdir('downloads')):
    os.makedirs('downloads')
    print('directory downloads created')
os.chdir('./downloads')
print(Fore.LIGHTGREEN_EX+"current directory :", os.getcwd())
url = input('enter url :')
print(Fore.LIGHTGREEN_EX+'url set to -->', url)
if "album" in url:
    try:
        modelname = url.split('/')[4].split('.')[0]
        print(Fore.LIGHTGREEN_EX+"album name :", modelname)
        if os.path.isdir(modelname):
            os.chdir(f'./{modelname}')
        else:
            os.makedirs(modelname)
            os.chdir(f'./{modelname}')
    except Exception as err:
        print("excp1", err)
try:
    numberofpages = int(input('give me number of pages :'))
except Exception:
    numberofpages = None
    print(Fore.YELLOW+'auto download mode activated')
# ----------------------------- where shit happens----------------------------------------------
i = 0
currentpage = 1
settotalimgs = True
totalimages = ""
print(Fore.RED+'::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
try:
    while True:
        print('current page :', currentpage)
        if not url:
            break
        data = req.get(url)
        if not data.status_code == 200:
            print('retrying')
            continue
        currentpage += 1
        html = soup(data.text, 'html.parser')
        if "album" in url and settotalimgs:
            try:
                totalimages = html.find(
                    "span", {"data-text": "image-count"}).text
            except Exception:
                totalimages = "unkown"
                print(Fore.RED+'excp3 unkonwn image number')
            settotalimgs = False
        thmbnailanchors = html.findAll(attrs={"class": "--media"})
        links = html.findAll(attrs={"data-pagination": "next"})
        try:
            url = links[0].attrs['href']
        except Exception as err:
            url = None
            print(Fore.YELLOW+"downloading will stop automatically after all images are downloaded")
        print('next page url :', url)
        for ref in thmbnailanchors:
            imgdata = req.get(ref.attrs['href'])
            if not imgdata.status_code == 200:
                print('retrying in 5 secs')
                time.sleep(5)
                continue
            imghtml = soup(imgdata.text, 'html.parser')
            downloadanch = imghtml.find(attrs={'class': 'btn-download'})
            currentimg = downloadanch.attrs['href']

            try:
                with open(str(ref.attrs['href'].split('/').pop())+".jpg", 'wb') as file:
                    try:
                        img = req.get(currentimg)
                        file.write(img.content)
                        i += 1
                        # print(f'downloaded images : {i}')
                        print(
                           Fore.LIGHTMAGENTA_EX+ f'latest download : {currentimg} ; images downloaded: {i} ; total images :{totalimages if len(totalimages) else "--> dynamic"}', end='\r')
                        time.sleep(0.5)
                    except Exception as err:
                        print(Fore.RED+"excp4", err)

            except Exception as err:
                print(Fore.RED+"excp5", err)
        # print('page switched')
        if numberofpages != None:
            if currentpage > numberofpages:
                break
    input('--------------------done press enter----------------------')
except Exception as err:
    print(Fore.RED+"excp6", err)
