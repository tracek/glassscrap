import urllib
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler


def get_crawler(uri):
    if urllib.parse.urlparse(uri).scheme in ('http', 'https',):
        scraper = WebCrawler(uri)
    else:
        scraper = LocalCrawler(uri)
    return scraper


def get_datetime(review):
    datetime = review.find("time").attrs['datetime']
    return datetime


def get_ratings(review):
    themes = ['Work Life Balance',
              'Culture and Values',
              'Career Opportunities',
              'Compensation and Benefits',
              'Senior Management']
    ratings_html = review.find_all('span', {'class': "gdBars gdRatings med "})
    ratings = {theme: int(float(rating.attrs['title'])) for theme, rating in zip(themes, ratings_html)}
    return ratings


def get_title(review):
    title = review.find('span', {'class': 'authorJobTitle middle reviewer'}).getText()
    return title


def get_location(review):
    location = review.find('span', {'class': 'authorLocation middle'}).getText()
    return location


def get_recommendations(review):
    t = review.find('div', {'class': 'flex-grid recommends'})
    recommendations_html = t.find_all('span', class_='middle')
    recommendations = {'Recommendation {}'.format(idx+1): rec.getText()
                        for idx, rec in enumerate(recommendations_html)}
    return recommendations


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    crawler = get_crawler(uri)

    for page in crawler.get_page():
        soup = BeautifulSoup(page, "html.parser")
        reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
        for review in reviews:
            rat = get_ratings(review)


    # HTML = driver.page_source
    # soup = BeautifulSoup(HTML, "html.parser")
    # reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
