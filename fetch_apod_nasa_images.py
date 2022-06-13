import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from common import USER_AGENT, define_file_extension, download_image


def fetch_nasa_apod_images(nasa_id, quantity):
    Path("images/nasa_apod").mkdir(parents=True, exist_ok=True)
    payload = {"api_key": f"{nasa_id}", "count": f"{quantity}"}
    apod_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(apod_url, headers=USER_AGENT, params=payload)
    response.raise_for_status()
    for index, image_url in enumerate(response.json(), 1):
        image_url = image_url['url']
        image_path = f'images/nasa_apod/nasa_apod_{index}{define_file_extension(image_url)}'
        download_image(image_url, image_path)


if __name__ == '__main__':
    load_dotenv()
    apod_parser = argparse.ArgumentParser(description='Скачивание фото APOD(Nasa)')
    apod_parser.add_argument('--nasa_id', nargs='?', default=os.getenv('NASA_ID'), help='Токен API NASA')
    apod_parser.add_argument('--quantity', nargs='?', default=5, help='Количество фото')
    nasa_id = apod_parser.parse_args().nasa_id
    quantity = apod_parser.parse_args().quantity
    fetch_nasa_apod_images(nasa_id, quantity)
