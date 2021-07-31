import time
from posproc.networking.client import Client
from posproc.testing.newTests.testing_data import bob_key
from posproc.error_correction.cascade.reconciliation import Reconciliation
# python -m posproc.testing.newTests.client

client = Client('Bob', bob_key)
client.start_ursina_client()
client.start_sending_messages_thread()
client.start_events_processing_thread()
client.Initialize_Events()

start = time.perf_counter()
# print('Bob Orig Key: ', bob_key)
# recon = Reconciliation('original', client, bob_key, 0.1)
# reconedKey = recon.reconcile()
# print('Bob Reconed Key: ', reconedKey)
# end = time.perf_counter()

# print('Finished in ',(end-start))

# client.stopClient()