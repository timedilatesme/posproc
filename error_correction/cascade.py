from qber_estm.qber import qber_estimation
import os
from queuelib import PriorityQueue
import numpy as np

Q = qber_estimation()
k1= np.floor(0.73/Q)
# consider the functions to be implmented by Bob believing that the raw key of Alice is correct

# function for implementing divide and conquer algorithm over a block
def binary(bob_string_block):
    block = bob_string_block

    #case of a single bit block
    if(block.length == 1):
        return block.getindex()

    else:
        # extracting the left half of for binary implementation
        lefthalf = block.get_sub_block(0,block.length//2)

        # asking alice the correct parity of sub block chosen i.e. left through a public channel
        correct_lefthalf_parity = ask_block_parity(lefthalf)

        # calcuating the parity of the concerned sub block 
        current_lefthalf_parity=calculate_parity(lefthalf)

        # recursive implementation of divide and conquer algorithm in the concerned subblock where the ask parity and calculated parity are mismatched
        if(correct_lefthalf_parity != current_lefthalf_parity):
            return binary(lefthalf)
        else:
            righthalf=block.getsubblock(block.length//2+1,block.length)
            return binary(righthalf)


# main function for implementing the cascade algorithm
def cascade(raw_key, n):
# n -> no. of iterations
    for iteration_number in range(n):

        # extracting the blocks to be iterated using iteration number & raw key as an array(2D)
        iteration_blocks = get_iteration_blocks(raw_key,iteration_number)
        
        # calculating the parity of those blocks as an array(1D)
        current_block_parities = calculate_parities(iteration_blocks)

        # asking Alice the parities of those blocks through a public channel
        correct_block_parities = ask_parities(iteration_blocks)

        #loop for finding/correcting the error using binary() 
        for block_number in range(current_block_parities.length):
            if( correct_block_parities[block_number] != current_block_parities[block_number]):
                error_index = binary(iteration_blocks[block_number])
                if (raw_key[error_index]==0):
                    raw_key[error_index]=1
                else:
                    raw_key[error_index]=0
                
                # implementing the cascade effect due to the error found/corrected in this step
                # i.e. to possibly correct all the errors due to this error bit in previous iterations
                cascade_effect(raw_key,iteration_number,error_index)
    
    return raw_key

  
#function to implement the cascade effect
def cascade_effect(raw_key,last_iteration,first_error_index):
    #initailization & and declation of object of class queue
    set_of_error_blocks = PriorityQueue()
    current_iteration = last_iteration
    current_error_index = first_error_index
    
    #recursive loop to correct all the possible error bits in all previous iterations due to the concerned error bit
    while(not(set_of_error_blocks.empty())):
        for iteration_number in range(0,last_iteration+1):
            if(iteration_number!=current_iteration):
                block = get_corresponding_block(iteration_number,current_error_index)
                set_of_error_blocks.append(block)
            error_block = set_of_error_blocks.pop()
        if(get_parity(error_block) != get_correct_parity(error_block)):
            current_iteration = error_block.iteration
            current_error_index = binary(error_block)
            if (raw_key[current_error_index]==0):
                raw_key[current_error_index]=1
            else:
                raw_key[current_error_index]=0

def ask_block_parity(block):
    pass

def ask_parities(iteration_block):
    pass

def calculate_parity(block):
    return (sum(block)%2)

def calculate_parities(iteration_block):
    return (np.sum(iteration_block,axis=1))

def get_iteration_blocks(raw_key, iteration_number):
    kn = 2**iteration_number*k1
    dict = raw_key.get_dictionary
    data = list(dict.keys)
    oned_raw_key = np.array(data)
    return (np.reshape(oned_raw_key,raw_key.length//kn,kn))

def get_corresponding_block(iteration_number,current_error_index):
    pass

def get_parity(error_block):
    pass

def get_correct_parity(error_block):
    pass
