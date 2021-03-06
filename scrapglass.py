#!/usr/bin/env python

__copyright__ = """

    Copyright 2018 Lukasz Tracewski

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import argparse
from urllib import parse
from csv import DictWriter
from bs4 import BeautifulSoup
from tqdm import tqdm
from localcrawler import LocalCrawler
from webcrawler import WebCrawler
from glassparser import parse_review, get_header


def get_crawler(uri: str, chrome_driver_path, dump_to_local):
    if parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri, chrome_driver_path, dump_to_local)
    else:
        scraper = LocalCrawler(uri)
    return scraper


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parse Glassdoor reviews.')
    argparser.add_argument('--skipheader', action='store_true', help='Skip writing header to the file')
    argparser.add_argument('--dump', action='store_true', help='Dump the web pages to the local directory. Only relevant for web addresses.')
    argparser.add_argument('-s', '--source', help='Path to the reviews (either local or web e.g. '
                                                  'https://www.glassdoor.com/Reviews/Google-Reviews-E9079.htm', required=True)
    argparser.add_argument('-d', '--dest', help='Destination: local path (incl. filename), defaults to review.csv', default='review.csv')
    argparser.add_argument('--driver', help='Path to the chrome driver (see installation instruction on github). '
                                            'Defaults to /usr/local/bin/chromedriver', default="/usr/local/bin/chromedriver")
    args = argparser.parse_args()
    crawler = get_crawler(args.source, args.driver, args.dump)

    with open(args.dest, 'wt', encoding='utf-8', newline='\n') as fp:
        # Replace None with "NULL" so that MySQL interprets is as NULL (otherwise it is parsed as empty string)
        writer = DictWriter(fp, fieldnames=get_header(), delimiter=',', restval='NULL', lineterminator='\n')
        if not args.skipheader:
            writer.writeheader()
        for page in tqdm(crawler.get_page(), total=crawler.total_pages):
            soup = BeautifulSoup(page, "lxml")
            reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
            for review in reviews:
                result = parse_review(review)
                writer.writerow(result)