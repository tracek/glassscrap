import csv
import os
import json
from urllib import parse
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler
from parser import parse_review


def get_crawler(uri):
    if parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri)
    else:
        scraper = LocalCrawler(uri)
    return scraper


def save_as_json(results, path):
    with open(path, 'a') as fp:
        res_json = json.dumps(results)
        fp.write(res_json + '\n')


def save_complete_as_json(results, path='results.json'):
    with open(path, 'a') as fp:
        json.dump(results, fp)


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    output_json = 'sandvik.json'

    if os.path.exists(output_json):
        os.remove(output_json)

    crawler = get_crawler(uri)
    results = []

    for page in crawler.get_page():
        soup = BeautifulSoup(page, "html.parser")
        reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
        for review in reviews:
            result = parse_review(review)
            save_as_json(result, path=output_json)
