import bs4
import requests
import re


def get_float(text):
    text = text.replace(',', '.')
    float_regex = re.compile(r'\d+(\.\d+)?')
    float_value = float(re.search(float_regex, text)[0])
    return float_value


def valor(url):
    req = requests.get(url).text
    soup = bs4.BeautifulSoup(req, 'html.parser')
    cotizacion_div = soup.find('div', class_='cotizacion_moneda')
    valor_compra, valor_venta = cotizacion_div.find_all('div', class_='value')
    act = cotizacion_div.find('span')

    if valor_venta is not None:
        valor_venta = get_float(valor_venta.text)
        valor_compra = get_float(valor_compra.text)
        return valor_compra, valor_venta, act.text

    else:
        return -1
