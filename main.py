from pars_url import pars_url
from pars_product import parse_product
from excel import save_to_excel

if __name__ == "__main__":
    try:
        url = 'https://entero.ru/list/1470'
        product_links, title = pars_url(url)

        print(f"Найдено товаров: {len(product_links)}")
        product_data = parse_product(product_links, title)

        save_to_excel(product_data, title)
        print("Готово. Данные сохранены в Excel.")
    except Exception as e:
        print(f"Ошибка выполнения: {e}")