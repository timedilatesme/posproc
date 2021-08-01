# python -m posproc.testing.cascade_test.eve_side
import time
from posproc.networking.client import Client
from posproc.testing.cascade_test.testing_data import eve_key,size,seed, fraction_of_bits_for_qber_estm, algorithm
from posproc.error_correction.cascade.reconciliation import Reconciliation
from posproc.qber import qber_estimation  

def cascade_algorithm_test_eavesdropping():
    print(f'Eave\'s Initial Key: {eve_key}')
    st = time.perf_counter()
    
    eve = Client('Eve', eve_key)
    error_rate = qber_estimation(size, eve, fraction = fraction_of_bits_for_qber_estm,seed = seed)
    print(f'QBER is: {error_rate}')
    
    recon = Reconciliation(algorithm,eve,eve_key,error_rate)
    recon.reconcile()
    eve._current_key = recon.get_reconciled_key()
    #print(f'Eve\'s Reconciled Key: {eve._current_key}')
    new_error_rate = qber_estimation(
        eve._current_key._size, eve, fraction=1, seed=seed)

    print(f'Eve\'s new QBER is: {new_error_rate}')
    
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")
    
cascade_algorithm_test_eavesdropping()

#TODO: check with eaves dropper.
