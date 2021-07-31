# python -m posproc.privacy_amplification.algorithms.testing

from posproc.privacy_amplification.algorithms.algo import apply_hash_alorithms


c = apply_hash_alorithms("1010100010111100111111")
size = 100 
result = {}
for algo in c.HASHING_ALGORITHMS.keys():
    try:
        final_key = c.HASHING_ALGORITHMS[algo]()
    except:
        final_key = c.HASHING_ALGORITHMS[algo](size)
    result[algo] = final_key

print("FINAL KEYS ARE:",result)
    


print(c.div_fn(4))
print(c.mod_fn(4))
print(c.perm_mod_fn(4))
print(c.perm_div_fn(4))
print(c.hash_div_fn(4))
print(c.hash_mod_fn(4))
