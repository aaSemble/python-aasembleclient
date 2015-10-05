import argparse
import logging
import requests
import os
import os.path
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from .repositories import RepositoryManager
from .sources import SourceManager
from .builds import BuildManager

from requests.auth import AuthBase

class aaSembleAuth(AuthBase):
    def __init__(self, key):
        self.key = key

    def __call__(self, r):
        r.headers['Authorization'] = 'Token %s' % self.key
        return r


class Client(object):
    def __init__(self, url, token):
        self.session = requests.Session()
        self.url = url
        self.auth = aaSembleAuth(token)
        self.Repositories = RepositoryManager(self)
        self.Sources = SourceManager(self)
        self.Builds = BuildManager(self)

class aaSembleApp(App):
    def __init__(self):
        super(aaSembleApp, self).__init__(description='aaSemble client',
                                          version='0.1',
                                          command_manager=CommandManager('aasemble.client'),
                                          deferred_help=True)
        
        
    def initialize_app(self, *args, **kwargs):
        self.client = Client(self.options.url, self.options.token)

    def build_option_parser(self, *args, **kwargs):
        parser = super(aaSembleApp, self).build_option_parser(*args, **kwargs)
        parser.add_argument('--token', '-t',
                            help='Auth token (defaults to $AASEMBLE_TOKEN)',
                            default=os.environ.get('AASEMBLE_TOKEN'))
        parser.add_argument('--url', '-u',
                            help='API URL [default=%(default)s',
                            default='https://aasemble.com/api/v1')
        return parser

def main(argv=sys.argv[1:]):
    aasembleapp = aaSembleApp()
    return aasembleapp.run(argv)
