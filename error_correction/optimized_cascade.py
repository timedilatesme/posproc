from error_correction.cascade import ask_block_parity, calculate_parity ,binary


def binconf(raw_key,no_of_biconf_iter):
    iter_number = 0
    while(iter_number<no_of_biconf_iter):
        iteration_blocks = split_in_two_blocks(raw_key)
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
        return raw_key

def split_in_two_blocks():
    pass
