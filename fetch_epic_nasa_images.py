import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from common import USER_AGENT
import argparse

load_dotenv()


def fetch_epic_dataset(nasa_id) -> dict:
    payload = {"api_key": f"{nasa_id}"}
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_url, headers=USER_AGENT, params=payload)
    response.raise_for_status()
    epic_dataset = {datetime.fromisoformat(epic['date']): epic['image'] for epic in response.json()}
    return epic_dataset


def fetch_epic_photos(nasa_id, quantity, epic_dataset):
    Path("images/epic").mkdir(parents=True, exist_ok=True)
    epic_urls = []
    payload = {"api_key": f"{nasa_id}"}
    for date, filename in epic_dataset.items():
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
                   f'{date.year}/{date.month:02d}/' \
                   f'{date.day:02d}/png/{filename}.png'
        epic_urls.append(epic_url)
    for index, image_url in enumerate(epic_urls[:int(quantity)], 1):
        response = requests.get(image_url, params=payload, headers=USER_AGENT)
        response.raise_for_status()
        with open(f'images/epic/epic_{index}.png', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    epic_parser = argparse.ArgumentParser(description='Скачивание фото EPIC(Nasa)')
    epic_parser.add_argument('nasa_id', help='ID от APOD Api NASA')
    epic_parser.add_argument('quantity', help='Количиство фото')
    nasa_id = epic_parser.parse_args().nasa_id
    quantity = epic_parser.parse_args().quantity
    epic_dataset = fetch_epic_dataset(nasa_id)
    fetch_epic_photos(nasa_id, quantity, epic_dataset)
