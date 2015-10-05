import logging
import requests

from .exceptions import InvalidDataException

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
            res = self.client.session.get(next_url)
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
        return self.from_json(self.client.session.get(url).json())
        
    def get(self, url, cached=False):
        if not cached or url not in self._cache:
            self._cache[url] = self._get(url)
        return self._cache[url]

    def delete(self, url):
        response = self.client.session.delete(url)
        return response.status_code == 204

    def create(self, **kwargs):
        response = self.client.session.post(self.list_path, json=kwargs)
        if response.status_code == 201:
            data = response.json()
            self._cache[data['self']] = self.from_json(data)
            return self._cache[data['self']]
        elif response.status_code == 400:
            raise InvalidDataException(response.json())
