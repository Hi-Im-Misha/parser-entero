import openpyxl
import os

def save_to_excel(data_list, title):
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip()

    folder_path = os.path.join("products", safe_title)
    filename = os.path.join(folder_path, f"{safe_title}.xlsx")

    os.makedirs(folder_path, exist_ok=True)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Товары"

    if not data_list:
        print("Список данных пустой")
        return

    headers = list(data_list[0].keys())
    sheet.append(headers)

    for item in data_list:
        row = [item.get(header, "") for header in headers]
        sheet.append(row)

    workbook.save(filename)
    print(f"Excel сохранён: {filename}")
