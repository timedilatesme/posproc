from key import *

shuffle_seed = 10
key_size = 100
seed = 5
noise_bob = 0.1
block_size = 2
copy_method = 'exact'
alice_key = Random_Key_Generator(key_size,seed)

bob_key = alice_key.copy(noise_bob,copy_method)