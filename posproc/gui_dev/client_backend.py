from posproc import* 
# access data
data_path = sys.argv[1]
parameters = utils.load(data_path)

#CONSTANTS
LIST_ERROR_CORECTION_ALGOS = ['CASCADE', 'BICONF', 'YANETAL']
LIST_PRIVACY_AMPLIFACTION_ALGOS = ['RANDOM', 'SHA', 'BLAKE', 'MD']
BACKEND_EC_ALGO_NAMES = {'CASCADE': 'original',
                         'BICONF': 'biconf', 'YANETAL': 'yanetal'}


bob = QKDClient('Bob', current_key=Key(key_as_str=parameters['key_str']),
                server_address=parameters['address'])

totalTime = time.perf_counter()

bob.start_connecting()

# QBER Estimation
initial_qber = qber.qber_estimation(
    bob, parameters["fraction_for_qber_estm"], seed=None)
print('Initial QBER: ' + str(initial_qber))
print('Key Size after QBER Estimation: ' + str(bob.get_key()._size))

# Reconciliation
reconTime = time.perf_counter()
recon = CascadeReconciliation(BACKEND_EC_ALGO_NAMES[parameters["ec_algorithm"]], bob,
                                bob._current_key,
                                initial_qber)
if 0 < initial_qber <= parameters["qber_threshold"]:       
    bob._current_key = recon.reconcile()
    reconTime = time.perf_counter() - reconTime
    print('Reconciliation Time: ', (reconTime), 's')
    print('Key Size after Reconciliation: ', bob.get_key()._size)
    
    # Privacy Amplification
    paTime = time.perf_counter()
    pa_algoname = bob.ask_server_to_do_privacy_amplification(
        final_key_bytes_size=parameters["final_key_size"], algorithm=None)
    paTime = time.perf_counter() - paTime
    print('Privacy Amplification Time: ', paTime, 's')
    
else:
    reconTime = 0 
    print('QBER > threshold, no reconciliation!')
    
    paTime = 0
    pa_algoname = None

totalTime = time.perf_counter() - totalTime

data_to_write = {
    'final_key_length': bob._current_key._size,
    'time_reconciliation' : reconTime,
    'time_qkd' : totalTime,
    'qber' : initial_qber,
    'fraction_for_qber': parameters["fraction_for_qber_estm"],
    'algorithm_pa' : pa_algoname,
    'recon_algo': parameters["ec_algorithm"] if 0 < initial_qber <= parameters["qber_threshold"] else None,
    'parity_msgs_bits': (recon.stats.ask_parity_messages, recon.stats.ask_parity_bits),
    'unrealistic_efficiency':recon.stats.unrealistic_efficiency,
    'realistic_efficiency':recon.stats.realistic_efficiency,
    'qber_threshold': parameters["qber_threshold"],
}

bob.send_message_to_server('final_data_to_display_on_gui', data_to_write)

print('Total Time: ', totalTime, 's')

data_to_write['final_key'] = bob._current_key.__str__()
utils.dump(data_to_write, data_path)

bob.stopClient()
