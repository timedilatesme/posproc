import random

def qber_estimation(key_size, active_client, fraction = 0.1, seed = None):
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
    random.seed(seed)
    # Generate random indexes to be used for qber estimation.   
    indexes = random.sample(range(key_size),int(fraction*key_size))
    
    sample_length = len(indexes)
    # print(f"Indexes: {indexes}")

    # Get the bit values that bob and alice have. 
    raw_key_a = active_client.ask_server_for_bits_to_estimate_qber(indexes)
    
    raw_key_b = active_client.get_bits_for_qber(indexes)
    # print(f"raw_key_a: {raw_key_a}")
    # print(f"raw_key_b: {raw_key_b}")
    
    diff = 0
    for index in indexes:
        if raw_key_a[index] != raw_key_b[index]:
            diff += 1
    # Return the fraction of bits that are different
    return float(diff/sample_length)