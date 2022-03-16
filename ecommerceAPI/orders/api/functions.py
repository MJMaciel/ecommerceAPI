import json
import requests


def get_dollar_price():
    response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if response.status_code == 200:
        for r in response.json():
            if r['casa']['nombre'] == 'Dolar Blue':
                return float(r['casa']['venta'].replace(',', '.'))



if __name__ == '__main__':
    value = get_dollar_price()
    print(value)