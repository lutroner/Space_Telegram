import telegram
from dotenv import load_dotenv
import os
from os import environ
import random


def get_file_path():
    file_path_list = []
    for path, dirs, files in os.walk('images/'):
        for name in files:
            file_path_list.append(os.path.join(path, name))
    return file_path_list


def get_random_path(file_path_list):
    random_path = random.choice(file_path_list)
    file_path_list.remove(random_path)
    return random_path


def publish_random_image(random_image, chat_id):
    bot = telegram.Bot(token=environ.get('BOT_TOKEN'))
    try:
        bot.send_photo(photo=open(random_image, 'rb'), chat_id=chat_id)
    except IndexError:
        print('Images/ directory is empty')


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.environ.get('CHAT_ID')
    random_image = get_random_path(get_file_path())
    publish_random_image(random_image, chat_id=chat_id)
