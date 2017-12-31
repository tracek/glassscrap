import json
from csv import DictWriter

HEADER = False


def save_as_json(result, path):
    with open(path, 'at', encoding='utf-8') as fp:
        res_json = json.dumps(result, ensure_ascii=False)
        fp.write(res_json + '\n')


def save_as_csv(result, path):
    global HEADER
    with open(path, 'at', encoding='utf-8') as fp:
        d = _flatten_json(result)
        if not HEADER:
            HEADER = d.keys()
            writer = DictWriter(fp, HEADER)
            writer.writeheader()
        else:
            writer = DictWriter(fp, HEADER)
        writer.writerow(d)


def _flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
