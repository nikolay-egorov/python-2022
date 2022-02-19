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

    def write_hash_results(self):
        os.makedirs("artifacts/hash", exist_ok=True)
        a = MatrixHash([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
        c = MatrixHash([[1, 0, 0], [0, 1, 0], [1, 0, 1]])
        a.write_to_file("artifacts/hash/A.txt")
        c.write_to_file("artifacts/hash/C.txt")
        b = MatrixHash([[1, 0, 1], [0, 2, 0], [1, 0, 1]])
        d = MatrixHash([[1, 0, 1], [0, 2, 0], [1, 0, 1]])
        b.write_to_file("artifacts/hash/B.txt")
        d.write_to_file("artifacts/hash/D.txt")
        fst = MatrixHash((a @ b).data)
        snd = MatrixHash((c @ d).data)
        fst.write_to_file("artifacts/hash/AB.txt")
        snd.write_to_file("artifacts/hash/CD.txt")
        with open("artifacts/hash/hash.txt", "w") as f:
            f.write(f"AB hash: {fst.__hash__()}\n")
            f.write(f"CD hash: {snd.__hash__()}")

    def write_results(self, level: str):
        os.makedirs("artifacts", exist_ok=True)
        constr = self.level[level]
        a = constr(np.random.randint(0, 10, (10, 10)))
        b = constr(np.random.randint(0, 10, (10, 10)))
        self.flash_to(a + b, mode="+", prefix=level)
        self.flash_to(a * b, mode="*", prefix=level)
        self.flash_to(a @ b, mode="@", prefix=level)
