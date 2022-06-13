from os import environ
from time import sleep

from dotenv import load_dotenv

from fetch_apod_nasa_images import fetch_nasa_apod_images
from fetch_epic_nasa_images import fetch_epic_dataset, fetch_epic_nasa_images
from fetch_spacex_images import fetch_spacex_last_launch_images
from publish_image_to_telegram import (get_file_paths, get_random_image_path,
                                       publish_random_image)

if __name__ == '__main__':
    load_dotenv()
    nasa_id = environ.get('NASA_ID')
    spacex_id = environ.get('SPACEX_ID')
    chat_id = environ.get('CHAT_ID')
    delay = int(environ.get('DELAY'))
    bot_token = environ.get('BOT_TOKEN')
    file_path = get_file_paths()
    while True:
        if not file_path:
            fetch_spacex_last_launch_images(spacex_id)
            fetch_nasa_apod_images(nasa_id, 2)
            epic_dataset = fetch_epic_dataset(nasa_id)
            fetch_epic_nasa_images(nasa_id, quantity=2, epic_dataset=epic_dataset)
            file_path = get_file_paths()
        else:
            random_image = get_random_image_path(file_path)
            publish_random_image(random_image, chat_id=chat_id, bot_token=bot_token)
        sleep(delay)
