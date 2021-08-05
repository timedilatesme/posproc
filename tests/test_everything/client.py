from posproc import*
constants.DATA_STORAGE = 'data/'
from testing_data import bob_key, algorithm, noise_bob, size, fraction_of_bits_for_qber_estm,seed

# python client.py


bob = QKDClient('Bob', current_key = bob_key)
bob.Initialize_Events()
bob.start_ursina_client()
bob.start_events_processing_thread()
print('Initial Key Size: ', bob._current_key._size)

# print('Initial Key: ',bob._current_key)

totalTime = time.perf_counter()

qber1Time = time.perf_counter()
initial_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed = seed)
print('Initial QBER: ',initial_qber)
qber1Time = time.perf_counter() - qber1Time
print('Initial QBER Time: ', qber1Time, 's\n')

reconTime = time.perf_counter()
recon = CascadeReconciliation(algorithm, bob, bob._current_key, noise_bob)
bob._current_key = recon.reconcile()
reconTime = time.perf_counter() - reconTime
print('Reconciliation Time', (reconTime), 's \n')
# print('Reconciled Key: ',bob._current_key)

qber2Time = time.perf_counter()
reconciled_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
qber2Time = time.perf_counter() - qber2Time
print('Reconciled QBER: ', reconciled_qber)
print('Reconciled QBER Time: ',qber2Time,'s \n')

paTime = time.perf_counter()
bob.ask_server_to_do_privacy_amplification(final_key_bytes_size = 128)
# print('PA KEY: ',bob._current_key)
paTime = time.perf_counter() - paTime
print('Priv. Amplification Time: ', paTime, 's \n')

qber3Time = time.perf_counter()
pa_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
qber3Time = time.perf_counter() - qber3Time
print('Privacy Amplified QBER: ', pa_qber)
print('Privacy Amplified QBER Time: ', qber3Time,'s\n')

print('Final Key Size: ', bob._current_key._size)

totalTime = time.perf_counter() - totalTime

print('Finished in :', totalTime, 's')

bob.stopClient()