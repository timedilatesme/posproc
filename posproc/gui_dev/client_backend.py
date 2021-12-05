from posproc import*
# access data
parameters = utils.load('client_submitted_data.txt')

#CONSTANTS
LIST_ERROR_CORECTION_ALGOS = ['CASCADE', 'BICONF', 'YANETAL']
LIST_PRIVACY_AMPLIFACTION_ALGOS = ['RANDOM', 'SHA', 'BLAKE', 'MD']
BACKEND_EC_ALGO_NAMES = {'CASCADE': 'original',
                         'BICONF': 'biconf', 'YANETAL': 'yanetal'}

bob = QKDClient('Bob', current_key=Key(key_as_str=parameters['key_str']),
                server_address=parameters['address'])

bob.start_connecting()

totalTime = time.perf_counter()

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
bob.ask_server_to_do_privacy_amplification(
    final_key_bytes_size=parameters["final_key_size"], algorithm=None)
paTime = time.perf_counter() - paTime
bob.console_output('Priv. Amplification Time: ', paTime, 's \n')

# window.Element(FINAL_KEY_LENGTH_OUTPUT).Update(bob.get_key()._size)
bob.stopClient()