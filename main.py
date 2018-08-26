# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
# from view import IndexView
from postgreDB import Base
from header	import updateHistoryToJson
from sqlalchemy import create_engine
import datetime
from dateutil.relativedelta import relativedelta
# from copy import deepcopy
# from app import create_app

# app = create_app()
# IndexView.register(app)
app = Flask(__name__)
base = Base()

#--- connect to Base, using the SQLAlchemy
engine = create_engine('postgresql+psycopg2://tocka_user:test1234@localhost/tochka_flask')
# connection = engine.connect()

##---- Task 2
@app.route("/")
def hello():
	res = base.getMainUrls()
	urls = [traderName[0] for traderName in res]

	print(res)
	return render_template("./index.html", title='List of traders', urls=urls, description='List of traders')
	
	
##---- Task 3
@app.route("/<string:trader_name>")
def trader(trader_name):
	# res = base.getTrader(trader_name)
	# resJson = updateHistoryToJson(res)
	# print(resJson)
	
	connection = engine.connect()
	
	# result = connection.execute("SELECT DISTINCT trader_name FROM tochka_history "\
		# " WHERE trade_date >= '{}'".format((datetime.datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d')))
	
	# print(trader_name, result)
	# if  trader_name in result:
		# print ("GOTHCA")
	
	##--- get the history of trader_name, on last 3 month
	result = connection.execute("select * from tochka_history "\
		" where trader_name='{}' and trade_date >= '{}' "\
		" order by trade_date desc".format(
			trader_name, 
			(datetime.datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') 
			))
	connection.close()
	
	# for row in result:
		# row['trade_date'] = row['trade_date'].strftime('%Y-%m-%d')
		# print("trade_date:", type(row['trade_date']))
		
	# res2 = deepcopy(result)
	# resultJson = updateHistoryToJson(res2)
	print(result)
	# print(resJson)
	return render_template("./trader.html", title='Trader {}'.format(trader_name), trader_name=trader_name, resJson=result, description='Trader')


###--- Task 4
@app.route("/<string:trader_name>/insider")
def insider(trader_name):
	
	connection = engine.connect()
	
	
	##--- get the history of trader_name, on last 3 month
	result = connection.execute("select * from tochka_insider "\
		" where trader_name='{}'  "\
		" order by id desc".format(trader_name))
	connection.close()
	
	# for row in result:
		# row['trade_date'] = row['trade_date'].strftime('%Y-%m-%d')
		# print("trade_date:", type(row['trade_date']))
		
	# res2 = deepcopy(result)
	# resultJson = updateHistoryToJson(res2)
	print(result)
	# print(resJson)
	return render_template("./insider.html", title='Trader {}'.format(trader_name), trader_name=trader_name, resJson=result, description='Trader')

	
	
	
##---- Task 6
@app.route("/<string:trader_name>/analytics", methods=['GET'])
def traderAnalytics(trader_name):
	date_from = request.args.get('date_from')
	date_to = request.args.get('date_to')
	
	##--- check if GET here
	if date_to and date_from:
		##-- check if correct date
		try:
			datetime.datetime.strptime(date_from, '%Y-%m-%d')
		except:
			return "Incorrect date_from format. Need YYY-MM-DD"
			
		try:
			datetime.datetime.strptime(date_to, '%Y-%m-%d')
		except:
			return "Incorrect date_to format. Need YYY-MM-DD"
			
		##-- all OK, get data from base
		connection = engine.connect()
	
		result = connection.execute("SELECT table_from.trader_name, table_to.open - table_from.open as open, table_to.high-table_from.high as high, table_to.low-table_from.low as low, table_to.close_last - table_from.close_last as close_last, table_to.vol-table_from.vol as vol "\
			" FROM (select * from tochka_history where trader_name='{0}' and trade_date='{1}' ) as table_from, "\
			" (select * from tochka_history where trader_name='{0}' and trade_date='{2}' ) as table_to "\
			.format(trader_name, date_from, date_to))			
		
		connection.close()
	else:
		return "Please, add GET parametres data_to and data_from, like: /aapl/analytics?date_from=2018-08-01&date_to=2018-08-02"
			
		
	return render_template("./traderAnalytics.html", title='Trader {}'.format(trader_name), trader_name=trader_name, result=result, description='Trader Analytics. Between {} and {}'.format(date_from, date_to))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
##---- Run the server
if __name__ == '__main__':
	app.run(host='192.168.1.127',port=50001)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	