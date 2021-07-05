# python -m testing.net_test.client
import random
from constants import PUBLIC_SERVER, LOCAL_SERVER
from networking.networking_class import Client
import time
#from concurrent.futures import ProcessPoolExecutor



bob = []

instances = int(input("number of instances: "))
key_length = int(input("Enter Key-Length: "))
indexes_len = int(input("Enter Indexes-Length: "))

for i in range(instances):
    bob.append(Client())

st = time.perf_counter()

if instances == 1:
    bob = bob[0]
    for block_no in range(100):
        indexes = random.sample(range(key_length), k=indexes_len)
        p = bob.ask_for_parity_from_server(indexes)
        print(f"Parity is: {p}")
else:
    for i in range(instances):
        indexes = random.sample(range(key_length),k = indexes_len)
        p = bob[i].ask_for_parity_from_server(indexes)
        print(f"Parity is: {p}")

end = time.perf_counter()
print(f"Finished in {end-st} second(s).")

# Above tests show that multiple clients at bob end only decrease the speed
# of this protocol so we'll use only 1 client and only one server !
