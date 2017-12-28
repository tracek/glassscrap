import glob

class LocalCrawler(object):

    def __init__(self, path):
        self.pages_visited = 0
        self.path = path
        self.pages = glob.glob(path + '/*.htm')
        self.total_pages = self.get_total_pages()

    def get_total_pages(self):
        return len(self.pages)

    def get_page(self):
        for page in self.pages:
            with open(page, 'r') as f:
               yield f.read()

    def __next__(self):
        pass

    def open(self, url):
        pass

    def __iter__(self):
        return self


if __name__ == '__main__':
    crawler = LocalCrawler('www')
