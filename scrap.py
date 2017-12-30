from urllib import parse
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler


def get_crawler(uri):
    if parse.urlparse(uri).scheme in ('http', 'https',):
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


def get_jobtitle(review):
    title = review.find('span', {'class': 'authorJobTitle middle reviewer'})
    if title:
        title = title.text
    return title


def get_location(review):
    location = review.find('span', {'class': 'authorLocation middle'})
    if location:
        location = location.text
    return location


def get_recommendations(review):
    recommendations = None
    t = review.find('div', {'class': 'flex-grid recommends'})
    if t:
        recommendations_html = t.find_all('span', class_='middle')
        if recommendations_html:
            recommendations = {'Recommendation {}'.format(idx+1): rec.getText()
                                for idx, rec in enumerate(recommendations_html)}
    return recommendations


def get_maintext(review):
    main_text = review.find('p', {'class': ' tightBot mainText'})
    if main_text:
        main_text = main_text.text.replace(u'\xa0', u' ')
    return main_text


def get_pros(review):
    pros = review.find('p', {'class': ' pros mainText truncateThis wrapToggleStr'})
    if pros:
        pros = pros.text
    return pros


def get_cons(review):
    cons = review.find('p', {'class': ' cons mainText truncateThis wrapToggleStr'})
    if cons:
        cons = cons.text
    return cons


def get_advice(review):
    advice = review.find('p', {'class': 'dviceMgmt mainText truncateThis wrapToggleStr truncatedThis pointer'})
    if advice:
        advice = advice.text
    return advice

def parse_review(review):
    datetime = get_datetime(review)
    maintext = get_maintext(review)
    jobtitle = get_jobtitle(review)
    location = get_location(review)
    recommendations = get_recommendations(review)
    ratings = get_ratings(review)
    pros = get_pros(review)
    cons = get_cons(review)
    advice = get_advice(review)


if __name__ == '__main__':

    uri = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"
    uri = 'www'
    crawler = get_crawler(uri)

    for page in crawler.get_page():
        soup = BeautifulSoup(page, "html.parser")
        reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
        for review in reviews:
            datetime = get_datetime(review)
            maintext = get_maintext(review)
            jobtitle = get_jobtitle(review)
            location = get_location(review)
            recommendations = get_recommendations(review)
            ratings = get_ratings(review)
            pros = get_pros(review)
            cons = get_cons(review)
            advice = get_advice(review)


    # HTML = driver.page_source
    # soup = BeautifulSoup(HTML, "html.parser")
    # reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
