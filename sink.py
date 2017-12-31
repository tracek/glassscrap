import json
import csv
import os

def flatten_json(y):
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

class FileWriter(object):

    def __init__(self, path, output_format='csv,json', delete_old=True):
        output_format = output_format.replace(' ', '')
        self.json_path = path + '.json' if 'json' in output_format else None
        self.csv_path = path + '.csv' if 'csv' in output_format else None
        if not (self.json_path or self.csv_path):
            raise NotImplementedError('Format {} is not implemented'.format(output_format))
        if delete_old:
            for format in output_format.split(','):
                p = path + '.' + format
                if os.path.exists(p):
                    os.remove(p)
        if self.json_path:
            self.json_fp = open(self.json_path, 'a')
        if self.csv_path:
            self.csv_fp = open(self.csv_path, 'a')

    def write(self):
        if self.json_path:
            self.json_fp.write('test')
            self.json_fp.close()
        if self.csv_path:
            self.csv_fp.write('test2')
            self.csv_fp.close()

    def __del__(self):
        if self.json_path:
            self.json_fp.close()
        if self.csv_path:
            self.csv_fp.close()


if __name__ == '__main__':
    writer = FileWriter('test', output_format='csv')
    writer.write()