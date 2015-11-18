#!./env/bin/python

from models import Player, Item, Zone, Connector, World
from fsm import StateMachine
import json, sys

class controller(object):
    def __init__(self, world=""):
        self.fsm = StateMachine()
        self.player = Player()
        if '-f' in sys.argv:
            try:
                f = sys.argv[sys.argv.index('-f') + 1]
            except IndexError:
                print "You didn't include a file"
                sys.exit(0)
            self._make_world(f)
        else:
            room1 = Zone("Grand Entrance")
            room2 = Zone("Grand Hallway")
            room3 = Zone("Grand Staircase")
            conn = Connector(room1)
            room2.add_connector(conn, 'south')
            conn = Connector(room2)
            room1.add_connector(conn, 'north')
            room3.add_connector(conn, 'south')
            conn = Connector(room3)
            room2.add_connector(conn, 'north')
            room3.add_connector(conn, 'north')
            self.start_room = room1
 
    def _make_world(self, path):
        json_data = open(path, 'r').read()
        data = json.loads(json_data)
        self.world = World(data["title"])
        room1 = Zone("Grand Entrance")
        room2 = Zone("Grand Hallway")
        room3 = Zone("Grand Staircase")
        conn = Connector(room1)
        room2.add_connector(conn, 'south')
        conn = Connector(room2)
        room1.add_connector(conn, 'north')
        room3.add_connector(conn, 'south')
        conn = Connector(room3)
        room2.add_connector(conn, 'north')
        room3.add_connector(conn, 'north')
        self.world.add_zone(room1)
        self.world.add_zone(room2)
        self.world.add_zone(room3)
        self.start_room = self.world.zones[0]

    def setup(self, current_room):
        choice = raw_input("What is your name? (Leave blank default: 'Madeleine') ")
        if len(choice) > 0:
            self.player.set_name(choice)
        print "Hello, " + self.player.name
        print "Welcome to " + self.world.title
        print
        return ("Describe Surrounding", current_room)
        
    def describe_surrounding(self, current_room):
        print current_room.name
        print
        print "Exits:"
        print "====================="
        for direction in current_room.exits:
            print direction + " => " + str(current_room.exits[direction].destination)
        return ("Prompt Input", current_room)

    def prompt(self, current_room):
        choice = raw_input("What's next? ")
        if len(choice) <= 0:
            print "Ummm..."
            return ("Prompt Input", current_room)
        if choice.lower() == 'exit' or choice.lower() == 'quit':
            print "Goodbye, " + self.player.name
            return ("End Game", current_room)
        if choice.lower() == 'i' or choice.lower() == 'inventory':
            return ("Check Inventory", current_room)
        elif choice.lower() in current_room.exits:
            current_room = current_room.exits[choice.lower()].destination
            return ("Describe Surrounding", current_room)
        else:
            print "Ouch, no exit there"
            return ("Prompt Input", current_room)

    def end_game(self, current_room):
        print "You ended the game in " + current_room.name
        
if __name__ == "__main__":
    c = controller()
    c.fsm.add_state("Get Player Info", c.setup)
    c.fsm.add_state("Check Inventory", c.player.check_inventory)
    c.fsm.add_state("Describe Surrounding", c.describe_surrounding)
    c.fsm.add_state("Prompt Input", c.prompt)
    c.fsm.add_state("End Game", c.end_game, end_state=True)
    c.fsm.set_start("Get Player Info")
    c.fsm.run(c.start_room)
