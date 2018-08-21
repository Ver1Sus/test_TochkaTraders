import postgreDB
import asyncio



dbPostgre = postgreDB.Base()
# dbPostgre.connect()
# print(dbPostgre.execute("SELECT * FROM tochka_history"))
# dbPostgre.insertHistory( '2018-08-14', 'Text', 1, 2.2)
# dbPostgre.close()


fileName = 'tickers.txt'
with open(fileName, "r") as f:
	urls = ['https://www.nasdaq.com/symbol/{}/historical'.format(traderName.replace('\n','')) for traderName in f]
	print (urls)