import re
from locator import get_geoinfo
from bs4.element import Tag


def get_header() -> list:
    header = [
        'date',
        'jobtitle',
        'currently_employed',
        'fulltime',
        'min_years_employment',
        'region',
        'region_code',
        'sub_region',
        'sub_region_code',
        'country',
        'country_code',
        'US_state_code',
        'city',
        'location_raw',
        'rating_Senior_Management',
        'rating_Work_Life_Balance',
        'rating_Culture_and_Values',
        'rating_Compensation_and_Benefits',
        'rating_Career_Opportunities',
        'ceo_opinion',
        'ceo_opinion_num',
        'recommends',
        'recommends_num',
        'company_outlook',
        'company_outlook_num',
        'pros',
        'cons',
        'advice'
    ]
    return header


def parse_review(review: Tag) -> dict:
    """
    Extract user review from HTML
    :param review: html document (bs4.element.Tag) with user review
    :return: dictionary with user review info
    """
    d = {'date': _get_date(review),
         'pros': _get_pros(review),
         'cons': _get_cons(review),
         'advice': _get_advice(review)
         }

    location = _get_location(review)
    geoinfo = get_geoinfo(location)
    recommendations = _get_recommendations(review)
    ratings = _get_ratings(review)
    jobstatus = _get_jobstatus(review)
    exp = _get_exp(review)

    d.update(geoinfo)
    d.update(recommendations)
    d.update(ratings)
    d.update(jobstatus)
    d.update(exp)

    return d


def _get_date(review: Tag) -> str:
    date = review.find("time").attrs['datetime']
    return date


def _get_ratings(review: Tag) -> dict:
    themes = ['rating_Work_Life_Balance',
              'rating_Culture_and_Values',
              'rating_Career_Opportunities',
              'rating_Compensation_and_Benefits',
              'rating_Senior_Management']
    ratings_html = review.find_all('span', {'class': "gdBars gdRatings med "})
    ratings = {theme: int(float(rating.attrs['title'])) for theme, rating in zip(themes, ratings_html)}
    return ratings


def _get_jobstatus(review: Tag) -> dict:
    """
    The structure is assumed to always follow this pattern:
    Current Employee - something ..
    Former Employee - something ..
    e.g.: Current Employee - Sales Engineer, Former Employee - Anonymous Employee
    :param review: html document (bs4.element.Tag) with user review
    :return: dictionary with information on current employment (bool) and title (str)
    """
    title = review.find('span', {'class': 'authorJobTitle middle reviewer'}).text
    title = title.split(' ')
    current_employee = title[0] == 'Current'
    if title[3] == 'Anonymous':
        jobtitle = 'NULL'
    else:
        jobtitle = ' '.join(title[3:])

    d = {'currently_employed': current_employee, 'jobtitle': jobtitle}
    return d


def _get_location(review: Tag) -> str:
    location = review.find('span', {'class': 'authorLocation middle'})
    location = location.text if location else None
    return location


def _get_recommendations(review: Tag) -> dict:
    result = {}

    rec_map = {'Approves of CEO': ['ceo_opinion', 'Approves', 1],
               'Disapproves of CEO': ['ceo_opinion', 'Disapproves', -1],
               'No opinion of CEO': ['ceo_opinion', 'No opinion', 0],
               "Doesn't Recommend": ['recommends', False, -1],
               'Recommends': ['recommends', True, 1],
               'Negative Outlook': ['company_outlook', 'Negative', -1],
               'Neutral Outlook': ['company_outlook', 'Neutral', 0],
               'Positive Outlook': ['company_outlook', 'Positive', 1] }

    t = review.find('div', {'class': 'flex-grid recommends'})
    if t:
        recommendations_html = t.find_all('span', class_='middle')
        if recommendations_html:
            recommendations = [rec.get_text() for rec in recommendations_html]
            for rec in recommendations:
                rec_type = rec_map[rec][0]
                result[rec_type] = rec_map[rec][1]
                result[rec_type + '_num'] = rec_map[rec][2]

    return result


def _get_exp(review: Tag) -> dict:
    main_text = review.find('p', {'class': ' tightBot mainText'})
    main_text = main_text.text.replace(u'\xa0', u' ') if main_text else None
    if main_text:
        fulltime = True if 'full-time' in main_text else False
        years_employment = _get_num_years(main_text)
        d = {'fulltime': fulltime, 'min_years_employment': years_employment}
    else:
        d = {}

    return d


def _get_num_years(text: str) -> int:
    search = re.search(r'\((.*?)\)', text)
    if search:
        year_info_text = search.group(1)
        year_info = year_info_text.split(' ')
        if year_info[2] + ' ' + year_info[3] == 'a year':
            years = 1
        else:
            try:
                years = int(year_info[2])
            except ValueError:
                years = None
    else:
        years = None
    return years


def _get_pros(review: Tag) -> str:
    pros = review.find('p', {'class': ' pros mainText truncateThis wrapToggleStr'})
    pros = pros.get_text(separator=' | ') if pros else None
    return pros


def _get_cons(review: Tag) -> str:
    cons = review.find('p', {'class': ' cons mainText truncateThis wrapToggleStr'})
    cons = cons.get_text(separator=' | ') if cons else None
    return cons


def _get_advice(review: Tag) -> str:
    advice = review.find('p', {'class': ' adviceMgmt mainText truncateThis wrapToggleStr'})
    advice = advice.get_text(separator=' | ') if advice else None
    return advice

