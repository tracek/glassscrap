# Ethical web crawler for Glassdoor

What is "ethical" when it comes to web crawling is subjective and debatable, but the way I understand it is that the crawler simply automates some user actions; it does not produce heavier traffic nor tries to parse the web site from the root level. In this case it simply takes the company we are interested in and extracts relevant fields. Later it enriches the data set with structured location information.

## Installation

Set versions:

```bash
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
SELENIUM_STANDALONE_VERSION=3.8.0
SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)
```

Set up virtualenv:
```bash
mkvirtualenv scrapy
pip install -r requirements.txt
```

Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
```

Install Chrome if needed be:
```bash
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
```

Install ChromeDriver:

```bash
wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver
```
