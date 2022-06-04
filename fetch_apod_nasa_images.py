import requests
from pathlib import Path
from common import define_file_extension, USER_AGENT
import argparse


def fetch_nasa_apod(nasa_id, quantity):
    Path("images/nasa_apod").mkdir(parents=True, exist_ok=True)
    payload = {"api_key": f"{nasa_id}", "count": f"{quantity}"}
    apod_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(apod_url, headers=USER_AGENT, params=payload)
    response.raise_for_status()
    for index, image_url in enumerate(response.json(), 1):
        response = requests.get(image_url['url'], headers=USER_AGENT)
        response.raise_for_status()
        with open(f'images/nasa_apod/nasa_apod_{index}'
                  f'{define_file_extension(image_url["url"])}', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    apod_parser = argparse.ArgumentParser(description='Скачивание фото APOD(Nasa)')
    apod_parser.add_argument('nasa_id', help='ID от APOD Api NASA')
    apod_parser.add_argument('quantity', help='Количиство фото')
    nasa_id = apod_parser.parse_args().nasa_id
    quantity = apod_parser.parse_args().quantity
    fetch_nasa_apod(nasa_id, quantity)
