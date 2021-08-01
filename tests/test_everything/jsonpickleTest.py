from posproc.utils import*

# d = {1:2,2:4}
# dumped = dumps(d)
# print(dumped)
# loaded = loads(dumped)
# print(loaded)

@rename('naga')
def f():
    print(__name__)
locals()['naga']