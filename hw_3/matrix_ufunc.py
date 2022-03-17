import numpy as np


class BaseUnifiedMatrix:
    def __init__(self, data):
        if type(data) is list:
            self.data = np.array(data)
        else:
            self.data = data

    @property
    def rows(self):
        return self.data.shape[0]

    @property
    def cols(self):
        return self.data.shape[1]

    @rows.setter
    def rows(self, value):
        self.data.shape[0] = value

    @cols.setter
    def cols(self, value):
        self.data.shape[1] = value

    def __str__(self):
        return '\n'.join([str(row) for row in self.data])


class UMatrix(BaseUnifiedMatrix, np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, data):
        super().__init__(data)
        self.checkers = {
            "matmul": self.check_matr_product
        }

    _HANDLED_TYPES = (type(np.array), type(list), type(np.ndarray))

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def check_matr_product(self, lhs: 'UMatrix'):
        if self.rows != lhs.cols:
            raise Exception("Matrices dimensions don't match for multiplication!")

    def check_size(self, lhs:'UMatrix'):
        if self.rows != lhs.rows or self.cols != lhs.cols:
            raise Exception("Matrices dimensions don't match!")

    def __array_ufunc__(self, ufunc: np.ufunc, method, *inputs, **kwargs):
        for x in inputs:
            if not isinstance(x, self._HANDLED_TYPES + (UMatrix,)):
                return NotImplemented

        self.checkers.get(ufunc.__name__, self.check_size)(inputs[1])
        # print(ufunc)
        # print(method)
        # print(inputs)
        result = getattr(ufunc, method)(*map(lambda x: x.data, inputs), **kwargs)
        return UMatrix(result)
