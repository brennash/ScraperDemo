import os
import sys
import json
import logging
import dryscrape
from optparse import OptionParser
from logging.handlers import RotatingFileHandler

class Scraper:


	def __init__(self):

		self.logger   = None
		self.logFile  = None

		self.loginURL = None
		self.username = None
		self.password = None
		self.baseURL  = None


	def run(self, jsonConfigFilename):
		""" Use a separate run function to enable class-wide
		    testing.
		"""

		# Load the config file first
		self.loadConfig(jsonConfigFilename)

		# Then setup the logging
		self.setupLogging()

		# Now launch the scraper
		if self.baseURL is not None:
			self.startScraper()

	def loadConfig(self, jsonConfigFilename):
		try:
			with open(jsonConfigFilename,"r") as json_file:
     				data = json.load(json_file)

				self.username = data['username']
				self.password = data['password']
				self.baseURL  = data['base-url']
				self.loginURL = data['login-url']
				self.logFile  = data['log-file']

		except Exception, err:
			print 'Problem with JSON config ({0}).'.format(jsonConfigFilename)
			print str(err)
			print 'Exiting...'
			exit(1)

	def setupLogging(self):
		""" 
		Sets up the logging function to write data to the log folder with a rotating file logger.
		"""
		try:
			self.logger = logging.getLogger(__name__)
			handler = RotatingFileHandler(self.logFile, maxBytes=500000, backupCount=5)
			format  = "%(asctime)s %(levelname)-8s %(message)s"
			handler.setFormatter(logging.Formatter(format))
			handler.setLevel(self.logLevel)
			self.logger.addHandler(handler)
			self.logger.setLevel(self.logLevel)
		except Exception, err:
			errorStr = 'Error initializing log file, ',err

	def startScraper(self):

		#dryscrape.start_xvfb()
		#sess = dryscrape.Session(base_url = self.loginURL)
		#sess.set_attribute('auto_load_images', False)
		#sess.visit(self.loginURL)
		#q = sess.at_xpath('user_email')
		#q.set(self.username)
		#p = sess.at_xpath('user_password')
		#p.set(self.username)
		#q.form().submit()

		try:
			dryscrape.start_xvfb()
			session = dryscrape.Session()
			session.set_attribute('auto_load_images', False)
			session.visit(self.loginURL)
			name = session.at_xpath('//*[@name="user_email"]')
			name.set(self.username)
			password = session.at_xpath('//*[@name="user_password"]')
			password.set(self.password)
			name.form().submit()
			session.visit(self.baseURL)

			# extract all links
			for link in session.xpath('//a[@href]'):
				print(link['href'])

			# save a screenshot of the web page
			session.render('hounds.png')
			print("Screenshot written to 'hounds.png'")
		except Exception, err:
			if self.logger is None:
				print 'Error scraping data - {0}'.format(str(err))
			else:
				self.logger.error('Error scraping data - {0}'.format(str(err)))




def main(argv):
        parser = OptionParser(usage="Usage: Scraper <json-config-filename>")
        (options, filename) = parser.parse_args()

	if len(filename) == 1:
		if os.path.exists(filename[0]):
			runner = Scraper()
			runner.run(filename[0])
		else:
			parser.print_help()
			print '\nYou need to provide an existing JSON config file.'
			exit(1)
	else:
		parser.print_help()
		print '\nYou need to provide an existing JSON config file.'
                exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
