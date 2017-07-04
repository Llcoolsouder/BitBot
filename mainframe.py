import sqlite3
import time
import os
import requests
import json

from apscheduler.schedulers.background import BackgroundScheduler

def add_table(db_name, table_name):
    db = sqlite3.connect(db_name)
    curs = db.cursor()
    curs.execute("DROP TABLE IF EXISTS " + table_name + ";")
    curs.execute("CREATE TABLE " + table_name +
                 """(tdatetime DATETIME, rank INT, price_usd REAL, price_btc REAL,
                 \"24h_volume_usd\" REAL, market_cap_usd REAL, available_supply REAL,
                 total_supply REAL, percent_change_1h REAL, percent_change_24h REAL, percent_change_7d REAL);""")
    db.commit()
    db.close()

def query_database(table, rank, price_usd,
                  price_btc, volume_usd_24h, market_cap_usd, available_supply,
                  total_supply, percent_change_1h, percent_change_24h, percent_change_7d
                  ):

    ticker = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=20')
    ticker = ticker.content
    json_ticker = json.loads(ticker)
    for i in json_ticker:
        if i['id'] not in coincap_coins:
            coincap_coins.append(i['id'])
        coincap_data[i['id']] = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(i['name'], i['symbol'], i['rank'], i['price_usd'], i['price_btc'], i['24h_volume_usd'], i['market_cap_usd'], i['available_supply'], i['total_supply'], i['percent_change_1h'], i['percent_change_24h'], i['percent_change_7d'], i['last_updated'])
        print(i['id'])

    db = sqlite3.connect('test.db')
    curs = db.cursor()
    tdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
    curs.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (tdatetime, rank, price_usd, price_btc, volume_usd_24h, market_cap_usd,
                  available_supply, total_supply, percent_change_1h, percent_change_24h, percent_change_7d))
    db.commit()
    db.close()
    print ("It worked")
    

if __name__ == '__main__':
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(query_database, 'cron',args=['bitcoin', 1, 700, 1, 15000,
                                     16000000, 0, 17000000, 2, 1.5, 0.2], minute='*/5')
    scheduler.start()
    print ('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(30)
            add_table('test.db', 'ethereum')
            print ("Other Thread")
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        


