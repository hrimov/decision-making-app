from itertools import islice
from typing import Iterable


def batched(iterable: Iterable, batch_size: int):
    error_msg = "batch_size must be at least one"
    if batch_size < 1:
        raise ValueError(error_msg)
    it = iter(iterable)
    while batch := tuple(islice(it, batch_size)):
        yield batch
