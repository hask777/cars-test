import requests
from bs4 import BeautifulSoup
import json
import re
from avlist import brands_code_list

# brands_code_list = {
#     'acura': 1444,
#     'alfa-romeo': 1,
#     'audi': 6,
#     'bmw': 8,
#     'cadilac': 40,
#     'chevrolet': 41,
#     'chrysler': 42,
#     'citroen': 43,
#     'daewoo': 46,
#     'dodge':45,
#     'fiat': 301,
#     'ford': 330,
#     'geely': 2012,
#     'great-wall': 1726,
#     'honda': 383,
#     'hyundai': 433,
#     'infinity': 1343,
#     'jaguar': 526,
#     'jeep': 540,
#     'kia': 545,
#     'lada': 1279,
#     'lancia': 572,
#     'land-rover': 548,
#     'lexus': 589,
#     'mazda': 634,
#     'mercedes-benz': 683,
#     'mitsubishi': 834,
#     'nissan': 892,
#     'opel': 966,
#     'peugeot': 989,
#     'porshe': 1485,
#     'renault': 1039,
#     'rover': 1067,
#     'saab': 1085,
#     'seat': 1091,
#     'skoda': 1126,
#     'ssangyong': 1597,
#     'subaru': 1136,
#     'toyota': 1181,
#     'volkswagen': 1216,
#     'volvo': 1238,
#     'uaz': 1464
# }

# for k, v in brands_code_list.items():
#     print(k)

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

            finalcars.append(carslinks)

    print(len(finalcars))


    cars = f"{k}.json"
    with open(cars, 'w', encoding='utf-8') as json_file:
        json.dump(finalcars, json_file, ensure_ascii = False, indent =4)


    print('file dumped')