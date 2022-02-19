import os
import numpy as np

from hw_3.matrix import Matrix
from hw_3.matrix_hash import MatrixHash
from hw_3.matrix_ufunc import UMatrix


class Writer:
    def __init__(self):
        self.mode = {
            "+": "matrix+.txt",
            "*": "matrix_mult.txt",  # got issue with invalid character
            "@": "matrix@.txt"
        }

        self.level = {
            'ez': Matrix,
            'medium': UMatrix,
            'hash': MatrixHash
        }

    def flash_to(self, data: 'Matrix', mode, prefix: str):
        name = self.mode[mode]
        os.makedirs(f"artifacts/{prefix}", exist_ok=True)
        with open(f"artifacts/{prefix}/{name}", 'w') as f:
            f.write('\n'.join([str(row) for row in data.data]))

    def write_results(self, level: str):
        os.makedirs("artifacts", exist_ok=True)
        constr = self.level[level]
        a = constr(np.random.randint(0, 10, (10, 10)))
        b = constr(np.random.randint(0, 10, (10, 10)))
        self.flash_to(a + b, mode="+", prefix=level)
        self.flash_to(a * b, mode="*", prefix=level)
        self.flash_to(a @ b, mode="@", prefix=level)
