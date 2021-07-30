# python -m algorithms.testing

from algorithms.algo import apply_hash_alorithms

c = apply_hash_alorithms("101010000111100111111")
print(c.ripemd160())
import hashlib
print(hashlib.algorithms_guaranteed)
