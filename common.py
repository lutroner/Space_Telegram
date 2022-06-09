from urllib.parse import urlsplit
from os.path import splitext

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def define_file_extension(url="https://example.com/txt/hello%20world.txt?v=9#python"):
    file_path = urlsplit(url).path
    _, file_extension = splitext(file_path)
    return file_extension
