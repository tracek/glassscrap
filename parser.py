from locator import get_geoinfo


def parse_review(review):
    location = _get_location(review)
    d = {'datetime': _get_datetime(review),
         'maintext': _get_maintext(review),
         'jobtitle': _get_jobtitle(review),
         'location': get_geoinfo(location),
         'recommendations': _get_recommendations(review),
         'ratings': _get_ratings(review),
         'pros': _get_pros(review),
         'cons': _get_cons(review),
         'advice': _get_advice(review)
         }
    return d


def _get_datetime(review):
    datetime = review.find("time").attrs['datetime']
    return datetime


def _get_ratings(review):
    themes = ['Work_Life_Balance',
              'Culture_and_Values',
              'Career_Opportunities',
              'Compensation_and_Benefits',
              'Senior_Management']
    ratings_html = review.find_all('span', {'class': "gdBars gdRatings med "})
    ratings = {theme: int(float(rating.attrs['title'])) for theme, rating in zip(themes, ratings_html)}
    return ratings


def _get_jobtitle(review):
    title = review.find('span', {'class': 'authorJobTitle middle reviewer'})
    title = title.text if title else None
    return title


def _get_location(review):
    location = review.find('span', {'class': 'authorLocation middle'})
    location = location.text if location else None
    return location


def _get_recommendations(review):
    recommendations = None
    t = review.find('div', {'class': 'flex-grid recommends'})
    if t:
        recommendations_html = t.find_all('span', class_='middle')
        if recommendations_html:
            recommendations = {'Recommendation_{}'.format(idx+1): rec.getText()
                                for idx, rec in enumerate(recommendations_html)}
    return recommendations


def _get_maintext(review):
    main_text = review.find('p', {'class': ' tightBot mainText'})
    main_text = main_text.text.replace(u'\xa0', u' ') if main_text else None
    return main_text


def _get_pros(review):
    pros = review.find('p', {'class': ' pros mainText truncateThis wrapToggleStr'})
    pros = pros.text if pros else None
    return pros


def _get_cons(review):
    cons = review.find('p', {'class': ' cons mainText truncateThis wrapToggleStr'})
    cons = cons.text if cons else None
    return cons


def _get_advice(review):
    advice = review.find('p', {'class': 'dviceMgmt mainText truncateThis wrapToggleStr truncatedThis pointer'})
    advice = advice.text if advice else None
    return advice

