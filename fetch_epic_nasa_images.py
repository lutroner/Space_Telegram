import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from common import USER_AGENT, download_image
import argparse
import os


def fetch_epic_dataset(nasa_id):
    payload = {"api_key": f"{nasa_id}"}
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_url, headers=USER_AGENT, params=payload)
    response.raise_for_status()
    epic_dataset = {datetime.fromisoformat(epic['date']): epic['image'] for epic in response.json()}
    return epic_dataset


def fetch_epic_nasa_images(nasa_id, quantity, epic_dataset):
    Path("images/epic").mkdir(parents=True, exist_ok=True)
    epic_urls = []
    payload = {"api_key": f"{nasa_id}"}
    for date, filename in epic_dataset.items():
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
                   f'{date.year}/{date.month:02d}/' \
                   f'{date.day:02d}/png/{filename}.png'
        epic_urls.append(epic_url)
    for index, image_url in enumerate(epic_urls[:int(quantity)], 1):
        image_path = f'images/epic/epic_{index}.png'
        download_image(image_url, image_path, payload)


if __name__ == '__main__':
    load_dotenv()
    epic_parser = argparse.ArgumentParser(description='Скачивание фото EPIC(Nasa)')
    epic_parser.add_argument('--nasa_id', nargs='?', default=os.getenv('NASA_ID'), help='Токен API NASA')
    epic_parser.add_argument('--quantity', nargs='?', default=5, help='Количиство фото')
    nasa_id = epic_parser.parse_args().nasa_id
    quantity = epic_parser.parse_args().quantity
    epic_dataset = fetch_epic_dataset(nasa_id)
    fetch_epic_nasa_images(nasa_id, quantity, epic_dataset)
