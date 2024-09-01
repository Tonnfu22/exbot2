import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
SUPPORTED_COINS = {
    'bitcoin': 'BTC',
    'litecoin': 'LTC',
    'ethereum': 'ETH',
    'monero': 'XMR',
    'tether': 'USDT'
}

def get_crypto_price(coin):
    if coin not in SUPPORTED_COINS:
        return None
    params = {
        'ids': coin,
        'vs_currencies': 'usd'
    }
    response = requests.get(COINGECKO_API_URL, params=params)
    data = response.json()
    return data[coin]['usd'] if coin in data else None