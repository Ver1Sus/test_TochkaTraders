

class IndexView(FlaskView):
	
	@route("/")
	def hello():
		return "Hello"