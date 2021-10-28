from posproc import*
constants.DATA_STORAGE = 'data/'
from testing_data import algorithm, noise_bob, size, fraction_of_bits_for_qber_estm,seed, bob_key
# python client.py
# from posproc.networking.uebn import console_output

file_name = '17072021_Bob_2.txt'

def console_output(message,*args):
    print(' >>> ' + message,*args)

with open('lab_data/' + file_name) as fh:
    bob_key_f = Key( key_as_str= fh.read())



bob = QKDClient('Bob', current_key = bob_key_f)
bob.Initialize_Events()
bob.start_ursina_client()
bob.start_events_processing_thread()
console_output('Error-correction algorithm: ' + str(algorithm))
console_output('Initial Key Size: '+ str(bob._current_key._size))

# print('Initial Key: ',bob._current_key)

totalTime = time.perf_counter()

qber1Time = time.perf_counter()
initial_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed = seed)
console_output('Initial QBER: ',initial_qber)
qber1Time = time.perf_counter() - qber1Time
console_output('Initial QBER Time: ', qber1Time, 's')
console_output('Key Size after QBER: ' + str(bob._current_key._size) + '\n')

reconTime = time.perf_counter()
recon = CascadeReconciliation(algorithm, bob, bob._current_key, noise_bob)
bob._current_key = recon.reconcile()
reconTime = time.perf_counter() - reconTime
console_output('Reconciliation Time: '+ str(reconTime)+ 's')
console_output('Key Size after Reconciliation: ' + str(bob._current_key._size))
# print('Reconciled Key: ',bob._current_key)

# qber2Time = time.perf_counter()
reconciled_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
# qber2Time = time.perf_counter() - qber2Time
console_output('Reconciled QBER: ' + str(reconciled_qber) + '\n')
# console_output('Reconciled QBER Time: ',qber2Time,'s \n')
# console_output('Key Size after Reconciliation: ', bob._current_key._size)

# print('Key before pa: ', bob._current_key)

# paTime = time.perf_counter()
bob.ask_server_to_do_privacy_amplification(final_key_bytes_size = 512)
# print('PA KEY: ',bob._current_key)
# paTime = time.perf_counter() - paTime
# console_output('Priv. Amplification Time: ', paTime, 's \n')

bob_final_key_str = bob._current_key.__str__()

with open('lab_data/final_key/' +file_name, 'w') as f:
    f.write(bob_final_key_str)
    # console_output('Final Key: ',bob._current_key)

# qber3Time = time.perf_counter()
# pa_qber = qber.qber_estimation(bob, fraction=fraction_of_bits_for_qber_estm, seed=seed)
# qber3Time = time.perf_counter() - qber3Time
# console_output('Privacy Amplified QBER: ', pa_qber)
# console_output('Privacy Amplified QBER Time: ', qber3Time,'s\n')

console_output('Final Key Size :', bob._current_key._size)

totalTime = time.perf_counter() - totalTime

console_output('Finished in:', totalTime, 's' + '\n')

stats = vars(recon.stats)
console_output('Parity Messages Transferred: '+ str(stats['ask_parity_messages']))
console_output('Parity Blocks Transferred: '+ str(stats['ask_parity_blocks']))
console_output('Unrealistic Efficiency: '+ str(stats['unrealistic_efficiency']))
console_output('Realistic Efficiency: ' + str(stats['realistic_efficiency']))

bob.send_message_to_server('when_client_qkd_completes', '')

# print('STats: ', vars(recon.stats))

# bob.stopClient()
