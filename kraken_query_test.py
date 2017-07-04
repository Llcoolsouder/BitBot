from lxml import html
import requests
import json

print('TESTING TIME')
server_time = requests.get('https://api.kraken.com/0/public/Time')
time_tree = html.fromstring(server_time.content)

print("the time html is", time_tree)
print("the time string is", server_time)

print('TESTING ASSETS')
coins = ['XXBT', 'XETH', 'XXRP', 'XETC', 'XLTC', 'DASH', 'XXMR', 'XXLM', 'XZEC', 'XXDG']

print('Kraken Data')
kraken_file = open("kraken_coin_kraken.csv", 'a')
for i in coins:
    assets = requests.get('https://api.kraken.com/0/public/Assets?asset=%s'% i)
    assets = assets.content
    print(assets)
    assets = json.loads(assets)
    assets = assets['result'][i]
    aclass = assets['aclass']
    altname = assets['altname']
    decimals = assets['decimals']
    display_decimals = assets['display_decimals']
    print('aclass = ', aclass)
    print('altname = ', altname)
    print('decimals = ', decimals)
    print('display_decimals = ', display_decimals)
    kraken_file.write(aclass)
    kraken_file.write(',')
    kraken_file.write(altname)
    kraken_file.write(',')
    kraken_file.write(str(decimals))
    kraken_file.write(',')
    kraken_file.write(str(display_decimals))
    kraken_file.write('\n')
    
kraken_file.close()

print('CryptoCurrency Market Capitalizations Data')

coincap_coins = []
coincap_data = {}
coincap_file = open("coincap_data.csv", 'a')

ticker = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=20')
ticker = ticker.content
json_ticker = json.loads(ticker)
for i in json_ticker:
    if i['id'] not in coincap_coins:
        coincap_coins.append(i['id'])
    coincap_data[i['id']] = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(i['name'], i['symbol'], i['rank'], i['price_usd'], i['price_btc'], i['24h_volume_usd'], i['market_cap_usd'], i['available_supply'], i['total_supply'], i['percent_change_1h'], i['percent_change_24h'], i['percent_change_7d'], i['last_updated'])
    print(i['id'])

for key in coincap_data:
    coincap_file.write('%s,%s\n' %(key, coincap_data[key]))

coincap_file.close()
