from error_correction.cascade import ask_block_parity, calculate_parity ,binary
import numpy as np

def optimized_cascade():
    
    pass
def binconf(raw_key,no_of_biconf_iter,size_of_first_block):
    iter_number = 0
    while(iter_number<no_of_biconf_iter):
        iteration_blocks = split_in_two_blocks(raw_key,size_of_first_block)
        current_first_block_parity = calculate_parity(iteration_blocks[0])
        correct_first_block_parity = ask_block_parity(iteration_blocks[0])

        if(current_first_block_parity!=correct_first_block_parity):
            error_index = binary(iteration_blocks[0])
            if (raw_key[error_index]==0):
                    raw_key[error_index]=1
            else:
                raw_key[error_index]=0
            error_index = binary(iteration_blocks[1])
            if (raw_key[error_index]==0):
                    raw_key[error_index]=1
            else:
                raw_key[error_index]=0
        iter_number+=1
    return raw_key

def split_in_two_blocks(raw_key,size_of_first_block):
    shuffle = raw_key.shuffle()
    arr,a=[],[]
    keys = shuffle.keys()
    for i in range(size_of_first_block):
        a.append(keys[i])
    arr.append(a)
    a=[]
    for j in range(size_of_first_block,raw_key.size,1):
        a.append(keys[j])
    arr.append(a)
    return arr
