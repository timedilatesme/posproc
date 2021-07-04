from raw_key import Raw_Key
#from qber_estm.qber import qber_estimation
import numpy as np
import random
import sys
from queuelib import PriorityQueue
from queuelib import LifoDiskQueue
def qfactory(priority): return LifoDiskQueue('queue-dir-%s' % priority)

sys.setrecursionlimit(10000)

def initialisation():
    #n = int(input("Length of the original key:"))
    n = 1000
    #e = float(input("Error rate: "))
    e = 0.2
    alice = np.random.randint(2, size=n)
    alice = alice.tolist()
    global original_key
    original_key = Raw_Key(alice)
    #print("alice original:",alice)
    global bob
    bob = alice.copy()
    
    indexes = random.sample(range(n), int(np.floor(e*n)))
    for i in indexes:
        if(bob[i] == 1):
            bob[i] = 0
            # print("first")
        else:
            bob[i] = 1
            # print("second")
    # print("bob:",bob)

    global raw_key_bob_complete
    raw_key_bob_complete = Raw_Key(bob)
    global a 
    a = Raw_Key(bob)

initialisation()
# print(original_key.as_list)
# print(raw_key_bob.as_list)
all_raw_keys = []

# temporary QBER


def QBER():
    fraction = 0.1
    n = raw_key_bob_complete.length
    indexes = random.sample(range(n), int(fraction*n))
    sample_length = len(indexes)
    diff = 0
    for i in range(sample_length):
        if raw_key_bob_complete.as_list[i] != original_key.as_list[i]:
            diff += 1

    return (diff/(fraction*n))


Q = QBER()
print("Q=", Q)
k1 = np.floor(0.73/Q)
# consider the functions to be implmented by Bob believing that the raw key of Alice is correct

# function for implementing divide and conquer algorithm over a block


