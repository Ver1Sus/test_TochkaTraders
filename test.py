import postgreDB
import asyncio
from sqlalchemy import create_engine



dbPostgre = postgreDB.Base()
# dbPostgre.connect()
# print(dbPostgre.execute("SELECT * FROM tochka_history"))
# dbPostgre.insertHistory( '2018-08-14', 'Text', 1, 2.2)
# dbPostgre.close()


fileName = 'tickers.txt'
with open(fileName, "r") as f:
	urls = ['https://www.nasdaq.com/symbol/{}/historical'.format(traderName.replace('\n','')) for traderName in f]
	print (urls)

	
	
	
# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
engine = create_engine('postgresql+psycopg2://tocka_user:test1234@localhost/tochka_flask')
connection = engine.connect()


result = connection.execute("select * from tochka_history")
for row in result:
    print("trade_date:", row['trade_date'])
connection.close()










