import argparse

from .base import BaseResourceManager
from .repositories import RepositoryManager
from cliff.lister import Lister

class ExternalDependency(object):
    pass


class ExternalDependencyManager(BaseResourceManager):
    object_class = ExternalDependency
    path = '/external_dependencies/'
    
    def from_json(self, data):
        obj = self.object_class()
        print data
        obj.client = self.client
        obj.self = data['self']
        obj.key = data['key']
        obj.url = data['url']
        obj.series = data['series']
        obj.components = data['components']
        obj.repository = self.client.Repositories.get(url=data['repository'], cached=True)
        return obj


class ExternalDependencyLister(Lister):
    def format_external_dependencies(self, external_dependencies):
        data = []

        for external_dependency in external_dependencies:
            data.append((external_dependency.self, external_dependency.url,
                         external_dependency.series,
                         external_dependency.components,
                         '%s/%s' % (external_dependency.repository.user,
                                    external_dependency.repository.name)))

        return (('Id', 'URL', 'Series', 'Components', 'APT repository'), data)

class List(ExternalDependencyLister):
    """ List all external dependencies """

    def take_action(self, parsed_args):
        return self.format_external_dependencies(self.app.client.ExternalDependencies.list())
