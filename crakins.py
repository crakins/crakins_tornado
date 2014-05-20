import tornado.ioloop
import tornado.web
import os.path
import sqlite3 as db
import time, datetime, pytz
from riverlevel import get_level

    
class MainHandler(tornado.web.RequestHandler):

	def get(self):
		imagePath = "images/crakinscom.png"
		self.render("index.html", imagePath=imagePath)
		
	def post(self):
		# Get email address from form
		email = self.get_argument("email")
		# Get timestamp
		email_timestamp = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S')
		# connect to database
		connection = db.connect('emails.db')
		cur = connection.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS emails (email TEXT, timestamp TEXT)")
		# store in database
		with connection:
			cur.execute("INSERT INTO emails VALUES (?, ?)", (email, email_timestamp))
		# close database connection
		connection.close()
		self.redirect("/", status=303)

class RiverHandler(tornado.web.RequestHandler):

	def get(self):
		corivers = {'Browns Canyon': '07091200', 'Pine Creek': '07087050', 'The Numbers': '07087050', 'Royal Gorge': '07094500', 'Upper East' : '09112200', 'Daisy Creek' : '09111500', 'Slate' : '09111500' }
		levels = {}		
		for k, v in corivers.items():
			levels[k] = get_level(v)	
		self.render("corivers.html", levels=levels)

handlers = [
	(r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "images"}),
	(r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "css"}),
	(r"/", MainHandler),
	(r"/rivers", RiverHandler),
]

settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

application = tornado.web.Application(handlers, debug=True, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
