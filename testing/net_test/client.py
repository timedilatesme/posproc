# python -m testing.net_test.client

from constants import PUBLIC_SERVER, LOCAL_SERVER
from networking.networking_class import Client
import time

bob = {}

st = time.perf_counter()
for i in range(100):
    bob.add(f"thread{i}",Client())

p = c.ask_for_parity_from_server(indexes=[0,1,3,5])

print(f"Parity is: {p}")
end = time.perf_counter()

print(f"Finished in {end-st} second(s).")