# 'in-memory' database
import random
import uuid
from datetime import datetime


class LlamaBase:
    def __init__(self):
        self.llamas = {}
        self.inventory = {}
        self.users = {}

        # API AUTH
        self.api_tokens = {}

        self.init_data()

    def init_data(self):
        # User
        demo_user = User('demo', 'demo')
        self.users['bobuel'] = User('bobuel', 'bob123')
        self.users[demo_user.name] = demo_user

        # Llamas
        for i in xrange(5):
            l = Llama(demo_user.name)
            self.llamas[l.id] = l

        # Items
        items = [
            Item('Apple', 10, demo_user.name),
            Item('Quinoa', 5, demo_user.name),
            Item('Hay', 50, demo_user.name),
            Item('MRE', 100, demo_user.name),
            Item('Hay', 50, 'bobuel'),
        ]
        for i in items:
            self.inventory[i.id] = i

        # Token
        token = {
            'id': 'd4f90bf9-ec42-4225-b2e4-a9ffa57125d7',
            'user': 'demo',
            'createdate': datetime.now()
        }
        self.api_tokens[token['id']] = token

    def create_api_token(self, username):
        token = {
            'id': str(uuid.uuid4()),
            'user': username,
            'createdate': datetime.now()
        }
        self.api_tokens[token['id']] = token
        return token


class Llama:
    sequencer = 1

    def __init__(self, owner):
        self.id = Llama.sequencer
        Llama.sequencer += 1
        self.name = 'Llama {}'.format(self.id)
        self.hunger = random.randint(0, 100)
        self.owner = owner

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'hunger': self.hunger,
            'owner': self.owner
        }


class Item:
    sequencer = 1

    def __init__(self, name, fillingness, owner):
        self.id = Item.sequencer
        Item.sequencer += 1
        self.name = name
        self.fillingness = fillingness
        self.owner = None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'fillingness': self.fillingness,
            'owner': self.owner
        }


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.cash = 1000

    def serialize(self):
        return {
            'name': self.name,
            'password': self.password,
            'cash': self.cash
        }
