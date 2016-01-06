import tornado.ioloop
import tornado.web
#import tornado.torndb
import os.path
import sqlite3 as db
import time, datetime, pytz
from riverlevel import get_level, get_level_cswc

def _execute(query):
    dbPath = '/home/dev/crakins_tornado/emails.db'
    connection = db.connect('emails.db')
    cur = connection.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        connection.commit()
    except Exception:
        raise
    connection.close()
    return result

class User(tornado.web.RequestHandler):

    def get(self):
        cookiename = "crakins"
        if not self.get_cookie(cookiename):
            self.set_cookie(cookiename, str(time.time()))
            self.write("Cookie is now set")
        else:
            self.write("Cookie is " + cookiename)
	
    
class MainHandler(tornado.web.RequestHandler):

	def get(self):
		imagePath = "images/crakinscom.png"
		self.render("index.html", imagePath=imagePath)

class RiverHandler(tornado.web.RequestHandler):

	def get(self):
		# get levels from USGS
		corivers = {'Browns Canyon': '07091200', 'Pine Creek': '07087050', 'The Numbers': '07087050', 'Upper East' : '09112200', 'Daisy Creek' : '09111500', 'Slate' : '09111500' }
		levels = {}
		levels_cswc = {}
		for k, v in corivers.items():
			levels[k] = get_level(v)
		# get levels from colorado's suface water conditions
		corivers_cswc = {'Clear Creek of Ark' : 'CCACCRCO', 'Royal Gorge' : 'ARKWELCO'}
		for k, v in corivers_cswc.items():
			levels_cswc[k] = get_level_cswc(v)
		self.render("corivers.html", levels=levels, levels_cswc = levels_cswc)

class ShowEmailHandler(tornado.web.RequestHandler):
    def get(self):
        query = 'select * from emails'
        rows = _execute(query)
        self._processresponse(rows)
    
    def _processresponse(self, rows):
        self.write("<b>Records</b> <br /><br />")
        for row in rows:
            self.write(str(row[0]) + "  " + str(row[1]) + "<br />")
        

class EmailHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('success.html')        
        
    def post(self):
        # save email to database
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
		# set cookie to success message
		message = "Success! I will be in contact soon."
		#self.set_secure_cookie("flash", message)
		self.redirect("/email")

class AddEmail(tornado.web.RequestHandler):
    def get(self):
        self.render('add.html')
    
    def post(self):
        email = self.get_argument("email")
        email_timestamp = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S')
        query = "'insert into emails (email, timestamp) values (email, email_timestamp)'"
        _execute(query)
        self.set_secure_cookie("flash", message)
        self.render('success.html')

class ComingSoon(tornado.web.RequestHandler):
    def get(self):
        self.render('comingsoon.html')

handlers = [
	(r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "images"}),
	(r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "css"}),
	(r"/", MainHandler),
	(r"/rivers", RiverHandler),
	(r"/email", EmailHandler),
	(r"/add", AddEmail),
	(r"/user", User),
	(r"/showemails", ShowEmailHandler),
	(r"/comingsoon", ComingSoon),
]

settings = {
			"template_path": os.path.join(os.path.dirname(__file__), "templates"),
			"xsrf_cookies": False,
}


application = tornado.web.Application(handlers, debug=True, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
