# python -m posproc.testing.auth_test.testing_data

from posproc.networking.user_data import User, UserData
from random import seed
from posproc.key import Random_Key_Generator

size = 1000
seed = 99
copy_method = 'exact'
fraction_of_bits_for_qber_estm = 0.1
noise_bob = 0.5
user_data = UserData()

alice_key = Random_Key_Generator(size,seed)
bob_key = alice_key.copy(noise_bob,copy_method)