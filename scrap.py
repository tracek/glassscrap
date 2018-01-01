from urllib import parse
from csv import DictWriter
from bs4 import BeautifulSoup
from tqdm import tqdm
from localcrawler import LocalCrawler
from webcrawler import WebCrawler
from parser import parse_review, get_header


def get_crawler(uri):
    if parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri)
    else:
        scraper = LocalCrawler(uri)
    return scraper


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    output_csv = 'sandvik.csv'
    crawler = get_crawler(uri)

    with open(output_csv, 'wt', encoding='utf-8') as fp:
        writer = DictWriter(fp, fieldnames=get_header(), delimiter=',')
        writer.writeheader()
        for page in tqdm(crawler.get_page(), total=crawler.total_pages):
            soup = BeautifulSoup(page, "lxml")
            reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
            for review in reviews:
                result = parse_review(review)
                writer.writerow(result)