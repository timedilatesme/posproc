import pyldpc

class Reconciliation:
    """
    A single information reconciliation exchange between a client (Bob) and a server (Alice).
    """

    def __init__(self, classical_channel, noisy_key, estimated_bit_error_rate):
        """
        Create a Cascade reconciliation.

        Args:
            classical_channel (subclass of ClassicalChannel): The classical channel over which
                Bob communicates with Alice.
            noisy_key (Key): The noisy key that Bob has, which needs to be reconciliated.
            estimated_bit_error_rate (float): The estimated bit error rate in the noisy key.
        """

        # Store the arguments.
        self._classical_channel = classical_channel
        self._estimated_bit_error_rate = estimated_bit_error_rate
        self._noisy_key = noisy_key
        self._reconciled_key = None

        # Map key indexes to blocks.
        self._key_index_to_blocks = {}

        
    def get_noisy_key(self):
        return self._noisy_key

    def get_reconciled_key(self):
        return self._reconciled_key

    def reconcile(self):
        pass
        return self._reconciled_key