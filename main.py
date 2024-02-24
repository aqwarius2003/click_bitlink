import requests
import os
from urllib.parse import urlparse
BITLY_API = 'https://api-ssl.bitly.com/v4/bitlinks'


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink_url = parsed_url.netloc + parsed_url.path
    response = requests.get(f'{BITLY_API}/{bitlink_url}', headers=headers)
    if response.ok:
        return True


def get_shorten_link(token, url):
    response = requests.get(url)
    if response.ok:
        headers = {'Authorization': f'Bearer {token}'}
        deeplinks = {'long_url': url}
        response = requests.post(BITLY_API, headers=headers, json=deeplinks)
        if response.ok:
            bitlink = response.json().get('link')
            return bitlink


def get_count_cliks(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    bitlink = url.replace('https://', '').replace('http://', '')
    clicks_bitlink_link = f'{BITLY_API}/{bitlink}/clicks/summary'
    response = requests.get(clicks_bitlink_link, headers=headers)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def main():
    token = os.environ['BITLY_TOKEN']
    url = input('Введите ссылку: ')
    response = requests.get(url)
    if not response.ok:
        print('URL-адрес недоступен')
        return
    if is_bitlink(token, url):
        try:
            click_count = get_count_cliks(token, url)
            print(f'По ссылке {url}\nбыло совершено {click_count} кликов')
        except requests.exceptions.HTTPError as error:
            print('При проверке количества кликов ошибка:\n{0}'.format(error))
            return
    else:
        try:
            bitlink = get_shorten_link(token, url)
            print(f'Короткая ссылка: {bitlink}')
        except requests.exceptions.HTTPError as error:
            print('При пролучении короткой ссылки ошибка:\n{0}'.format(error))


if __name__ == "__main__":
    main()
