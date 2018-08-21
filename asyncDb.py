import asyncio
import aiopg
			
			
class PostgreDB():
	def __init__(self):
		from settings import config
		config = config['postgres']
		self.dsn = dsn = 'dbname={} user={} password={} host={}'.format(config['database'], config['user'], config['password'], config['host'])

	async def getStatus(self):
		##-- get last status of checkbox 
		pool = await aiopg.create_pool(self.dsn)
		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute("SELECT * from test_table order by test_table.click_time desc limit 1")
				async for row in cur:
					print(row[0])
					self.statusActive = row[0]
					# print (row)
					return(row)		

	async def insert(self, check, click_time):
		#-- update status of checkbox
		pool = await aiopg.create_pool(self.dsn)
		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute("INSERT INTO test_table VALUES({}, '{}')".format(check, str(click_time)))
	
	def insertHistory(self, trade_date='2018-08-22', traderName='test', open=0.0, high=0.0, low=0.0, close_last=0.0, vol=0):
		pool = aiopg.create_pool(self.dsn)
		print(pool)
		with pool.acquire() as conn:
			with conn.cursor() as cur:
				cur.execute("INSERT INTO test_table(trade_date, trader_name, open, high, low, close_last, vol) "/
				" VALUES('{}', '{}', {}, {}, {}, {}, {})".format(str(trade_date), traderName, open, high, low, close_last, vol))
	
		pool.close()
	
	
			