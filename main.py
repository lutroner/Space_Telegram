import requests
from pathlib import Path
from urllib.parse import urlsplit, unquote
from os.path import split, splitext
from dotenv import load_dotenv
from os import environ
from datetime import datetime
import telegram

Path("images").mkdir(parents=True, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def define_file_extension(url="https://example.com/txt/hello%20world.txt?v=9#python"):
    return splitext(split(unquote(urlsplit(url).path))[1])[1]


def fetch_spacex_last_launch(spacex_id):
    Path("images/spacex").mkdir(parents=True, exist_ok=True)
    photos_url = f'https://api.spacexdata.com/v4/launches/{spacex_id}'
    response = requests.get(photos_url, headers=headers)
    response.raise_for_status()
    spacex_photos = response.json()['links']['flickr']['original']
    for index, photo in enumerate(spacex_photos, 1):
        response = requests.get(photo, headers=headers)
        response.raise_for_status()
        with open(f'images/spacex/spacex{index}.jpg', 'wb') as file:
            file.write(response.content)


def fetch_nasa_apod(nasa_id, quantity):
    Path("images/nasa_apod").mkdir(parents=True, exist_ok=True)
    payload = {"api_key": f"{nasa_id}", "count": f"{quantity}"}
    apod_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(apod_url, headers=headers, params=payload)
    response.raise_for_status()
    for index, image_url in enumerate(response.json(), 1):
        response = requests.get(image_url['url'], headers=headers)
        response.raise_for_status()
        with open(f'images/nasa_apod/nasa_apod_{index}{define_file_extension(image_url["url"])}', 'wb') as file:
            file.write(response.content)


def fetch_epic_dataset(nasa_id) -> dict:
    payload = {"api_key": f"{nasa_id}"}
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_url, headers=headers, params=payload)
    response.raise_for_status()
    epic_dataset = {datetime.fromisoformat(epic['date']): epic['image'] for epic in response.json()}
    return epic_dataset


def fetch_epic_photos(nasa_id, epic_dataset, quantity):
    Path("images/epic").mkdir(parents=True, exist_ok=True)
    epic_urls = []
    payload = {"api_key": f"{nasa_id}"}
    for date, filename in epic_dataset.items():
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date.month:02d}/' \
                   f'{date.day:02d}/png/{filename}.png'
        epic_urls.append(epic_url)
    for index, image_url in enumerate(epic_urls[:quantity + 1], 1):
        response = requests.get(image_url, params=payload, headers=headers)
        response.raise_for_status()
        with open(f'images/epic/epic_{index}.png', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    load_dotenv()
    nasa_id = environ.get('NASA_ID')
    spacex_id = environ.get('SPACEX_ID')
    chat_id = environ.get('CHAT_ID')
    fetch_spacex_last_launch(spacex_id)
    fetch_nasa_apod(nasa_id, 5)
    epic_dataset = fetch_epic_dataset(nasa_id)
    fetch_epic_photos(nasa_id, epic_dataset=epic_dataset, quantity=5)
    bot = telegram.Bot(token=environ.get('BOT_TOKEN'))
    print(bot.get_me())
    l = bot.send_message(chat_id=chat_id, text='Hi there!?')