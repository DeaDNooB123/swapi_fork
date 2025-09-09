import requests
import os
from time import sleep


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, add_path=''):
        try:
            response = requests.get(self.base_url + add_path)
            response.raise_for_status()
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')
            return None
        else:
            return response


class SWRequester(APIRequester):
    def get_sw_categories(self):
        resp = self.get('/')
        if resp.status_code != requests.codes.ok:
            return []
        return resp.json()['result'].keys()

    def get_sw_info(self, category):
        resp = self.get(f'/{category}/')
        if resp.status_code != requests.codes.ok:
            return ''
        return resp.text


def save_sw_data():
    requester = SWRequester('https://swapi.tech/api')
    os.makedirs('./data', exist_ok=True)

    categories_list = requester.get_sw_categories()

    for category in categories_list:

        data = requester.get_sw_info(category)
        with open(f'data/{category}.txt', 'w', encoding='utf-8') as file:
            file.write(data + '\n')

        sleep(1)


if __name__ == '__main__':
    save_sw_data()
