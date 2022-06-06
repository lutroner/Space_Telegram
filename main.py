from dotenv import load_dotenv
from os import environ
from fetch_spacex_images import fetch_spacex_last_launch
from fetch_apod_nasa_images import fetch_nasa_apod
from fetch_epic_nasa_images import fetch_epic_photos, fetch_epic_dataset
from publish_image_to_telegram import get_file_path, get_random_path, publish_random_image
from time import sleep

if __name__ == '__main__':
    load_dotenv()
    nasa_id = environ.get('NASA_ID')
    spacex_id = environ.get('SPACEX_ID')
    chat_id = environ.get('CHAT_ID')
    delay = int(environ.get('DELAY'))
    file_path = get_file_path()
    while True:
        if not file_path:
            fetch_spacex_last_launch(spacex_id)
            fetch_nasa_apod(nasa_id, 2)
            epic_dataset = fetch_epic_dataset(nasa_id)
            fetch_epic_photos(nasa_id, quantity=2, epic_dataset=epic_dataset)
            file_path = get_file_path()
        else:
            random_image = get_random_path(file_path)
            publish_random_image(random_image, chat_id=chat_id)
        sleep(delay)
        print(file_path)
