import logging
import requests

class BaseResourceManager(object):
    def __init__(self, client):
        self.client = client
        self._cache = {}

    @property
    def list_path(self):
        return '%s%s' % (self.client.url, self.path)

    def list(self, url=None):
        if url is None:
            next_url = self.list_path
        else:
            next_url = url

        while next_url:
            logging.info('Fetching %s', next_url)
            res = self.client.session.get(next_url, auth=self.client.auth)
            try:
                data = res.json()
                for item in data['results']:
                    self._cache[item['self']] = self.from_json(item)
                    yield self._cache[item['self']]
                next_url = data.get('next', None)
            except Exception, e:
                print 'something went wrong', res, e
                raise

    def _get(self, url):
        logging.info('Fetching %s', url)
        return self.from_json(self.client.session.get(url, auth=self.client.auth).json())
        
    def get(self, url, cached=False):
        if not cached or url not in self._cache:
            self._cache[url] = self._get(url)
        return self._cache[url]
