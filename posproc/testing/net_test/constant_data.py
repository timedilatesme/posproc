from random import seed
from posproc.key import Random_Key_Generator

size = 1000
seed = 10
ak = Random_Key_Generator(size,seed)
bk = ak.copy(0.1,'exact')