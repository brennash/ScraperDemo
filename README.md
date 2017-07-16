# ScraperDemo
Web Scraper Demo, using Python with headless browsers.


## Installation
The installation is best done on a clean AWS EC2 instance. 

<pre>
sudo apt-get update
sudo apt-get install virtualenv python-pip
sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
git clone <Scraper-Demo-SSH-URI>
cd ScraperDemo
virtualenv venv
. venv/bin/activate
pip install dryscrape logging
</pre>

## Running the Scraper
In the conf folder, change your username/password to whatever you use to login to the site. Also, 
if you've installed the repository somewhere else, you might need to change the log folder location too.
Once you've done all that, then scraping the site is as simple as

<pre>
python src/Scraper conf/myconfig.json
</pre>

The output data should be then written to the data folder as raw HTML (parsed HTML to CSV to come later). 
