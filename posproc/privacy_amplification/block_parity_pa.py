from posproc import *
from posproc.error_correction.cascade.shuffle import Shuffle

shuffle_seed = 10
key_size = 100
seed = 5
noise_bob = 0.1
block_size = 2
copy_method = 'exact'
alice_key = Random_Key_Generator(key_size, seed)

bob_key = alice_key.copy(noise_bob, copy_method)

def get_shufffle_for_key(key_size,seed):
    shuffle = Shuffle(key_size,Shuffle.SHUFFLE_RANDOM,seed)
    return shuffle


def do_privacy_amplification(alice_key,seed):

    shuffle = get_shufffle_for_key(alice_key.get_size(),seed)
    pakey = []
    i =0
    while(True):
        try:
            pakey.append(shuffle.calculate_parity(alice_key,i,i+block_size))
            i+=block_size
            
        except:
            pakey.append(shuffle.calculate_parity(alice_key,i,key_size-1))
            break
    
    pakey = list(map(str, pakey))

    pakey = "".join(pakey)
    return pakey


print(alice_key)
print("Privacy amplified key:",do_privacy_amplification(alice_key,shuffle_seed))

if __name__ == '__main__':
    shuffle_seed = 10
    key_size = 100
    seed = 5
    noise_bob = 0.1
    block_size = 2
    copy_method = 'exact'
    alice_key = Random_Key_Generator(key_size, seed)
    
