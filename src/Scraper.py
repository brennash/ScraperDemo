import os
import sys
import time
import json
import logging
import dryscrape
from random import randint
from optparse import OptionParser
from logging.handlers import RotatingFileHandler

class Scraper:


	def __init__(self):

		self.logger   = None
		self.logFile  = None
		self.dataDir  = None

		self.loginURL  = None
		self.logoutURL = None
		self.username  = None
		self.password  = None
		self.baseURL   = None


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

				self.username  = data['username']
				self.password  = data['password']
				self.baseURL   = data['base-url']
				self.loginURL  = data['login-url']
				self.logoutURL = data['logout-url']
				self.logFile   = data['log-file']
				self.dataDir   = data['data-dir']
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
			handler.setLevel(logging.INFO)
			self.logger.addHandler(handler)
			self.logger.setLevel(logging.INFO)
			self.logger.info('Starting logging..')
		except Exception, err:
			errorStr = 'Error initializing log file, ',err
			print self.logFile
			print errorStr
			exit(1)

	def startScraper(self):

		validPages = []

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

			session.visit('http://www.greyhound-data.com/d?r=4159265')
			rawHTML = session.source()
			self.saveHTML(session.url(), rawHTML)
			exit(1)
#			session.visit(self.baseURL)

#			currentURL = session.url()
#			rawHTML    = session.source()

			# extract all links
#			for link in session.xpath('//a[@href]'):
#				urlLink = link['href']
#				if 'd?r=' in urlLink:
#					validPages.append(link)
#					session.visit(link['href'])
#					rawHTML = session.source()
#					self.saveHTML(link['href'], rawHTML)

#
#			if self.logger is not None:
#				self.logger.info('Added {0} links to follow.'.format(len(validPages)))

#			for link in validPages:
#				if self.logger is not None:
#					self.logger.info('Clicking on link {0}'.format(link['href']))
#				link.hover()
#				link.click()
#				time.sleep(randint(1,4))
#				rawHTML = session.source()

#				if 'Because of constant attacks on our server' in rawHTML:
#					print 'Cannot follow link, because of login'
#					name = session.at_xpath('//*[@name="user_email"]')
#					name.set(self.username)
#					password = session.at_xpath('//*[@name="user_password"]')
#					password.set(self.password)
#					name.form().submit()


#				self.saveHTML(session.url(), rawHTML)
#				exit(1)
#
#			session.visit('self.logoutURL')

			# save a screenshot of the web page
			# session.render('hounds.png')
			# print("Screenshot written to 'hounds.png'")
		except KeyError, err:
			if self.logger is None:
				print 'Error scraping data - {0}'.format(str(err))
			else:
				self.logger.error('Error scraping data - {0}'.format(str(err)))


	def saveHTML(self, url, html):
		raceNumber = self.getRaceNumber(url)
		filename = '{0}/race_{1}.html'.format(self.dataDir, raceNumber)

		if self.dataDir is not None:
			try:
				if self.logger is not None:
					self.logger.info('Saving HTML (length: {0}) for race {1}'.format(len(html),raceNumber))
				file = open(filename,"wb")
				file.write(html)
				file.close()
				print 'Writing html ({0}) to file {1}'.format(len(html), filename)
			except Exception, err:
				if self.logger is None:
					print 'Problem writing html to file'
				else:
					self.logger.error('Problem writing html to file ({0}) - {1}'.format(filename, err))

	def getRaceNumber(self, url):
		if 'r=' in url:
			startIndex = url.index('r=')
			numberStr  = url[(startIndex+3):]
			tokens     = numberStr.split('&')
			return tokens[0]
		else:
			return randint(99999999,99999999999999)

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
