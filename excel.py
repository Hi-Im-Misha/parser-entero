import openpyxl

def save_to_excel(data_list, filename='products.xlsx'):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Товары"

    # Заголовки — берём из первого элемента словаря
    if not data_list:
        print("[!] Список данных пустой")
        return

    headers = list(data_list[0].keys())
    sheet.append(headers)

    for item in data_list:
        row = [item.get(header, "") for header in headers]
        sheet.append(row)

    workbook.save(filename)
    print(f"[✓] Excel сохранён: {filename}")
