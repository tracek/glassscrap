import re

def infer_country(location):
    country = 'Unknown'
    if location:
        search = re.search(r'\((.*?)\)', location)
        if search:
            country = search.group(1)
        else:
            country = 'United States of America'
            state = location[-2:]
            code = 'US-' + state