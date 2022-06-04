from urllib.parse import urlsplit, unquote
from os.path import split, splitext

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


def define_file_extension(url="https://example.com/txt/hello%20world.txt?v=9#python"):
    return splitext(split(unquote(urlsplit(url).path))[1])[1]
