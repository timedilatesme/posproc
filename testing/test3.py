from queuelib import PriorityQueue
from queuelib import FifoDiskQueue
import json
qfactory = lambda priority: FifoDiskQueue('queue-dir-%s' % priority)
pq = PriorityQueue(qfactory)



str_block = '['
iter = 1
block = [684, 926, 406, 302, 404, 299]
for i in block:
    str_block+=str(i)
    str_block += ','
str_block_new = str_block[0:-1]
str_block_new += ']'+str(iter)
#print(str_block_new)
#print(type(str_block_new))
#print(type(block))
b = bytes(str_block_new,encoding='ascii')
#print(type(b))

pq.push(b,0)
pq.push(b'v',1)

c = pq.pop()
#print(c)
#print(type(c))
d= c.decode('ascii')
#print(d)
#print(type(d))
iter = d[-1]
d=d[0:-1]

print(int(iter))
block = d.strip('][').split(',')
block_new = list()
for i in block:
    block_new.append((int(i)))
print(block_new)
print(type(block))
'''res = json.loads(d)
print(res)
print(type(res))'''

k = "[84,362,391,988]"
j = bytes(k,encoding = 'ascii')
print(j)
m= j.decode('ascii')
l = m.strip('][').split(',')
error_block=list()
for i in l:
    error_block.append(int(i))
print(error_block)