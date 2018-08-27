
import json
import datetime


def updateHistoryToJson(res):
	'''
		res is list of tuples like this:
		(datetime.date(2018, 5, 21), 1074.06, 1088.0, 1073.65, 1079.58, 1012258)
		
		need perform it in json
	'''
	resJson = {'history':[]}
	for el in res:
		resJson['history'].append({
			# 'trade_date':el[0].strftime('%Y-%m-%d'),
			'trade_date':el[0],
			'open':el[1],
			'high':el[2],
			'low':el[3],
			'close_last':el[4],
			'vol':el[5]})
	return json.dumps(resJson)
	
def createApi(headers, res):
	resJson = {'root':[]}
	for el in res:
		innerElement = {}
		for i, columnName in enumerate(headers):
			##--- if get date - convert to string format
			if isinstance(el[i], datetime.date):
				innerElement[columnName] = el[i].strftime('%Y-%m-%d')
			else:
				innerElement[columnName] = el[i]
		resJson['root'].append(innerElement)
		
	return json.dumps(resJson)