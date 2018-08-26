'''
	How to run: 
	> scrapy crawl testParse


'''


import scrapy
from urllib.parse import urljoin
import datetime
import re
import sys
sys.path.insert(0, '../../../')
import postgreDB




		
def convertDate(dateStr):
	'''
		return now time if get time, not last date, or if the get error when try convert
	'''
	if ':' in dateStr:
		return datetime.datetime.now().strftime('%Y-%m-%d')
	try:
		return datetime.datetime.strptime(dateStr, '%m/%d/%Y').strftime('%Y-%m-%d')
	except:
		print(sys.exc_info())
		return datetime.datetime.now().strftime('%Y-%m-%d')
		

		
		
		
def updateTrList(trList):
	'''
		Example of tr:
			['08/20/2018', '118', '2,118.32', '117.33', '117.75', '5,393,835']
		need:
			- formate date from mm/dd/yyyy to yyy-mm-dd/yyyy
			- update element to int		
	'''
	trNew = []
	for tr in trList:
		tdList = [x.strip().replace(',','') for x in tr]
		tdList[0] = convertDate(tdList[0])
						
		trNew.append(tdList)
		
	return trNew	

	
def updateTrListInsider(trList):
	'''
		Example of tr:
			(Insider, 	Relation 	
			Last Date,	Transaction Type, 	OwnerType,
			Shares Traded, 	Last Price, 	Shares Held)
			
			['<td><a href="..">JOHNSON JAMES WILLIAM</a></td>', '<td>Officer</td>', 
			'<td>05/22/2018</td>', '<td>Option Execute</td>', '<td>direct</td>', 
			'<td>9,500</td>', '<td>69.7000</td>', '<td>9,500</td>']
			
		need:
			- get name from <a></a> 
				(re.findall(r'">\w+ \w+ \w+',a))
				(re.findall(r'\b[A-Z]\w+', a)

			- formate date from mm/dd/yyyy to yyy-mm-dd/yyyy
			- update element to int		
	'''
	trNew = []
	for tr in trList:
		tdList = [x.strip().replace(',','').replace('<td>','').replace('</td>','') for x in tr]
		tdList = [x if x else '0' for x in tdList] ##-- if get empty element
		tdList[0] = " ".join(re.findall(r'\b[A-Z]\w+', tdList[0]))
		tdList[2] = convertDate(tdList[2])
						
		trNew.append(tdList)
		
	return trNew	


class PycoderSpider(scrapy.Spider):
	name = "testParse"
	
	##--- open file tickers.txt with list of traders, and get list with urls
	fileName = '../../../tickers.txt'
	
	# start_urls = [ 'https://www.nasdaq.com/symbol/cvx/historical', 
				# 'https://www.nasdaq.com/symbol/aapl/historical', 
		# ]
	start_urls = []
		
	with open(fileName, "r") as f:
		# start_urls = ['https://www.nasdaq.com/symbol/{}/historical'.format(traderName.replace('\n','')) for traderName in f]
		# for i in range(10):
			# start_urls += ['https://www.nasdaq.com/symbol/{}/insider-trades?page={}'.format(traderName.replace('\n',''), i) for traderName in f]
		
		for line in f:
			# start_urls += ['https://www.nasdaq.com/symbol/{}/historical'.format(line.replace('\n',''))]
			for i in range(10):
				start_urls += ['https://www.nasdaq.com/symbol/{}/insider-trades?page={}'.format(line.replace('\n','').lower(), i+1)]		
		
		print(start_urls)
	
	
	

	def parse(self, response):
        # for post_link in response.xpath(
                # '//div[@class="post mb-2"]/h2/a/@href').extract():
            # url = urljoin(response.url, post_link)
            # print(url)
			
		dbPostgre = postgreDB.Base()	
		
		# for quote in response.css('div.genTable'):
			# yield {
				# 'text': quote.css('span.text::text').extract_first(),
				# 'author': quote.css('small.author::text').extract_first(),
				# 'tags': quote.css('div.tags a.tag::text').extract(),
			# }
		
		traderName = re.findall(r'symbol/(\w+)',response.request.url)[0]
		
		div = response.css('div.genTable')
		if (re.findall(r'symbol/\w+/(\w+)',response.request.url)[0]) == 'historical':
		
			trList = div.xpath("div/table/tbody/tr")
		
			trList = [x.xpath("td/text()").extract() for x in trList]
			
			trNew = updateTrList(trList)
			
			
			print("*"*8)
			print(trNew[0])
			traderName = re.findall(r'symbol/(\w+)',response.request.url)[0]
			
			#----- push in DB all values
			[dbPostgre.insertHistory_td( traderName, td) for td in trNew]
			# dbPostgre.insertHistory_td( traderName, trNew[0])
			print("*"*8)
		elif (re.findall(r'symbol/\w+/(\w+)',response.request.url)[0]) == 'insider':
			
			# trList = div.xpath("table/tbody/tr")#.extract()
			trList = div.xpath("table/tr")
			trList = [x.xpath("td").extract() for x in trList]
			
			trNew = updateTrListInsider(trList)
			
			print("*"*8)
			# print(trList)
			print(response.request.url, trNew[0])
			#----- push in DB all values
			[dbPostgre.insertInsider_td( traderName, td) for td in trNew]
			# dbPostgre.insertInsider_td( traderName, trNew[0])
			print("*"*8)
		
		##--- save the page in file
		# page = response.url.split("/")[-2]
		# filename = 'quotes-%s.html' % page
		# with open(filename, 'wb') as f:
			# f.write(response.body)
		# self.log('Saved file %s' % filename)
		
		
		
		
		
	
		
		
		
		
		
		
