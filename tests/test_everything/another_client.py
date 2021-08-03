from posproc import*
constants.DATA_STORAGE = 'data/'
from testing_data import bob_key, algorithm, noise_bob, size, fraction_of_bits_for_qber_estm,seed
from client import bob

initial_qber = qber.qber_estimation(size, bob, fraction=fraction_of_bits_for_qber_estm, seed = seed)

print('Initial QBER: ',initial_qber)