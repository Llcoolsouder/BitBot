import sqlite3
import time
import os
import json
import requests

from apscheduler.schedulers.background import BackgroundScheduler

def add_table(db_name, table_name):
    db = sqlite3.connect(db_name)
    curs = db.cursor()
    curs.execute("DROP TABLE IF EXISTS [" + table_name + "];")
    curs.execute("CREATE TABLE [" + table_name +
                 """] (tdatetime DATETIME, rank INT, price_usd REAL, price_btc REAL,
                 \"24h_volume_usd\" REAL, market_cap_usd REAL, available_supply REAL,
                 total_supply REAL, percent_change_1h REAL, percent_change_24h REAL, percent_change_7d REAL);""")
    db.commit()
    db.close()
    print("Added " + table_name + " to " + db_name)


def get_tables_from(db):
    db = sqlite3.connect(db)
    curs = db.cursor()
    res = curs.execute("""SELECT name FROM sqlite_master WHERE TYPE=\'table\'""")
    res = curs.fetchall()
    db.close()

    tables = []
    for i in range(len(res)):
        temp = str(res[i])
        temp=temp[2:len(temp)-3]
        tables.append(temp)
    return tables


def add_data_to(database, table, rank, price_usd,
                  price_btc, volume_usd_24h, market_cap_usd, available_supply,
                  total_supply, percent_change_1h, percent_change_24h, percent_change_7d
                  ):
    
    db = sqlite3.connect(database)
    curs = db.cursor()
    tdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
    curs.execute("INSERT INTO [" + table + "] VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (tdatetime, rank, price_usd, price_btc, volume_usd_24h, market_cap_usd,
                  available_supply, total_supply, percent_change_1h, percent_change_24h, percent_change_7d))
    db.commit()
    db.close()
    print ("Data added to " + database + ', ' + table)


def query_coinmarketcap(db):
    
    coins = get_tables_from(db)
    ticker = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=20')
    json_ticker = ticker.json()
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    for i in json_ticker:
        if i['id'] not in coins:
            add_table(db, i['id'])
        add_data_to(db, i['id'], i['rank'], i['price_usd'], i['price_btc'], i['24h_volume_usd'], i['market_cap_usd'], i['available_supply'],
                    i['total_supply'], i['percent_change_1h'], i['percent_change_24h'], i['percent_change_7d'])
    print('\n')
    

if __name__ == '__main__':
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(query_coinmarketcap, 'cron',args=['coins.db'], minute ='*/5')
    scheduler.start()
    print ('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        


