import requests
import os
BITLINKS_URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def is_bitlink(url, token):
    headers = {'Authorization': f'Bearer{token}'}
    bitlink = url.replace('https://', '').replace('http://', '')
    response = requests.get(f'{BITLINKS_URL}/{bitlink}', headers=headers)
    if response.ok:
        return True
    else:
        return False


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer{token}'}
    data_url = {'long_url': url}
    response = requests.post(BITLINKS_URL, headers=headers, json=data_url)
    response.raise_for_status()
    bitlink = response.json().get('link')
    return bitlink


def count_cliks(token, url):
    headers = {'Authorization': f'Bearer{token}'}
    bitlink = url.replace('https://', '').replace('http://', '')
    clicks_bitlink_link = f'{BITLINKS_URL}/{bitlink}/clicks'
    response = requests.get(clicks_bitlink_link, headers=headers)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def main():
    token = os.environ['BITLINK_TOKEN']
    url = input('Введите ссылку: ')

    if is_bitlink(url, token):
        try:
            count_cliks(token, url)
        except requests.exceptions.HTTPError as error:
            quit('При проверке количества кликов ошибка:\n{0}'.format(error))
        print(f'По ссылке {url} было совершено {count_cliks} переходов')
    else:
        try:
            bitlink = shorten_link(token, url)
        except requests.exceptions.HTTPError as error:
            quit('При получении короткой ссылки ошибка:\n{0}'.format(error))
        print(f'Для адреса {url} \nкороткая ссылка: {bitlink}')


if __name__ == "__main__":
    main()
