import argparse

from .base import BaseResourceManager
from .repositories import RepositoryManager
from cliff.lister import Lister

class Mirror(object):
    pass


class MirrorManager(BaseResourceManager):
    object_class = Mirror
    path = '/mirrors/'
    
    def from_json(self, data):
        obj = self.object_class()
        obj.client = self.client
        obj.self = data['self']
        obj.url = data['url']
        obj.series = data['series']
        obj.components = data['components']
        return obj


class MirrorLister(Lister):
    def format_mirrors(self, mirrors):
        data = []

        for mirror in mirrors:
            data.append((mirror.self, mirror.url, ' '.join(mirror.series), ' '.join(mirror.components)))

        return (('Id', 'URL', 'Series', 'Components'), data)

class List(MirrorLister):
    """ List all mirrors """

    def take_action(self, parsed_args):
        return self.format_mirrors(self.app.client.Mirrors.list())


#class ListByRepository(SourceLister):
#    """ List all sources for given repository """
#
#    def get_parser(self, prog_name):
#        parser = super(ListByRepository, self).get_parser(prog_name)
#        parser.add_argument('id')
#        return parser
#
#   
#    def take_action(self, parsed_args):
#        repository = self.app.client.Repositories.get(parsed_args.id)
#        return self.format_sources(repository.sources)
