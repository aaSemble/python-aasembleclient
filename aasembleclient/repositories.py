from .base import BaseResourceManager
from cliff.lister import Lister

class Repository(object):
    @property
    def sources(self):
        return self.client.Sources.list(self.sources_url)

class RepositoryManager(BaseResourceManager):
    object_class = Repository
    path = '/repositories/'

    def from_json(self, data):
        obj = self.object_class()
        obj.self = data['self']
        obj.user = data['user']
        obj.name = data['name']
        obj.sources_url = data['sources']
        obj.client = self.client
        return obj


class List(Lister):
    """ List all repositories """

    def take_action(self, parsed_args):
        return (('Id', 'User', 'Name'),
                [(r.self, r.user, r.name) for r in self.app.client.Repositories.list()])
