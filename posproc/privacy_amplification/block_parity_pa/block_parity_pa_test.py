from posproc import *



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