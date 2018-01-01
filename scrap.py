from urllib import parse
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler
from parser import parse_review
from csv import DictWriter

def get_crawler(uri):
    if parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri)
    else:
        scraper = LocalCrawler(uri)
    return scraper


header = [
    'date',
    'jobtitle',
    'currently_employed',
    'fulltime',
    'min_years_employment',
    'region',
    'region-code',
    'sub-region',
    'sub-region-code',
    'country',
    'country-code',
    'US_state_code',
    'city',
    'location_raw',
    'rating_Senior_Management',
    'rating_Work_Life_Balance',
    'rating_Culture_and_Values',
    'rating_Compensation_and_Benefits',
    'rating_Career_Opportunities',
    'ceo_opinion',
    'recommends',
    'company_outlook',
    'pros',
    'cons',
    'advice'
]


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    output_csv = 'sandvik.csv'
    crawler = get_crawler(uri)

    with open(output_csv, 'wt', encoding='utf-8') as fp:
        writer = DictWriter(fp, fieldnames=header, delimiter=',')
        writer.writeheader()
        for page in crawler.get_page():
            soup = BeautifulSoup(page, "lxml")
            reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
            for review in reviews:
                result = parse_review(review)
                writer.writerow(result)