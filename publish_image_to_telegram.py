import telegram
from dotenv import load_dotenv
import os
import random


def get_file_paths():
    file_path_list = []
    for path, dirs, files in os.walk('images/'):
        for name in files:
            file_path_list.append(os.path.join(path, name))
    return file_path_list


def get_random_image_path(file_path_list):
    try:
        random_image_path = random.choice(file_path_list)
        file_path_list.remove(random_image_path)
        return random_image_path
    except IndexError:
        print('Images/ directory is empty')


def publish_random_image(random_image_path, chat_id, bot_token):
    bot = telegram.Bot(token=bot_token)
    with open(random_image_path, 'rb') as file:
        bot.send_photo(photo=file, chat_id=chat_id)


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.environ.get('CHAT_ID')
    bot_token = os.environ.get('BOT_TOKEN')
    random_image = get_random_image_path(get_file_paths())
    publish_random_image(random_image, chat_id=chat_id, bot_token=bot_token)
