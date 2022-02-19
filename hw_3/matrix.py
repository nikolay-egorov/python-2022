import copy

import numpy as np


class Matrix:
    def __init__(self, data):
        if data is np.array:
            self.data = copy.deepcopy(data.tolist())
        else:
            self.data = copy.deepcopy(data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"{[self.data[i] for i in range(len(self))]}"

    def check_size(self, rhs: 'Matrix'):
        if len(self) != len(rhs) or len(self.data[0]) != len(rhs.data[0]):
            raise ValueError(f"Matrices dimensions don't match!")

    def __mul__(self, rhs: 'Matrix'):
        self.check_size(rhs)
        new_matr = Matrix(self.data)
        a_rows = len(self)
        b_cols = len(rhs.data[0])

        for i in range(0, a_rows):
            for j in range(0, b_cols):
                new_matr.data[i][j] *= rhs.data[i][j]
        return new_matr

    def __add__(self, rhs: 'Matrix'):
        new_matr = Matrix(self.data)
        new_matr += rhs
        return new_matr

    def __iadd__(self, rhs: 'Matrix'):
        self.check_size(rhs)
        a_rows = len(self)
        b_cols = len(rhs.data[0])

        for i in range(0, a_rows):
            for j in range(0, b_cols):
                self.data[i][j] += rhs.data[i][j]
        return self

    def __matmul__(self, rhs: 'Matrix'):
        a_rows = len(self)
        b_rows = len(rhs)
        if not (a_rows and b_rows):
            raise Exception("Matrices shall not be empty list")
        a_cols = len(self.data[0])
        b_cols = len(rhs.data[0])

        result_matr = list()
        if a_cols != b_rows:
            raise Exception("Matrices dimensions don't match for multiplication!")

        for i in range(0, a_rows):
            cur_row = list()
            for j in range(0, b_cols):
                cur_element = 0
                for k in range(0, a_cols):
                    cur_element += (self.data[i][k] * rhs.data[k][j])
                cur_row.append(cur_element)

            result_matr.append(cur_row)

        return Matrix(result_matr)
