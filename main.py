import json
import sys
from io import BytesIO
from requests_function import param_del, lonlat_distance

import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
toponym_coodrinates = toponym["Point"]["pos"].split(" ")

apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
search_params = {
    "apikey": api_key,
    "text": "Аптека",
    "lang": "ru_RU",
    "ll": ','.join([toponym_longitude, toponym_lattitude]),
    "type": "biz",
}
search_api_server = "https://search-maps.yandex.ru/v1/"
data = requests.get(search_api_server, params=search_params).json()
organization = data["features"][0]
print(organization)
organization_coordinates = organization['geometry']['coordinates']
organization_longitude, organization_latitude = organization_coordinates
organization_metadata = organization['properties']['CompanyMetaData']
print('Адрес:', organization_metadata['address'])
print('Название:', organization_metadata['name'])
print('Время работы:', organization_metadata['Hours']['text'])
print('Расстояние:', str(int(
    lonlat_distance(list(map(float, toponym_coodrinates)), list(map(float, organization_coordinates))))) + "м")

map_params = {
    "l": "map",
    "pt": f'{toponym_longitude},{toponym_lattitude},comma~{organization_longitude},{organization_latitude},pm2rdl'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
