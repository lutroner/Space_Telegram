import requests
from dotenv import load_dotenv
from pathlib import Path
from common import USER_AGENT, download_image
import argparse


def fetch_spacex_last_launch_images(spacex_id):
    Path("images/spacex").mkdir(parents=True, exist_ok=True)
    photos_url = f'https://api.spacexdata.com/v4/launches/{spacex_id}'
    response = requests.get(photos_url, headers=USER_AGENT)
    response.raise_for_status()
    spacex_photos = response.json()['links']['flickr']['original']
    for index, image_url in enumerate(spacex_photos, 1):
        file_path = f'images/spacex/spacex{index}.jpg'
        download_image(image_url, file_path)


if __name__ == '__main__':
    load_dotenv()
    spacex_parser = argparse.ArgumentParser(description='Скрипт для скачивания фото SpaceX')
    spacex_parser.add_argument('spacex_id', help='id аккаунта SpaceX')
    spacex_id = spacex_parser.parse_args().spacex_id
    fetch_spacex_last_launch_images(spacex_id)
