import psycopg2
from settings import config

'''
	###--- How to use:

	dbPostgre = postgreDB.Base(dbname = 'test_base')
	dbPostgre.connect()
	dbPostgre.execute("SELECT * FROM test_table")
	dbPostgre.insert(( 'Text', 'Add new', '2018-08-14 06:20:36'))
	dbPostgre.close()

'''


class Base():
	def __init__(self):
		cfg = config['postgres']
		self.dbname = cfg['database']
		self.user = cfg['user']
		self.host = cfg['host']
		self.password = cfg['password']
	
	def connect(self):
		self.con = psycopg2.connect(dbname=self.dbname, password=self.password, user=self.user, host=self.host)
		return self.con
		
	def execute(self, query):
		##--- open cursor and select all 
		cur = self.con.cursor()
		cur.execute(query)
		res = cur.fetchall()
		cur.close()
		return res
		
		
	def insertHistory(self, trade_date='2018-08-22', traderName='test', open=0.0, high=0.0, low=0.0, close_last=0.0, vol=0):
		with self.connect() as con:
			with self.con.cursor() as cur:
				cur.execute("INSERT INTO tochka_history(trade_date, trader_name, open, high, low, close_last, vol) " \
					" VALUES('{}', '{}', {}, {}, {}, {}, {})".format(trade_date, traderName, open, high, low, close_last, vol))

		return self.con.commit()
		
	def insertHistory_td(self, traderName, tdList):
		with self.connect() as con:
			with self.con.cursor() as cur:
				cur.execute("UPDATE tochka_history SET "\
					" trade_date='{0}', trader_name='{1}', open={2}, high={3}, low={4}, close_last={5}, vol={6}"\
					" WHERE trade_date='{0}' and trader_name='{1}';".format(tdList[0], traderName, tdList[1], tdList[2], tdList[3], tdList[4], tdList[5]))
				cur.execute("INSERT INTO tochka_history(trade_date, trader_name, open, high, low, close_last, vol) " \
					" SELECT '{0}', '{1}', {2}, {3}, {4}, {5}, {6} "\
					" WHERE NOT EXISTS "\
						"(SELECT 1 FROM tochka_history WHERE trade_date='{0}' and trader_name='{1}' and open={2} and high={3} and low={4} and close_last={5} and vol={6});"\
					.format(tdList[0], traderName, tdList[1], tdList[2], tdList[3], tdList[4], tdList[5]))
		
		return self.con.commit()
		
		
	def insertInsider_td(self, traderName, tdList):
		with self.connect() as con:
			with self.con.cursor() as cur:
				# cur.execute("UPDATE tochka_insider SET "\
					# " trade_date='{0}', trader_name='{1}', open={2}, high={3}, low={4}, close_last={5}, vol={6}"\
					# " WHERE trade_date='{0}' and trader_name='{1}';".format(tdList[0], traderName, tdList[1], tdList[2], tdList[3], tdList[4], tdList[5]))
				cur.execute("INSERT INTO tochka_insider(trader_name, insider_name, relation, last_date, transaction_type, owner_type, shares_traded, price, shares_held) " \
					" SELECT '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8} "\
					" WHERE NOT EXISTS "\
						"(SELECT 1 FROM tochka_insider WHERE trader_name='{0}' and insider_name='{1}' and relation='{2}' and last_date='{3}' and transaction_type='{4}' and owner_type='{5}' and shares_traded={6} and price={7} and shares_held={8})"\
					.format( traderName, tdList[0], tdList[1], tdList[2], tdList[3], tdList[4], tdList[5], tdList[6], tdList[7]))
		
		return self.con.commit()
		
		
	def getMainUrls(self):
		with self.connect() as con:
			with self.con.cursor() as cur:
				cur.execute("SELECT DISTINCT trader_name FROM tochka_history;")
				res = cur.fetchall()
		
		return res
		
	def getTrader(self, trader_name):
		with self.connect() as con:
			with self.con.cursor() as cur:
				cur.execute("SELECT  trade_date, open, high, low, close_last, vol FROM tochka_history WHERE trader_name='{}'".format(trader_name))
				res = cur.fetchall()
		
		return res
		
		
		
	def close(self):
		self.con.close()
	