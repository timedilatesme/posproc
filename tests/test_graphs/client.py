from posproc import *
constants.DATA_STORAGE = 'data/'
from testing_data import algorithm, key_pairs_to_use, fraction_of_bits_for_qber_estm, seed

# python client.py

def data_miner(key_pairs):
    time_vs_size_data = []
    final_qber_vs_size_data = []
    
    for i,(_,bob_key) in enumerate(key_pairs):
        totalTime = time.perf_counter()
        
        bob = QKDClient('Bob' + str(i), current_key=bob_key)
        bob.Initialize_Events()
        bob.start_ursina_client()
        bob.start_events_processing_thread()
        
        initial_qber = qber.qber_estimation(
            bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
        
        recon = CascadeReconciliation(
            algorithm, bob, bob._current_key, initial_qber)
        bob._current_key = recon.reconcile()
        
        # reconciled_qber = qber.qber_estimation(
        #     bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
        bob.ask_server_to_do_privacy_amplification(final_key_bytes_size=500)
        
        pa_qber = qber.qber_estimation(
            bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
        
        bob.send_message_to_server('completed', Content_= i)
        bob.stopClient()
        
        print('Final Key Size: ', bob._current_key._size)
        
        totalTime = time.perf_counter() - totalTime
        final_qber_vs_size_data.append((bob._current_key._size, pa_qber))
        time_vs_size_data.append((bob._current_key._size, totalTime))
                
data_miner(key_pairs_to_use)
