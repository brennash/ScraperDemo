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
pip install dryscrape
</pre>
