import requests
from bs4 import BeautifulSoup
from headers import get_random_headers
import re
import time
from headers import get_random_headers, get_cookies
import os

def parse_product(url_list, title):
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip()

    BASE_FOLDER = os.path.join('products', safe_title)
    PHOTOS_FOLDER = os.path.join(BASE_FOLDER, 'photos')
    os.makedirs(PHOTOS_FOLDER, exist_ok=True)

    headers = get_random_headers()
    cookies = get_cookies()
    
    all_data = []

    for full_link in url_list:
        response = requests.get(full_link, headers=headers, cookies=cookies)
        
        time.sleep(1)
        if response.status_code != 200:
            print(f"Ошибка при загрузке товара: {full_link}")
            continue
        
        time.sleep(1)
        
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



        data['Ссылки на фото'] = 'Нет данных на сайте'
        image_urls = []

        photo_block = soup.find('ul', class_='product-card-gallery-thumbs-list')
        if photo_block:
            photo_links = photo_block.find_all('a', href=True)
            image_urls = ['https:' + a['href'] for a in photo_links]

        if not image_urls:
            main_image_div = soup.find('div', class_='product-card-gallery-image-container')
            if main_image_div:
                main_img = main_image_div.find('img', src=True)
                if main_img:
                    image_urls = ['https:' + main_img['src']]

        # Сохраняем ссылки
        if image_urls:
            data['Ссылки на фото'] = '\n'.join(image_urls)

            # Создаём папку для фото
            raw_title = data.get('Заголовок', 'unknown')
            safe_title = re.sub(r'[^\w\-_\. ]', '_', raw_title)[:50]
            folder_name = os.path.join(PHOTOS_FOLDER, f'{safe_title.strip().replace(" ", "_")}')
            os.makedirs(folder_name, exist_ok=True)
            data['Папка с фото'] = folder_name


            for idx, img_url in enumerate(image_urls, start=1):
                try:
                    img_response = requests.get(img_url, headers=headers, cookies=cookies, timeout=10)
                    if img_response.status_code == 200:
                        ext = os.path.splitext(img_url)[1] or ".jpg"
                        img_path = os.path.join(folder_name, f'image_{idx}{ext}')
                        with open(img_path, 'wb') as f:
                            f.write(img_response.content)
                    else:
                        print(f"[!] Не удалось скачать изображение: {img_url}")
                except Exception as e:
                    print(f"[!] Ошибка при скачивании изображения: {img_url}\n{e}")



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

        print(f"Обработан: {full_link}")
        all_data.append(data)

    return all_data
