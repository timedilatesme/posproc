# python -m posproc.testing.cascade_test.client_side
from posproc.networking.user_data import User
import time
from posproc.networking.client import Client
from posproc.testing.cascade_test.testing_data import user_data,bob_key,size,seed, fraction_of_bits_for_qber_estm, algorithm
from posproc.error_correction.cascade.reconciliation import Reconciliation
from posproc.qber import qber_estimation

def authentication_test():
    #print(f'Bob\'s Initial Key: {bob_key}')
    st = time.perf_counter()

    bob = Client('Bob', bob_key)
    #TEST AUTH:
    bob_user = User(username='Bob', address=bob.getsockname(),
                    auth_id=bob.auth_id)
    bob_user.connected_to_server = True
    user_data.update_user_data(bob_user)

    error_rate = qber_estimation(
        bob._current_key._size, bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
    print(f'Bob\'s QBER is: {error_rate}')

    recon = Reconciliation(algorithm, bob, bob._current_key, error_rate)
    recon.reconcile()
    # Update bob's key to the new reconciled key.
    bob._current_key = recon.get_reconciled_key()

    # print(f'Bob\'s Reconciled Key: {recon.get_reconciled_key()._bits}')
    #print("Bob Key New Size: ",bob_key._size)
    new_error_rate = qber_estimation(
        bob._current_key._size, bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
    
    # print(f'Bob\'s new Key: {bob._current_key}')
    print(f'Bob\'s new QBER is: {new_error_rate}')
    
    # print("User Data: ",user_data)
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")

if __name__ == "__main__":
    authentication_test()

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
    #print(f'Bob\'s Initial Key: {bob_key}')
    st = time.perf_counter()
    
    bob = Client('Bob', bob_key)
    
    #TEST AUTH:
    bob_user = User(username='Bob', address= bob.getsockname(),auth_id=bob.auth_id)
    user_data.update_user_data(bob_user)
    
    
    error_rate = qber_estimation(size, bob, fraction = fraction_of_bits_for_qber_estm,seed = seed)
    #print(f'Bob\'s QBER is: {error_rate}')
    
    recon = Reconciliation(algorithm,bob,bob._current_key,error_rate)
    recon.reconcile()
    # Update bob's key to the new reconciled key.
    bob._noisy_key = recon.get_reconciled_key()
    
    #print(f'Bob\'s Reconciled Key: {recon.get_reconciled_key()._bits}')
    #print("Bob Key New Size: ",bob_key._size)
    new_error_rate = qber_estimation(bob_key._size,bob, fraction=fraction_of_bits_for_qber_estm, seed = seed )
    print(f'Bob\'s new QBER is: {new_error_rate}')
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")
    
