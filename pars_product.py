import requests
from bs4 import BeautifulSoup
from headers import get_random_headers
import re

def parse_product(url_list):
    all_data = []

    for full_link in url_list:
        header = get_random_headers()
        response = requests.get(full_link, headers=header)
        
        if response.status_code != 200:
            print(f"[!] Ошибка при загрузке товара: {full_link}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        # Заголовок
        title_tag = soup.find('h1', class_='navi')
        data['Заголовок'] = title_tag.get_text(strip=True) if title_tag else 'Нет данных на сайте'

        # Код товара
        data['Код товара'] = 'Нет данных на сайте'
        code_tag = soup.find('div', style="padding:0 0 2px 0")
        if code_tag:
            sku_tag = code_tag.find('b', itemprop='sku')
            if sku_tag:
                data['Код товара'] = sku_tag.get_text(strip=True)

        # Цена и Скидка
        data['Цена'] = 'Нет данных на сайте'
        data['Скидка'] = 'Нет данных на сайте'
        price_block = soup.find('div', class_='price')
        if price_block:
            prices = price_block.find_all('span')
            if len(prices) > 0:
                price_text = prices[0].get_text()
                data['Цена'] = int(''.join(re.findall(r'\d+', price_text)))
            if len(prices) > 1:
                price_text = prices[1].get_text()
                data['Скидка'] = int(''.join(re.findall(r'\d+', price_text)))

        # Основные характеристики
        characteristics = {}
        char_table = soup.find('table', class_='ch')
        if char_table:
            rows = char_table.find_all('tr')
            for row in rows:
                key_td = row.find('td', class_='name')
                val_td = row.find('td', class_='value')
                if key_td and val_td:
                    key = key_td.get_text(strip=True)
                    val = val_td.get_text(strip=True)
                    characteristics[key] = val
        data['Основные характеристики'] = (
            '\n'.join(f"{k}: {v}" for k, v in characteristics.items())
            if characteristics else 'Нет данных на сайте'
        )

        # Описание и доп. характеристики
        data['Описание'] = 'Нет данных на сайте'
        data['Доп. характеристики'] = 'Нет данных на сайте'
        desc_div = soup.find('div', style="padding:0 10px 20px 0")
        if desc_div:
            first_p = desc_div.find('p')
            if first_p:
                data['Описание'] = first_p.get_text(strip=True).replace('\xa0', ' ')

            ul = desc_div.find('ul')
            if ul:
                data['Доп. характеристики'] = '\n'.join(
                    li.get_text(strip=True).replace('\xa0', ' ') for li in ul.find_all('li')
                )

        # Видео
        iframe = soup.find('iframe')
        data['Ссылка на видео'] = iframe['src'] if iframe and iframe.has_attr('src') else 'Нет данных на сайте'

        # Документы
        manuals_div = soup.find('div', class_='product_manuals')
        if manuals_div:
            pdf_links = manuals_div.find_all('a', href=True)
            if pdf_links:
                pdf_urls = ['https://entero.ru' + a['href'] for a in pdf_links]
                data['Ссылка на документы'] = '\n'.join(pdf_urls)
            else:
                data['Ссылка на документы'] = 'Нет данных на сайте'
        else:
            data['Ссылка на документы'] = 'Нет данных на сайте'

        print(f"[✓] Обработан: {full_link}")
        all_data.append(data)

    return all_data
