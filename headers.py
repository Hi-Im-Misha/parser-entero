import random

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://entero.ru/",
    },
    # можешь добавить ещё разные заголовки
]

COOKIES = [
    {
    "_userGUID": "0:mdai6e5f:g1C7sRexMisr~t2L~z3Yd~MFtZFE~g6u",
    "_ym_uid": "1752944974988944562",
    "_ym_d": "1752944974",
    "cookies_popup": "1",
    "PHPSESSID": "6eb87997810da4e2a8086d1a048ad5e7",
    "yaDClientId": "1752944974988944562",
    "_ym_isad": "2",
    "_ym_visorc": "w",
    "_gid": "GA1.2.1389432637.1754322018",
    "_gat_gtag_UA_88584430_1": "1",
    "_ga": "GA1.1.975467151.1752944976",
    "_gat_UA-88584430-1": "1",
    "_ga_DMP7RC8YVT": "GS2.1.s1754322018$o12$g1$t1754322068$j10$l0$h0",
    "RCPC": "e78ae92880d35c2d99ebc80364f13af3"
    }
]
def get_random_headers():
    return random.choice(HEADERS_LIST)

def get_cookies():
    return random.choice(COOKIES)
