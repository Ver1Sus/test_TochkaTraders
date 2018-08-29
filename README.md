# test_TochkaTraders








How to use:
	<ol>
	<li>Activate env:</li>
		<b>source env/bin/activate</b>
	<li>To run spider for updating base:</li>
		<b>cd scrapyTest/scrapyTest/spiders/</b>
		<b>scrapy crawl testParse</b>		
	<li>Run server:</li>
		<b>python main.py</b>
	</ol>

P.S. Уже поздно понял что выбрал не подходящую либу для парсинга, с помощью нее не получилось использовать мультипоточность для ускорения работы. 
На различных форумах советуют использовать асинхронный способ, типа aioHTTP, т.к. многопоточность не сильно ускоряет парсинг, а асинхронное ожидание ответа страницы дает ощутимый прирост скорости - но возможно это не так - нужно тестировать.
	

