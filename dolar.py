import bs4
import requests
import re

def get_float(text):
	text = text.replace(',', '.')
	float_regex = re.compile(r'\d+(\.\d+)?')
	float_value = float(re.search(float_regex, text)[0])
	return float_value


def valor_dolar_blue():
	req = requests.get('https://www.dolarhoy.com/cotizaciondolarblue').text
	soup = bs4.BeautifulSoup(req, 'html.parser')
	valor_dolar_container = soup.find('div', class_ = 'venta')
	valor_c=soup.find('div', class_ = 'compra')

	if valor_dolar_container != None:
		valor_venta = get_float(valor_dolar_container.text)
		valor_compra=get_float(valor_c.text)
		return valor_compra,valor_venta

	else:
		return -1
