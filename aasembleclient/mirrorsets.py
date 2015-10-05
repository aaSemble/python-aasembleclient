import argparse

from .base import BaseResourceManager
from .repositories import RepositoryManager
from cliff.lister import Lister

class MirrorSet(object):
    pass


class MirrorSetManager(BaseResourceManager):
    object_class = MirrorSet
    path = '/mirror_sets/'
    
    def from_json(self, data):
        obj = self.object_class()
        obj.client = self.client
        obj.self = data['self']
        obj.mirrors = [self.client.Mirrors.get(url, cached=True)
                       for url in data['mirrors']]
        return obj


class MirrorSetLister(Lister):
    def format_mirrorsets(self, mirrorsets):
        data = []

        for mirrorset in mirrorsets:
            for mirror in mirrorset.mirrors:
                data.append((mirrorset.self, mirror.self, mirror.url, ' '.join(mirror.series), ' '.join(mirror.components)))

        return (('Id', 'Mirror Id', 'Mirror URL', 'Series', 'Components'), data)

class List(MirrorSetLister):
    """ List all mirror sets """

    def take_action(self, parsed_args):
        # Warm the cache
        list(self.app.client.Mirrors.list())

        return self.format_mirrorsets(self.app.client.MirrorSets.list())
