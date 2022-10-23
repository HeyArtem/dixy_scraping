# Скрапинг данных сайт продуктового ритейлера Dixy <br/>https://dixy.ru/catalog/


![alt-текст](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Текст заголовка логотипа 1")



## Тех.детали: 
* _requests_ 
* _BeautifulSoup_
* _os_
* _json_
* _csv_ 
* _time_
* _random_
<br/><br/>
<hr>

## Описание:
Скрипт сохранит первую страницу с акционными товарами (это чисто для проверки, что дает сайт) 
<br/>соберет данные с первой страницы:
<br/>- наименование товара,
<br/>- стоимость,
<br/>- размер скидки,
<br/>запишет данные в json и csv.
<br/><br/>
<hr>

## Особенности:
* когда делал запрос, получал ошибку связанную с устаревшими сертификатами
> 'requests.exceptions.SSLError: HTTPSConnectionPool(host='dixy.ru', port=443): Max retries exceeded with url: /catalog/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1131)')))'

решил проблему добавлением 'verify=False':
>  response = sess.get(url='https://dixy.ru/catalog/', headers=headers, verify=False)

* в архитектуре карточки не всегда в была полная информация о товаре, поэтому в первую очередь брал из другогй части карточки, но эта информация не всегда была заполнена. Решил через Try:
```python
try:
    card_name = card.find('div', class_='dixyCatalogItem__hover').text.strip()            
except Exception as ex:            
    card_name = card.find('div', class_='dixyCatalogItem__title').text.strip()
```

* В блоке с пагинацией не было информации о последней странице, только код следующей страницы, кроме последней, поэтому код поместил в "while True", а в конце создал условие, если нет ссылки на следующую страницу, то завершить цикл, перейти к return
```python
 else:
    # инфоблок
    print(f"\n[INFO] data collection completed !!! \n")
    
    # запишу в словарь переменные с собранными данными
    data_dict = {'all_data_csv' : all_data_csv, 'all_data_json' : all_data_json}

    # в следующ.функции, получу словарь для записи
    return data_dict
```

* Разбил код на две функции. Первая собирает данные, вторай записывает.

* Использовал передачу данных между функциями

<br/>
P.S. Нужно было ссылку на карточку взять и неплохо отсортировать товары по алфавиту
<br/><br/>
<hr>

## Что бы запустить проект:
- создать директорию на компьютере
- открыть нужный репозиторий-Code-HTTPS-скопировать ссылку
- $ git clone + ссылка
- перейти в паку с проектом
- $ python3 -m venv venv -создать виртуальное окружение
- $ source venv/bin/activate -активировать виртуальное окружение
- $ pip install -U pip setuptools
- $ pip install -r requirements.txt -установить библиотеки из requirements.txt
- $ code . -открыть проект
- запустить main.py (возможно потребуются свежие curl)
<br/><br/>
<hr>

