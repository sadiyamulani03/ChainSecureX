import random

P = 23
G = 5

def generate_private_key():
    return random.randint(1, 100)

def generate_public_key(private_key):
    return pow(G, private_key, P)

def generate_shared_key(their_public, my_private):
    return pow(their_public, my_private, P)