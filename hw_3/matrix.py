import copy

import numpy as np


class Matrix:
    def __init__(self, data):
        self.m = copy.deepcopy(data)

    def __len__(self):
        return len(self.m)

    def __str__(self):
        return f"{[self.m[i] for i in range(len(self))]}"

    def check_size(self, rhs: 'Matrix'):
        if len(self) != len(rhs) or len(self.m[0]) != len(rhs.m[0]):
            raise ValueError(f"Matrices dimensions dont match!")

    def __mul__(self, rhs: 'Matrix'):
        a_rows = len(self)
        b_rows = len(rhs)
        if not (a_rows and b_rows):
            raise Exception("Matrices shall not be empty list")
        a_cols = len(self.m[0])
        b_cols = len(rhs.m[0])

        result_matr = list()
        if a_cols != b_rows:
            raise Exception("Matrices dimensions dont match!")

        for i in range(0, a_rows):
            cur_row = list()
            for j in range(0, b_cols):
                cur_element = 0
                for k in range(0, a_cols):
                    cur_element += (self.m[i][k] * rhs.m[k][j])
                cur_row.append(cur_element)

            result_matr.append(cur_row)

        return Matrix(result_matr)

    def __add__(self, rhs: 'Matrix'):
        new_matr = Matrix(self.m)
        new_matr += rhs
        return new_matr

    def __iadd__(self, rhs: 'Matrix'):
        self.check_size(rhs)
        a_rows = len(self)
        b_cols = len(rhs.m[0])

        for i in range(0, a_rows):
            for j in range(0, b_cols):
                self.m[i][j] += rhs.m[i][j]
        return self

    def __matmul__(self, rhs: 'Matrix'):
        self.check_size(rhs)
        new_matr = Matrix(self.m)
        a_rows = len(self)
        b_cols = len(rhs.m[0])

        for i in range(0, a_rows):
            for j in range(0, b_cols):
                new_matr.m[i][j] *= rhs.m[i][j]
        return new_matr
