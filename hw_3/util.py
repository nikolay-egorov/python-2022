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
        a = MatrixHash([[3, 3, 5], [47, 4, 2], [5, 11, 8]])
        c = MatrixHash([[4, 7, 3], [47, 9, 1], [3, 1, -3]])
        a.write_to_file("artifacts/hash/A.txt")
        c.write_to_file("artifacts/hash/C.txt")
        b = MatrixHash([[1, 99, 4], [55, 49, -4], [9, 2, 1]])
        d = MatrixHash([[1, 99, 4], [55, 47, -4], [9, 2, 1]])
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
