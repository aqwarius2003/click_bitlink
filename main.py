import requests
import os
from urllib.parse import urlparse
BITLINKS_URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink = parsed_url.netloc + parsed_url.path
    response = requests.get(f'{BITLINKS_URL}/{bitlink}', headers=headers)
    if response.ok:
        return True


def get_shorten_link(token, url):
    response = requests.get(url)
    if response.ok:
        headers = {'Authorization': f'Bearer {token}'}
        data_url = {'long_url': url}
        response = requests.post(BITLINKS_URL, headers=headers, json=data_url)
        if response.ok:
            bitlink = response.json().get('link')
            return bitlink


def get_count_cliks(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    bitlink = url.replace('https://', '').replace('http://', '')
    clicks_bitlink_link = f'{BITLINKS_URL}/{bitlink}/clicks/summary'
    response = requests.get(clicks_bitlink_link, headers=headers)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def main():
    token = os.environ['BITLINK_TOKEN']
    url = input('Введите ссылку: ')
    response = requests.get(url)
    if not response.ok:
        print('URL-адрес недоступен')
        return
    if is_bitlink(token, url):
        try:
            click_count = get_count_cliks(token, url)
            print(f'По ссылке {url} было совершено {click_count} переходов')
        except requests.exceptions.HTTPError as error:
            print('При проверке количества кликов ошибка:\n{0}'.format(error))
            return
    else:
        bitlink = get_shorten_link(token, url)
        if bitlink:
            print(f'Для адреса {url} \nкороткая ссылка: {bitlink}')
        else:
            print(f'При получении короткой ссылки произошла ошибка')


if __name__ == "__main__":
    main()
