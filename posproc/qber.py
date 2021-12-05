from posproc import*
# import time
def qber_estimation(active_client : QKDClient, fraction = 0.1, seed = None):
    """
    Estimates the qber between the keys of Server(Alice) and Client(Bob).

    Args:
        key_size (int): Size of the current key.
        active_client (Client): The object Bob. 
        fraction (float, optional): The fraction of total bits to use for qber estimation. Defaults to 0.1.

    Returns:
        [float]: The fraction of bits that are different.
    """
    # Initialize the seed state.
    # t1_start = time.perf_counter()
    random.seed(seed)
    # Generate random indexes to be used for qber estimation.
    key_size = active_client._current_key._size
       
    indexes = random.sample(range(key_size),int(fraction*key_size))
    
    sample_length = len(indexes)
    # # print(f"Indexes: {indexes}")
    # t1_end = time.perf_counter()
    # # print("QBER STEP 1 TIME:",t1_end-t1_start)
    # Get the bit values that bob and alice have. 
    # t2_start = time.perf_counter()
    active_client.console_output(f"Estimating qber between Alice and Bob.\n")
    raw_key_a = active_client.ask_server_for_bits_to_estimate_qber(indexes)    
    # t2_end = time.perf_counter()
    # # print("QBER STEP 2 TIME:",t2_end-t2_start)

    # t3_start = time.perf_counter()
    raw_key_b = active_client.get_bits_for_qber(indexes)
    # t3_end = time.perf_counter()
    # # print("QBER STEP 3 TIME:",t3_end-t3_start)
    # # print(f"raw_key_a: {raw_key_a}")
    # # print(f"raw_key_b: {raw_key_b}")

    diff = 0
    for index in indexes:
        if raw_key_a[index] != raw_key_b[index]:
            diff += 1
    # Return the fraction of bits that are different
    # t3_end = time.perf_counter()
    
    return float(diff/sample_length)