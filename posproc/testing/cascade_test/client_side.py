# python -m posproc.testing.cascade_test.client_side
import time
from posproc.networking.client import Client
from posproc.testing.cascade_test.testing_data import bob_key,size,seed, fraction_of_bits_for_qber_estm, algorithm
from posproc.error_correction.cascade.reconciliation import Reconciliation
from posproc.qber import qber_estimation


def qber_test():
    print(f'Noisy Key: {bob_key}')
    st = time.perf_counter()

    bob = Client('Bob', bob_key)
    error_rate = qber_estimation(size, bob, fraction=0.5, seed = seed)
    print(f'QBER is: {error_rate}')
    print(f'Key after QBER: {bob_key}')
    
    #bob.send_closing_message_to_the_server()
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")
    

def cascade_algorithm_test():
    print(f'Bob\'s Initial Key: {bob_key}')
    st = time.perf_counter()
    
    bob = Client('Bob', bob_key)
    error_rate = qber_estimation(size, bob, fraction = fraction_of_bits_for_qber_estm,seed = seed)
    print(f'Bob\'s QBER is: {error_rate}')
    
    recon = Reconciliation(algorithm,bob,bob_key,error_rate)
    recon.reconcile()
    print(f'Bob\'s Reconciled Key: {recon.get_reconciled_key()}')
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")
    
cascade_algorithm_test()