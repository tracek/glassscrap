import re
import csv
import functools


@functools.lru_cache(maxsize=1)
def get_country_mapping():
    with open('country-mapping.csv') as fp:
        reader = csv.DictReader(fp)
        country_mapping = {line['name']: {'region': line['region'],
                                          'region-code': line['region-code'],
                                          'sub-region': line['sub-region'],
                                          'sub-region-code': line['sub-region-code'],
                                          'country': line['name'],
                                          'country-code': line['alpha-2']} for line in reader}
    return country_mapping


def get_geoinfo(location):
    mapping = get_country_mapping()
    if location:
        search = re.search(r'\((.*?)\)', location)
        if search:
            country = search.group(1)
            result = mapping[country]
            result['US_state_code'] = None
        else:
            result = mapping['United States of America']
            state = location[-2:]
            code = 'US-' + state
            result['US_state_code'] = code
        result['location_raw'] = location
    else:
        result = None
    return result


if __name__ == '__main__':
    mapping = get_country_mapping()
    print(mapping['Poland'])