import json, sys
import pprint

class Item(object):
    def __init__(self, name="Bag of Holding"):
        self.name = name

    def __str__(self):
        return self.name

class Player(object):
    def __init__(self, name="Madeleine"):
        self.name = name
        self.inventory = []

    def __str__(self):
        return self.name

    def pickup_item(self, item=Item()):
        self.inventory.append(item)

    def set_name(self, name):
        self.name = name

    def check_inventory(self, args):
        print self.name + "'s Inventory"
        print "=================================================="
        for item in self.inventory:
            print item
        return ("Describe Surrounding", args)

class Connector(object):
    def __init__(self, destination):
        self.destination = destination

class Zone(object):
    def __init__(self, name="Empty Void", description="Nothing here", game_over=False):
        self.name = name
        self.description = description
        self.game_over = game_over
        self.exits = {}
    
    def __str__(self):
        return self.name

    def add_connector(self, connector, direction):
        self.exits[direction] = connector

    def describe(self):
        print self.name
        print
        print self.description

class World(object):
    def __init__(self, f='world.json'):
        self.zones = {}
        json_data = open(f, 'r').read()
        data = json.loads(json_data)
        self.title = data['title']
        tmp = None
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(data)
        world_zones = data['zones']
        connectors = data['connectors']
        for count, z in enumerate(world_zones):
            tmp = Zone(world_zones[z]['title'], world_zones[z]['description'], world_zones[z]['game_over'])
            self._add_zone(str(z), tmp)
            if world_zones[z]['start']:
                self._set_start_zone(z)
        for c in connectors:
            conn = Connector(self.zones[c['to_id']])
            self.zones[c['from_id']].add_connector(conn, c['direction'])

    def __str__(self):
        return self.title

    def _add_zone(self, id, zone):
        self.zones[id] = zone

    def _set_start_zone(self, id):
        self.start_zone = self.zones[id]

    def start(self):
        return self.start_zone
