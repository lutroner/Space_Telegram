import requests
from pathlib import Path

from dotenv import load_dotenv
from os import environ
from datetime import datetime
import telegram
from fetch_spacex_images import fetch_spacex_last_launch
from fetch_apod_nasa_images import fetch_nasa_apod
from fetch_epic_nasa_images import fetch_epic_photos, fetch_epic_dataset



if __name__ == '__main__':
    load_dotenv()
    nasa_id = environ.get('NASA_ID')
    spacex_id = environ.get('SPACEX_ID')
    chat_id = environ.get('CHAT_ID')
    fetch_spacex_last_launch(spacex_id)
    fetch_nasa_apod(nasa_id, 5)
    epic_dataset = fetch_epic_dataset(nasa_id)
    fetch_epic_photos(nasa_id, quantity=5, epic_dataset=epic_dataset)
