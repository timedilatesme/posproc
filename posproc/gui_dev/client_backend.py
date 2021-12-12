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
bob.console_output('Initial QBER: ' + str(initial_qber))
bob.console_output(
    'Key Size after QBER Estimation: ' + str(bob.get_key()._size))

# Reconciliation
reconTime = time.perf_counter()
recon = CascadeReconciliation(BACKEND_EC_ALGO_NAMES[parameters["ec_algorithm"]], bob,
                                bob._current_key,
                                initial_qber)
bob._current_key = recon.reconcile()
reconTime = time.perf_counter() - reconTime
bob.console_output('Reconciliation Time', (reconTime), 's \n')
bob.console_output('Key Size after Recon: ', bob.get_key()._size)

# Privacy Amplification
paTime = time.perf_counter()
pa_algoname = bob.ask_server_to_do_privacy_amplification(
    final_key_bytes_size=parameters["final_key_size"], algorithm=None)
paTime = time.perf_counter() - paTime
bob.console_output('Priv. Amplification Time: ', paTime, 's \n')

totalTime = time.perf_counter() - totalTime

data_to_write = {
    'final_key' : bob._current_key.__str__(),
    'final_key_length': bob._current_key._size,
    'time_reconciliation' : reconTime,
    'time_qkd' : totalTime,
    'qber' : initial_qber,
    'fraction_for_qber': parameters["fraction_for_qber_estm"],
    'algorithm_pa' : pa_algoname,
    'recon_algo': parameters["ec_algorithm"],
    'parity_msgs_bits': (recon.stats.ask_parity_messages, recon.stats.ask_parity_bits),
    'unrealistic_efficiency':recon.stats.unrealistic_efficiency,
    'realistic_efficiency':recon.stats.realistic_efficiency,
}

bob.send_message_to_server('final_data_to_display_on_gui', data_to_write)

data_to_write['final_key'] = bob._current_key.__str__()
utils.dump(data_to_write, data_path)

bob.stopClient()
