import requests
from argparse import ArgumentParser
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


BITLY_API = 'https://api-ssl.bitly.com/v4/bitlinks'


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink_url = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'{BITLY_API}/{bitlink_url}', headers=headers)
    return response.ok


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    long_url = {'long_url': url}
    response = requests.post(BITLY_API, headers=headers, json=long_url)
    response.raise_for_status()
    bitlink = response.json().get('link')
    return bitlink


def count_cliks(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink_url = f'{parsed_url.netloc}{parsed_url.path}'
    clicks_bitlink_link = f'{BITLY_API}/{bitlink_url}/clicks/summary'
    response = requests.get(clicks_bitlink_link, headers=headers)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    # url = input('Введите ссылку: ')
    arg_parser = ArgumentParser(
        description='Скрипт сокращения ссылок с помощью bitlink '
                    'и отображения количества переходов по ним.'
    )
    arg_parser.add_argument('url', help="Длинная ссылка или битлинк.")
    args = arg_parser.parse_args()
    url = args.url
    try:
        if is_bitlink(token, url):
            click_count = count_cliks(token, url)
            print(f'По ссылке {url}\nбыло совершено {click_count} кликов')
        else:
            bitlink = shorten_link(token, url)
            print(f'Короткая ссылка: {bitlink}')
    except requests.exceptions.HTTPError as error:
        print('Произошла ошибка:\n{0}'.format(error))


if __name__ == "__main__":
    main()
