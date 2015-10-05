import argparse
import dateutil.parser

from .base import BaseResourceManager
from cliff.lister import Lister

class Snapshot(object):
    pass


class SnapshotManager(BaseResourceManager):
    object_class = Snapshot
    path = '/snapshots/'
    
    def from_json(self, data):
        obj = self.object_class()
        obj.client = self.client
        obj.self = data['self']
        obj.timestamp = dateutil.parser.parse(data['timestamp'])
        obj.mirror_set = data['mirrorset']
        return obj


class SnapshotLister(Lister):
    def format_snapshots(self, snapshots):
        data = []

        for snapshot in snapshots:
            data.append((snapshot.self, snapshot.mirror_set, snapshot.timestamp))

        return (('Id', 'Mirror Set Id', 'Timestamp'), data)

class List(SnapshotLister):
    """ List all snapshots """

    def take_action(self, parsed_args):
        # Warm the cache
        return self.format_snapshots(self.app.client.Snapshots.list())

