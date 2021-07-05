import random

def qber_estimation(n,alice, bob, fraction = 0.1): 
    # fraction: what fraction of key size to use for qber estimation
    # alice,bob : instances of the Client class
    # n : raw key size after sifting
    
    indexes = random.sample(range(n),int(fraction*n))
    sample_length = len(indexes)

    raw_key_a = alice.ask_for_bits(indexes) # returns a list with bit values
    raw_key_b = bob.ask_for_bits(indexes) 

    #TODO ask_for_bits method must also contain a way to remove the indexes used!
    
    diff = 0
    for i in range(sample_length):
        if raw_key_a[i] != raw_key_b[i]:
            diff += 1
    
    return f"{(diff/int(fraction*n))*100}%"
