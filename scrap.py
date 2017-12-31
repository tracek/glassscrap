import os
from urllib import parse
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler
from parser import parse_review
from iohelper import save_as_csv, save_as_json
from csv import DictWriter

def get_crawler(uri):
    if parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri)
    else:
        scraper = LocalCrawler(uri)
    return scraper


header = [
    'datetime',
    'maintext',
    'jobtitle',
    'location_region',
    'location_region-code',
    'location_sub-region',
    'location_sub-region-code',
    'location_country',
    'location_country-code',
    'location_US_state_code',
    'location_city',
    'location_location_raw',
    'ratings_Senior_Management',
    'ratings_Work_Life_Balance',
    'ratings_Culture_and_Values',
    'ratings_Compensation_and_Benefits',
    'ratings_Career_Opportunities',
    'recommendations_Recommendation_1',
    'recommendations_Recommendation_2',
    'recommendations_Recommendation_3',
    'pros',
    'cons',
    'advice'
]


def save_as_csv(result, path):
    global HEADER
    with open(path, 'at', encoding='utf-8') as fp:
        d = _flatten_json(result)
        if not HEADER:
            HEADER = d.keys()
            writer = DictWriter(fp, HEADER)
            writer.writeheader()
        else:
            writer = DictWriter(fp, HEADER)
        writer.writerow(d)


def _flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    output_json = 'sandvik.json'
    output_csv = 'sandvik.csv'

    if os.path.exists(output_json):
        os.remove(output_json)
    if os.path.exists(output_csv):
        os.remove(output_csv)

    crawler = get_crawler(uri)

    counter = 0

    with open('test.csv', 'wt', encoding='utf-8') as fp:
        writer = DictWriter(fp, fieldnames=header, delimiter=',')
        writer.writeheader()
        for page in crawler.get_page():
            soup = BeautifulSoup(page, "lxml")
            reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
            for review in reviews:
                print(counter)
                result = parse_review(review)
                save_as_json(result, path=output_json)
                flat = _flatten_json(result)
                writer.writerow(flat)
                counter += 1

            # save_as_csv(result, path=output_csv)
