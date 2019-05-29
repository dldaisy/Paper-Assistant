# Example:
# from crawler import query
# results = query(search_query="quantum", max_chunk_results=1, max_results=5)
# for result in results:
#     print(result)
# acm:
# from crawler import get_acm
#     results = get_acm(100)
# for result in results:
#     print(result)

import csv
import feedparser
from urllib.parse import urlencode
from urllib.request import urlretrieve

class Search(object):
    root_url = 'http://export.arxiv.org/api/'

    def __init__(self, query=None, id_list=None, max_results=None, sort_by=None, sort_order=None, max_chunk_results=None, time_sleep=3):

        self.query = query
        self.id_list = id_list
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.max_chunk_results = max_chunk_results
        self.time_sleep = time_sleep
        self.max_results = max_results

        if not self.max_results:
            print('No maximal number of results given by the user. Download all')
            self.max_results = float('inf')

    def _get_url(self, start=0, max_results=None):

        url_args = urlencode(
            {
                "search_query": self.query,
                "id_list": self.id_list,
                "start": start,
                "max_results": max_results,
                "sortBy": self.sort_by,
                "sortOrder": self.sort_order
            }
        )

        return self.root_url + 'query?' + url_args

    def _parse(self, url):
        """
        Downloads the data provided by the REST endpoint given in the url.
        """
        result = feedparser.parse(url)

        if result.get('status') != 200:
            print("HTTP Error {} in query".format(result.get('status', 'no status')))
            return []
        return result['entries']

    def _get_next(self):
        n_left = self.max_results
        start = 0

        while n_left > 0:

            url = self._get_url( start=start, max_results=min(n_left, self.max_chunk_results))
            results = self._parse(url)
            n_fetched = len(results)

            if n_fetched == 0:
                print('Fetching finished.')
                break

            n_left = n_left - n_fetched
            start = start + n_fetched

            yield results

    def crawl(self):
        results = []
        for result in self._get_next():
            results += result
        for result in results:
            result['abstract'] = result.pop('summary')
            result['comment'] = ''
            result['authors'] = ','.join([x['name'] for x in result.pop('authors')])
        return results

def query(search_query="", id_list=[], max_results=None, sort_by="relevance", sort_order="descending", max_chunk_results=1000):

    search = Search(
        query=search_query,
        id_list=','.join(id_list),
        sort_by=sort_by,
        sort_order=sort_order,
        max_results=max_results,
        max_chunk_results=max_chunk_results)

    return search.crawl()

def get_acm(max_results=None):
    csv_url = 'https://dl.acm.org/feeds/acm_kbart.csv'

    filename='acm_kbart.csv'
    keys = []
    results = []
    urlretrieve(csv_url, filename)
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        dict = {}
        cnt = 0
        for row in csv_reader:
            for x in row.keys():
                dict[x] = row[x]
            results.append(dict)
    return results
