import requests
from bs4 import BeautifulSoup
import json
from fastapi import FastAPI, Form, Request
import re
from src.avlist import brands_code_list


app = FastAPI()

def parse_cars():
    for k, v in brands_code_list.items():

        carslinks = {} 
        finalcars = []
        car_id = 0

        for x in range(1,400):

            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }

            r = requests.get(f'https://cars.av.by/filter?brands[0][brand]={v}&price_currency=2&page={x}')

            soup = BeautifulSoup(r.content, 'html.parser')
            carslist = soup.find_all('div', class_='listing-item')

            for item in carslist:

                ''' Find car image '''
                photo = item.find('div', class_='listing-item__photo')
                try:
                    image = photo.find('img')['data-src']
                except:
                    image = "none"

                ''' Find car title '''
                title = item.find('span', class_='link-text').text

                ''' Find car params '''
                params = item.find('div', class_='listing-item__params').text

                ''' Miles '''
                mile_param = re.compile(r"(\d{1}\s\d{3})|(\d{2}\s\d{3})|(\d{3}\s\d{3})")
                miles = mile_param.search(params)

                try:
                    fmiles = miles.group()
                    fmiles = fmiles.split()
                    
                    for x in fmiles:
                        x = int(x)

                    fmiles = fmiles[0] + fmiles[1]
                    fmiles = int(fmiles)
                    # print(type(fmiles))
                except:
                    fmiles = 0
                
                ''' Year '''
                year_param = re.compile(r"(\d{4})")
                year =  year_param.search(params)
                try:
                    fyear = year.group()
                    # print(type(fyear))
                except:
                    fyear = ''

                ''' Volume '''
                volume_param = re.compile(r"(\d{1}[.]\d{1})")
                volume = volume_param.search(params)
                try:
                    fvolume = volume.group()
                    fvolume = float(fvolume)
                except:
                    fvolume = 0.0

                ''' Transmision '''
                transmision_param = re.compile(r"(автомат|механика)")
                transmision = transmision_param.search(params)
                try:
                    ftransmision = transmision.group()
                except:
                    ftransmision = ''

                ''' Engine '''
                engine_param = re.compile(r"(бензин|дизель)")
                engine = engine_param.search(params)
                # print(engine.group())
                try:
                    fengine = engine.group()
                except:
                    fengine = ''

                ''' Find car link '''
                link = item.find('a', href=True)['href']

                ''' Find car price '''
                price_ru = item.find('div', class_='listing-item__price').text
                price_ru = price_ru.replace('р.', ' ').strip()
                price_ru = price_ru.split()

                try:
                    for x in price_ru:
                        x = int(x)

                    price_ru = price_ru[0] + price_ru[1]
                    price_ru = int(price_ru)
                    # print(type(price_ru))
                except:
                    price_ru = 0

                ''' Find car price by usd '''
                price_usd = item.find('div', class_='listing-item__priceusd').text
                price_usd = price_usd.replace('≈', ' ')
                price_usd = price_usd.replace('$', ' ').strip()
                price_usd = price_usd.split()
                
                try:
                    for x in price_usd:
                        x = int(x)
                    price_usd = price_usd[0] + price_usd[1]
                    price_usd = int(price_usd)
                except:
                    price_usd = 0

                
                car_id += 1
            
                carslinks = {
                    "id": car_id,
                    'image': image,
                    'title': title,
                    'params': params,
                    'year': fyear,
                    'volume': fvolume,
                    'engine': fengine,
                    'transmision': ftransmision,
                    'miles': fmiles,
                    'link': link,
                    'price_ru': price_ru,
                    'price_usd': price_usd
                }
                # print(carslinks)

                finalcars.append(carslinks)

        # print(len(finalcars))

        cars = f"{k}.json"
        with open(cars, 'w', encoding='utf-8') as json_file:
            json.dump(finalcars, json_file, ensure_ascii = False, indent =4)

        return finalcars
        # print('file dumped')

@app.get("/")
def home_view():
    return {"av":"parser"}

@app.get("/getcars/{name}")
def get_cars(name: str):
    with open(f'src/{name}.json') as f:
        cars = json.load(f)
        # print(cars)
    return {"cars":cars}

@app.post("/cars")
def get_brands():
    # parse_cars()
    return {"data": parse_cars()}

