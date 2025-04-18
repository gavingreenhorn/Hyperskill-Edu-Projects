import requests


ex_rates = dict()


def get_exchange_rate(_c_data, _ex_curr):
    ex_rate = _c_data.get(_ex_curr)['rate'] if _ex_curr != c_code else 1
    return ex_rate


c_code = input('Enter your currency code (e.g. USD, EUR): ').lower()
if c_code and len(c_code) == 3:
    r = requests.get(f'http://www.floatrates.com/daily/{c_code}.json')
else:
    print('Incorrect currency code format')

if r:
    json_data = r.json()
    ex_rates['usd'] = get_exchange_rate(json_data, 'usd')
    ex_rates['eur'] = get_exchange_rate(json_data, 'eur')
    while True:
        ex_curr = input('Enter exchange currency code: ').lower()
        if not ex_curr:
            print('No value entered')
            continue
        elif ex_curr == 'exit':
            break
        elif ex_curr.isnumeric() or len(ex_curr) != 3:
            print('Incorrect currency code format')
            continue
        try:
            ex_amount = float(input('Enter the amount of money you want to exchange: '))
        except:
            print('Incorrect value')
            continue
        if not ex_rates.get(ex_curr.lower()):
            ex_rates[ex_curr] = get_exchange_rate(json_data, ex_curr)
        ex_result = ex_rates[ex_curr] * ex_amount
        print(f'You received {ex_result:.2f} {ex_curr.upper()}')
else:
    print('Wrong currency code or resource unavailable')