def binary(bob_string_block):

    block = bob_string_block
    #print("binary/ block is: ",block)
    # case of a single bit block\
    if(len(block) == 1):
        #print("binary/ single element block is:",block)
        return block[0]

    else:
        # extracting the left half of for binary implementation
        lefthalf = block[0:len(block)//2]
        righthalf = block[len(block)//2:len(block)]

        # asking alice the correct parity of sub block chosen i.e. left through a public channel
        correct_lefthalf_parity = ask_block_parity(lefthalf)

        # calcuating the parity of the concerned sub block
        current_lefthalf_parity = calculate_parity(lefthalf)

        # recursive implementation of divide and conquer algorithm in the concerned subblock where the ask parity and calculated parity are mismatched
        if(correct_lefthalf_parity != current_lefthalf_parity):
            return binary(lefthalf)
        else:
            return binary(righthalf)


# main function for implementing the cascade algorithm
def cascade(raw_key_bob_complete, n):
    # n -> no. of iterations
    # removing the bits which can't form a block of size kn in iteration n.
    global raw_key_bob
    raw_key_bob = get_multiple_of_kn_key(raw_key_bob_complete, n)
    print(len(raw_key_bob.as_list))
    print((raw_key_bob.as_list))

    for iteration_number in range(n):

        print("cascade/ iteration number is:", iteration_number)
        # extracting the blocks to be iterated using iteration number & raw key as an array(2D)
        if(iteration_number == 0):

            all_raw_keys.append(raw_key_bob.get_dictionary())
            iteration_blocks = get_iteration_blocks(raw_key_bob.get_dictionary(), iteration_number)
            print("cascade/ iteration blocks are :", iteration_blocks)
        else:
            x = dict()
            x = raw_key_bob.shuffle()
            all_raw_keys.append(x)
            iteration_blocks = get_iteration_blocks(x, iteration_number)
        # calculating the parity of those blocks as an array(1D)
        current_block_parities = calculate_parities(iteration_blocks)
        #print("cascade/ current_block_parities_are:", current_block_parities)
        # asking Alice the parities of those blocks through a public channel
        correct_block_parities = ask_parities(iteration_blocks)
        #print("cascade/ correct_block_parities_are:", correct_block_parities)
        # loop for finding/correcting the error using binary()
        for block_number in range(len(current_block_parities)):
            #print("cascade/ all_raw_key is:",all_raw_keys[iteration_number-1].keys())
            #print("cascade/ block number is:", block_number)
            if(correct_block_parities[block_number] != current_block_parities[block_number]):

                error_index = binary(iteration_blocks[block_number])
                #print("cascade/ error detected and error is:",raw_key_bob.as_list[error_index])
                if (raw_key_bob.as_list[error_index] == 0):
                    raw_key_bob.as_list[error_index] = 1

                else:
                    raw_key_bob.as_list[error_index] = 0

                # implementing the cascade effect due to the error found/corrected in this step
                # i.e. to possibly correct all the errors due to this error bit in previous iterations

                if(iteration_number >= 1):
                    print("cascade/ implemnting cascade effect for error index and iter: ", error_index,iteration_number)
                    cascade_effect(raw_key_bob, iteration_number, error_index)

        if raw_key_bob.as_list == original_key.as_list:
            print("yes they are equal", iteration_number)

        s=0
        for i in range(raw_key_bob.length):
            if(raw_key_bob.as_list[i] != original_key.as_list[i]):
                s += 1
        print(f"cascade/ number of errors left = {s} in iteration step {iteration_number}")    
    return raw_key_bob


# function to implement the cascade effect
def cascade_effect(raw_key_bob, last_iteration, first_error_index):
    # initailization & and declation of object of class queue
    set_of_error_blocks = PriorityQueue(qfactory)
    current_iteration = last_iteration
    current_error_index = first_error_index
    #print("cascade effect/ current_error_index is:", current_error_index)

    # recursive loop to correct all the possible error bits in all previous iterations due to the concerned error bit
    a=3
    while(a!=0):
        for iteration_number in range(0, last_iteration):
            #print("cascade effect/ iteration number:", iteration_number)
            if(iteration_number != current_iteration):
                # tuple
                block, iter = get_corresponding_block(iteration_number, current_error_index)
                print(f"cascade effect/ getting corresponding block: {block} wih priority {iter}")
                #print("cascade effect/ getting corresponding block :", (block))

                str_block = '['
                for i in block:
                    str_block+=str(i)
                    str_block += ','
                str_block_new = str_block[0:-1]
                str_block_new += ']'+str(iter)

                str_block_new_bytes = bytes(str_block_new,encoding='ascii')
                set_of_error_blocks.push(str_block_new_bytes, priority=iter)

                #print("cascade effect/ set of error blocks is:",set_of_error_blocks)
                #print("cascade effect/ appending done!")

        error_block_with_iter_bytes = set_of_error_blocks.pop()
        error_block_with_iter_str = error_block_with_iter_bytes.decode('ascii')
        print("cascade effect/ error_block_with_iter is:", error_block_with_iter_str)
        iteration = int(error_block_with_iter_str[-1])
        error_block_with_iter_str=error_block_with_iter_str[0:-1]
        error_block_new = error_block_with_iter_str.strip('][').split(',')
        error_block=list()
        for i in error_block_new:
            error_block.append(int(i))
    
        print("cascade effect/ error block is:", error_block)

        if(calculate_parity(error_block) != ask_block_parity(error_block)):
            current_iteration = iteration
            current_error_index = binary(error_block)
            print("cascade effect/ error index in cascade effect is:", current_error_index)
            print("cascade effect/ calculate_parity!= ask_block_parity")
            if (raw_key_bob.as_list[current_error_index] == 0):
                raw_key_bob.as_list[current_error_index] = 1
            else:
                raw_key_bob.as_list[current_error_index] = 0
        print("cascade effect/ length of queue is:", len(set_of_error_blocks))
        if(len(set_of_error_blocks) == 0):
            break
        a-=1


def ask_parities(iteration_blocks):
    parities = []
    for block in iteration_blocks:
        parities.append(ask_block_parity(block))
    return parities


def calculate_parity(block):
    s = 0
    for i in block:
        s += raw_key_bob.as_list[i]
    return s % 2


def calculate_parities(iteration_blocks):
    s = 0
    parities = []
    for block in iteration_blocks:
        for i in block:
            s += raw_key_bob.as_list[i]
        parities.append(s % 2)
        s = 0
    return parities


def get_iteration_blocks(raw_key_bob_dict, iteration_number):
    k_n = 2**iteration_number*k1

    data = list(raw_key_bob_dict.keys())
    oned_raw_key = np.array(data)
    np.array(oned_raw_key)
    # print("k_n:",k_n)
    l = np.reshape(oned_raw_key, (int(len(oned_raw_key)/k_n), int(k_n)))
    l = l.tolist()
    return (l)


def get_corresponding_block(iteration_number, current_error_index):
    raw_key_of_iter_n = all_raw_keys[iteration_number]
    twod_nth_raw_key = get_iteration_blocks(raw_key_of_iter_n, iteration_number)
    #print("get_corresponding_block/ twod_nth_raw_key is: ", twod_nth_raw_key)
    for block in twod_nth_raw_key:
        for i in block:
            if(current_error_index == i):

                #print("get_correcponding_block/ block to be returned:",block)
                return block, iteration_number
                break
                break


def get_multiple_of_kn_key(raw_key_bob_complete, iterations):
    global kn
    kn = 2**iterations*k1
    #no_of_indexes_to_delete = raw_key_bob.length%kn
    # print(no_of_indexes_to_delete)
    global no_of_blocks_in_iter_n
    no_of_blocks_in_iter_n = raw_key_bob_complete.length//kn
    #last_bit = no_of_blocks_in_iter_n*kn
    # print(type(raw_key_bob.as_list))
    bob_new = bob[0:int(no_of_blocks_in_iter_n*kn)]
    raw_key_new = Raw_Key(bob_new)
    # for i in range(int(no_of_indexes_to_delete)):
    # raw_key_bob.remove(last_bit+i)
    return raw_key_new

# temporary ask_block_parity and QBER


def ask_block_parity(block):
    s = 0
    for i in block:
        s += original_key.as_list[i]
    return s % 2





#iterations = int(input("Number of Iterations:"))
iterations = 4
final_key = cascade(raw_key_bob_complete, iterations)
print("final key is:", final_key.as_list)
print(final_key.length)

'''for i in range(final_key.length):
    s = 0
    if(final_key.as_list[i] != original_key.as_list[i]):
        s += 1
print("number of errors left = ", s)
if final_key.as_list== original_key.as_list[0:int(no_of_blocks_in_iter_n*kn)]:
            print("yes they are equal")


s=0
for i in range(int(no_of_blocks_in_iter_n*kn)):
    if(raw_key_bob_complete.as_list[i] != a.as_list[i]):
        s += 1
print("number of errors were  = ", s)'''