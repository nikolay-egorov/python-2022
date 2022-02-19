import numpy as np

from hw_3.matrix import Matrix
from hw_3.matrix_hash import MatrixHash
from hw_3.matrix_ufunc import UMatrix
from hw_3.util import Writer

if __name__ == "__main__":
    writer = Writer()
    a = Matrix([[1, 2, 3], [4, 5, 6]])
    b = Matrix([[1, 2, 3], [-4, -5, -6]])
    c = Matrix([[1, 2], [-4, -5], [1, 1]])
    # print(a + b)
    # # a += b
    # # print(a)
    # print(a * b) # should be mul
    # print(a @ c)
    # writer.write_results(level='ez')

    a = UMatrix(np.array([[1, 2, 3], [4, 5, 6]]))
    b = UMatrix(np.array([[1, 2, 3], [-4, -5, -6]]))
    c = UMatrix(np.array([[1, 2], [-4, -5], [1, 1]]))
    # print(a + b)
    # print(a - b)
    # print(a * b)
    # print(a @ c)
    # writer.write_results(level='medium')
    # writer.write_results(level='hash')

    a = MatrixHash([[1, 0, 1], [0, 1, 0], [0, 0, 1]])
    c = MatrixHash([[1, 0, 0], [0, 1, 0], [1, 0, 1]])
    print(a.__hash__())
    print(c.__hash__())
    # b = MatrixHash([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    b = MatrixHash([[1, 0, 1], [0, 2, 0], [1, 0, 1]])
    d = MatrixHash([[1, 0, 1], [0, 2, 0], [1, 0, 1]])
    print(a @ b != c @ d)
    # print(c @ d)
    # print(c @ d)

    writer.write_hash_results()
    