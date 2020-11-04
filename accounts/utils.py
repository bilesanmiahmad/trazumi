import random


def get_verification_code():
    code = random.randint(100000, 999999)
    return code
