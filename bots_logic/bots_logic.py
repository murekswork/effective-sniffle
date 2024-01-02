import json
import random

def create_name():
    name_list = 'Hans Annabel Lula Tycen Deisy Maxim Monroe Briseida Arron Ayrabella Payson Edgar Maelynn Murphy Heidi Lucile Gianni Andee Emmie Emmelyn'.split()
    return random.choice(name_list)

def create_username_by_name(name):
    return f'user_{name}{random.randint(1, 99)}'