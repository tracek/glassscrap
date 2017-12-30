import csv
import os
import json
from urllib import parse
from collections import namedtuple, OrderedDict
from bs4 import BeautifulSoup
from localcrawler import LocalCrawler
from webcrawler import WebCrawler

Review = namedtuple('Review', ['datetime', 'maintext', 'jobtitle', 'location', ])


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
    themes = ['Work_Life_Balance',
              'Culture_and_Values',
              'Career_Opportunities',
              'Compensation_and_Benefits',
              'Senior_Management']
    ratings_html = review.find_all('span', {'class': "gdBars gdRatings med "})
    ratings = {theme: int(float(rating.attrs['title'])) for theme, rating in zip(themes, ratings_html)}
    return ratings


def get_jobtitle(review):
    title = review.find('span', {'class': 'authorJobTitle middle reviewer'})
    title = title.text if title else 'Unknown'
    return title


def get_location(review):
    location = review.find('span', {'class': 'authorLocation middle'})
    location = location.text if location else 'Unknown'
    return location


def get_recommendations(review):
    recommendations = 'Not present'
    t = review.find('div', {'class': 'flex-grid recommends'})
    if t:
        recommendations_html = t.find_all('span', class_='middle')
        if recommendations_html:
            recommendations = {'Recommendation_{}'.format(idx+1): rec.getText()
                                for idx, rec in enumerate(recommendations_html)}
    return recommendations


def get_maintext(review):
    main_text = review.find('p', {'class': ' tightBot mainText'})
    main_text = main_text.text.replace(u'\xa0', u' ') if main_text else 'Not present'
    return main_text


def get_pros(review):
    pros = review.find('p', {'class': ' pros mainText truncateThis wrapToggleStr'})
    pros = pros.text if pros else 'None'
    return pros


def get_cons(review):
    cons = review.find('p', {'class': ' cons mainText truncateThis wrapToggleStr'})
    cons = cons.text if cons else 'None'
    return cons


def get_advice(review):
    advice = review.find('p', {'class': 'dviceMgmt mainText truncateThis wrapToggleStr truncatedThis pointer'})
    advice = advice.text if advice else 'None'
    return advice


def parse_review(review):
    d = {'datetime': get_datetime(review),
         'maintext': get_maintext(review),
         'jobtitle': get_jobtitle(review),
         'location': get_location(review),
         'recommendations': get_recommendations(review),
         'ratings': get_ratings(review),
         'pros': get_pros(review),
         'cons': get_cons(review),
         'advice': get_advice(review)
         }
    return d


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



    # HTML = driver.page_source
    # soup = BeautifulSoup(HTML, "html.parser")
    # reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
    # datetime = get_datetime(review)
    # maintext = get_maintext(review)
    # jobtitle = get_jobtitle(review)
    # location = get_location(review)
    # recommendations = get_recommendations(review)
    # ratings = get_ratings(review)
    # pros = get_pros(review)
    # cons = get_cons(review)
    # advice = get_advice(review)