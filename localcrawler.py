__copyright__ = """

    Copyright 2018 Lukasz Tracewski

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import glob


class LocalCrawler(object):

    def __init__(self, path):
        self.pages_visited = 0
        self.path = path
        self.pages = glob.glob(path + '/*.htm')
        if not self.pages:
            raise FileNotFoundError('No files found on the path: {}'.format(path))
        self.total_pages = len(self.pages)

    def get_page(self):
        for page in self.pages:
            with open(page, 'r') as f:
                self.pages_visited += 1
                yield f.read()


if __name__ == '__main__':
    crawler = LocalCrawler('www')
