import requests
from bs4 import BeautifulSoup
from headers import get_random_headers

def pars_url(base_url):
    page = 1
    product_links = []

    while True:
        url = f"{base_url}?p={page}" if page > 1 else base_url
        headers = get_random_headers()
        print(f"[+] Обработка страницы: {url}")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Страница {url} не доступна: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        product_blocks = soup.find_all('div', class_='product-wrapper')

        if not product_blocks:
            print(f"[✓] Товаров на странице {page} больше нет. Завершаем.")
            break

        for product in product_blocks:
            a_tag = product.find('a', class_='product-image')
            if a_tag and 'href' in a_tag.attrs:
                product_link = a_tag['href']
                full_link = 'https://entero.ru' + product_link
                product_links.append(full_link)
        
        page += 1

    return product_links
