import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://finance.yahoo.com/quote/%5EGSPC/history?period1=1268179200&period2=1665360000&interval=1d&filter' \
      '=history&frequency=1d&includeAdjustedClose=true'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}

FILE = 's_and_p_index_data_1.csv'


def get_html(url, params=None):
    r = requests.get(url, timeout=30,  headers=HEADERS, params=params, stream=True)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_quote_data = soup.find_all('table', class_='W(100%) M(0)')
    data = []
    for item in items_quote_data:
        one_day_data = item.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')
        for values in one_day_data:
            date = values.find('td', class_='Py(10px) Ta(start) Pend(10px)').get_text().replace(',', '')
            # all data has the same class, so it will pass through find_all
            prices = values.find_all('td', class_='Py(10px) Pstart(10px)')
            for i, price in enumerate(prices):
                if i == 0:
                    open = price.get_text().replace(',', '')
                if i == 1:
                    high = price.get_text().replace(',', '')
                if i == 2:
                    low = price.get_text().replace(',', '')
                if i == 3:
                    close = price.get_text().replace(',', '')
                if i == 4:
                    adj_close = price.get_text().replace(',', '')
                if i == 5:
                    volume = price.get_text().replace(',', '')
            data.append({
                'date': date, 'open': open, 'high': high, 'low': low,
                'close': close, 'adj_close': adj_close, 'volume': volume
            })
    return data


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([
            'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
        for item in items:
            writer.writerow(
                [item['date'], item['open'], item['high'], item['low'],
                 item['close'], item['adj_close'], item['volume']])


def calculate_periods():
    period_1 = 1656633600
    period_2 = 1664496000
    diff = 7862400
    periods = []
    i = int(0)
    while i < 200:
        periods.append({'period_1': period_1, 'period_2': period_2})
        period_2 -= diff
        period_1 -= diff
        i += 1
    return periods


def parse():
    data = []
    periods = calculate_periods()
    for counter in range(len(periods)):
        html = get_html('https://finance.yahoo.com/quote/%5EGSPC/history?period1=' + str(
            periods[counter]['period_1']) + '&period2=' + str(periods[counter][
                                                                  'period_2']) + '&interval=1d&filter' + '=history&frequency=1d&includeAdjustedClose=true')

        data.extend(get_content(html.text))
        save_file(data, FILE)


parse()
