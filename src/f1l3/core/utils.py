import random
import string


def generate_random_sequence(seqlen=3) -> str:
    chrs = list(string.digits + string.ascii_letters + "-_~")
    return ''.join(random.choices(chrs, k=seqlen))
