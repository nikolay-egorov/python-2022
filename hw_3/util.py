import os
import numpy as np

from hw_3.matrix import Matrix


class Writer:
    def __init__(self):
        self.mode = {
            "+": "artifacts/matrix+.txt",
            "*": "artifacts/matrix_mult.txt",  # got issue with invalid character
            "@": "artifacts/matrix@.txt"
        }

    def flash_to(self, data: 'Matrix', mode):
        name = self.mode[mode]
        with open(name, 'w') as f:
            f.write('\n'.join([str(row) for row in data.m]))

    def write_results(self):
        os.makedirs("artifacts", exist_ok=True)
        a = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
        b = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
        self.flash_to(a + b, mode="+")
        self.flash_to(a * b, mode="*")
        self.flash_to(a @ b, mode="@")
