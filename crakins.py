import tornado.ioloop
import tornado.web
import os.path
import sqlite3 as db
import time, datetime, pytz

    
class MainHandler(tornado.web.RequestHandler):

	def get(self):
		imagePath = "/images/crakinscom.png"
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


handlers = [
	(r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "/home/rakins/Dev/crakins_tornado/images"}),
	(r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "/home/rakins/Dev/crakins_tornado/css"}),
	(r"/", MainHandler),
]

settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
