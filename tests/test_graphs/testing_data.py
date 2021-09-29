from posproc import*

seed = 5000
algorithm = 'original'
copy_method = 'exact'
fraction_of_bits_for_qber_estm = 0.1
noise = 0.05

key_sizes = [2500, 5000, 10000, 20000, 30000, 40000, 50000,
             60000, 70000, 80000, 90000, 100000, 150000, 200000]

def create_key_pair_with_noise(size, noise, copy_method, seed):
    alice_key = Random_Key_Generator(size, seed)
    bob_key = alice_key.copy(noise, copy_method)
    return alice_key, bob_key

def create_multiple_keys_for_tests(noise):
    key_pairs = []
    for i in key_sizes:
        key_pairs.append(create_key_pair_with_noise(i, noise, copy_method, seed))
    return key_pairs

key_pairs_to_use = create_multiple_keys_for_tests(noise)
