from posproc import*
constants.DATA_STORAGE = 'data/'
from testing_data import bob_key, algorithm, noise_bob, size, fraction_of_bits_for_qber_estm,seed

# python client.py

# Create the client
bob = QKDClient('Bob', current_key = bob_key)

# Start the client socket
bob.start_ursina_client()

# Important calls for event based networking
bob.start_sending_messages_thread()
bob.start_events_processing_thread()

# Initialize all the protocols for authentication, error correction, privacy amplification.
bob.Initialize_Events()


initial_qber = qber.qber_estimation(size, bob, fraction=fraction_of_bits_for_qber_estm, seed = seed)

print('Initial QBER: ',initial_qber)
'''
start = time.perf_counter()
recon = CascadeReconciliation(algorithm, bob, bob._current_key, initial_qber)
bob._current_key = recon.reconcile()

reconciled_qber = qber.qber_estimation(
    size, bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)

print('Reconciled QBER: ', reconciled_qber)


bob.ask_server_to_do_privacy_amplification(final_key_bytes_size=8)
print('PA KEY: ',bob._current_key)

pa_qber = qber.qber_estimation(
    size, bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)

print('Priv Ampl. QBER: ', pa_qber)

end = time.perf_counter()


print('Finished in :', (end-start), 's')'''

bob.stopClient()
