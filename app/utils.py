# -*- coding:utf-8 -*-
import random
import string


def generate_random_sequence():
    base = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNOPQRST123456789"  # remove l, I, o, 0
    random_sequence = string.join(random.sample(base, 8)).replace(" ", "")
    return random_sequence
