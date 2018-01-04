import re
import csv
import functools


class LocatorException(Exception):
    pass


@functools.lru_cache(maxsize=1)
def get_country_mapping() -> dict:
    """
    Read mapping from csv and cache
    :return: dictionary with ISO country mapping
    """
    with open('country-mapping.csv') as fp:
        reader = csv.DictReader(fp)
        country_mapping = {line['name']: {'region': line['region'],
                                          'region_code': line['region-code'],
                                          'sub_region': line['sub-region'],
                                          'sub_region_code': line['sub-region-code'],
                                          'country': line['name'],
                                          'country_code_2': line['alpha-2'],
                                          'country_code_3': line['alpha-3']
                                          } for line in reader}
    return country_mapping


def get_non_us_city(location: str) -> str:
    """
    Deals with two types of non-US locations:
    "New Delhi (India)" and "Perth, Western Australia (Australia)"
    :param location: geo location of the person
    :return city
    :raises LocatorException: could not infer the city name
    """
    sep_idx = location.find(',')
    if sep_idx != -1:
        # case: "Perth, Western Australia (Australia)"
        city = location[:sep_idx]
    else:
        city_last_idx = location.find('(')
        if city_last_idx == -1:
            raise LocatorException('Could not infer the city name from {}'.format(location))
        else:
            city = location[:city_last_idx - 1]
    return city


def get_geoinfo(location: str) -> dict:
    """
    Infer geographical ISO information from location
    :param location: geo location of the person
    :return: dictionary with ISO geo-information
    """
    mapping = get_country_mapping()
    if location:
        search = re.search(r'\((.*?)\)', location)
        if search:
            country = search.group(1)
            result = mapping[country]
            result['US_state_code'] = 'NULL'
            result['city'] = get_non_us_city(location)
        else:
            result = mapping['United States of America']
            city, state = [x.strip() for x in location.split(',')]
            code = 'US-' + state
            result['US_state_code'] = code
            result['city'] = city
        result['location_raw'] = location
    else:
        result = {}
    return result


if __name__ == '__main__':
    mapping = get_country_mapping()
    print(mapping['Poland'])