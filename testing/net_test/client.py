# python -m testing.net_test.client
import random
from constants import PUBLIC_SERVER, LOCAL_SERVER
from networking.networking_class import Client
import time
from concurrent.futures import ProcessPoolExecutor



bob = []

instances = int(input("number of instances: "))
key_length = int(input("Enter Key-Length: "))
indexes_len = int(input("Enter Indexes-Length: "))

st = time.perf_counter()

for i in range(instances):
    bob.append(Client())
    indexes = random.sample(range(key_length),k = indexes_len)
    p = bob[i].ask_for_parity_from_server(indexes)
    print(f"Parity is: {p}")

end = time.perf_counter()
print(f"Finished in {end-st} second(s).")
