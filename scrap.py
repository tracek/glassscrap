import time

from bs4 import BeautifulSoup






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


def parse_reviews_HTML(reviews):
    data = []
    for review in reviews:
        date = review.find("time", { "class" : "date" }).getText().strip()
        data.append(date)
    return data


if __name__ == '__main__':

    companyName = "sandvik"
    companyURL = "https://www.glassdoor.com/Reviews/Sandvik-Reviews-E10375.htm"



    total_pages = get_total_pages(driver=driver, url=companyURL)

    # HTML = driver.page_source
    # soup = BeautifulSoup(HTML, "html.parser")
    # reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})

    d = []

    for page_no in range(1, total_pages):
        print('Processing page: {}'.format(page_no))
        currentURL = '{}_P{}.htm'.format(companyURL[:companyURL.rfind('.')], page_no)
        driver.get(currentURL)
        some_int = randint(5, 10)
        driver.execute_script("window.scrollTo(0, {})".format(100 * some_int))
        time.sleep(some_int)
        HTML = driver.page_source

        with open(currentURL[currentURL.rfind('/') + 1:], 'w') as f:
            f.write(HTML)
    #     soup = BeautifulSoup(HTML, "html.parser")
    #     reviews = soup.find_all("li", {"class": ["empReview", "padVert"]})
    #     dates = parse_reviews_HTML(reviews)
    #     d.extend(dates)
