from asyncore import write
from urllib import response
import requests
from curl import headers  
import os
from bs4 import BeautifulSoup
import time
import random
import csv
import json


'''
Скрапинг сайта
https://dixy.ru/catalog/
'''

# функция сбора данных
def get_data():
    
    # создал объект ссесии
    sess = requests.Session()

    # запрос   
    response = sess.get(url='https://dixy.ru/catalog/', headers=headers, verify=False)

    # проверяю и в случае необходимости создаю директорию
    if not os.path.exists('data'):
        os.mkdir('data')

    # сохраняю страницу
    with open('data/index.html', 'w') as file:
        file.write(response.text)

    # инфоблок
    print(f"[INFO] index page saved\n")
    
    # переменна для записи данных в json
    all_data_json = []

    # переменная для записи данных в csv
    all_data_csv = []

    # в эту переменную буду записывать номер страницы
    number_page = 1

    while True:
        
        url_page = f'https://dixy.ru/catalog/?PAGEN_1={number_page}'

        # инфоблок
        print(f"[INFO] next page {number_page}\n")

        # запрос к странице        
        response = sess.get(url=url_page, headers=headers, verify=False)
    
        # создаю объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # нахожу блок с карточками
        product_cards = soup.find_all('div', class_='product-container')

        # собираю информация из карточек  !! забыл собрать ссылку на карточку 
        for card in product_cards:

            try:
                card_name = card.find('div', class_='dixyCatalogItem__hover').text.strip()            
            except Exception as ex:            
                card_name = card.find('div', class_='dixyCatalogItem__title').text.strip()                

            try:
                card_price = card.find('div', class_='dixyCatalogItemPrice__new').text.strip()
            except Exception as ex:
                card_price = "card_price"

            try:
                card_discont = card.find('div', class_='dixyCatalogItemPrice__discount').text.strip().replace('-', '').replace('%', '')
            except Exception as ex:
                card_discont = 'No data'

            # print(f'card_name: {card_name}\ncard_price: {card_price}\ncard_discont(%): {card_discont}\n')

            # собранные данные сохраню в переменную для записи в json
            all_data_json.append(
                {
                    'card_name': card_name,
                    'card_price': card_price,
                    'card_discont': card_discont,
                }
            )

            # собранные данные сохраню в переменную для записи в csv
            all_data_csv.append(
                [
                    card_name,
                    card_price,
                    card_discont
                ]
            )

        # условие если есть пагинация с номером следующей страницей, увеличиваю номер страницы для следующего запроса        
        if soup.find('a', class_='view-more'):
        # if soup.find('a', class_='view-more') and number_page < 3:  # для тестового запуска

            number_page += 1

            # инфоблок
            print(f"[INFO] this is not the last page \n")

            # пауза между страницами
            time.sleep(random.randrange(2, 4))            

        # если на текущей странице нет пагинации - записываю данные, останавливаю код
        else:
            # инфоблок
            print(f"\n[INFO] data collection completed !!! \n")

            # print(f'All_data_csv: {all_data_csv}\nAll_data_json: {all_data_json}\n')

            # запишу в словарь переменные с собранными данными
            data_dict = {'all_data_csv' : all_data_csv, 'all_data_json' : all_data_json}

            # в следующ.функции, получу словарь для записи
            return data_dict
            

def recording_data(data_dict):

    # инфоблок
    print(f"\n[INFO] start recording_data \n")

    all_data_csv = data_dict.get('all_data_csv')
    all_data_json = data_dict.get('all_data_json')

    # записываю данные в csv
    with open('data/all_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Card_name',
                'Card_price',
                'Card discont'
            )
        )
        writer.writerows(all_data_csv)

    # записываю данные в json
    with open('data/all_data.json', 'w') as file:
        json.dump(all_data_json, file, indent=4, ensure_ascii=False)

    # инфоблок
    print(f"[INFO] code completed!!!")        


def main():
    recording_data(get_data())

if __name__ == "__main__":
    main()
