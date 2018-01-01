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
