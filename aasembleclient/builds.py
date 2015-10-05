from .base import BaseResourceManager
from .repositories import RepositoryManager
from cliff.lister import Lister

class Build(object):
    pass

class BuildManager(BaseResourceManager):
    object_class = Build
    path = '/builds/'
    
    def from_json(self, data):
        obj = self.object_class()
        obj.client = self.client
        obj.self = data['self']
        obj.build_started = data['build_started']
        obj.sha = data['sha']
        obj.version = data['version']
        obj.buildlog = data['buildlog_url']
        obj.source = self.client.Sources.get(url=data['source'], cached=True)
        return obj
        

class BuildLister(Lister):
    def format_builds(self, builds):
        data = []

        for build in builds:
            data.append((build.self, build.build_started, build.sha, build.version, build.source.git_url, '%s/%s' % (build.source.repository.user, build.source.repository.name)))

        return (('Id', 'Build start time', 'SHA', 'Version', 'Source', 'APT repo'), data)


class List(BuildLister):
    """ List all builds """

    def take_action(self, parsed_args):
        # Warm the cache
        list(self.app.client.Repositories.list())
        list(self.app.client.Sources.list())

        return self.format_builds(self.app.client.Builds.list())


class ListBySource(BuildLister):
    """ List all builds of a given source"""

    def get_parser(self, prog_name):
        parser = super(ListBySource, self).get_parser(prog_name)
        parser.add_argument('id')
        return parser

   
    def take_action(self, parsed_args):
        # Warm the cache
        source = self.app.client.Sources.get(parsed_args.id)

        return self.format_builds(source.builds)
