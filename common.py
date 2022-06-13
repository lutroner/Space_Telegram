from os.path import splitext
from urllib.parse import urlsplit

import requests

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def define_file_extension(url="https://example.com/txt/hello%20world.txt?v=9#python"):
    file_path = urlsplit(url).path
    _, file_extension = splitext(file_path)
    return file_extension


def download_image(image_url, image_path, payload=None):
    response = requests.get(image_url, headers=USER_AGENT, params=payload)
    response.raise_for_status()
    with open(f'{image_path}', 'wb') as file:
        file.write(response.content)
