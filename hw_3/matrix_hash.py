import numpy as np

from hw_3.matrix_ufunc import UMatrix


class MatrixHash(UMatrix):
    def __init__(self, data):
        super().__init__(data)

    # каждый элемент матрицы вносится в хеширование с фиксированным множителем как максимум по всем элементам матрицы;
    # следовательно, данная хеширование точно не будет совершенным и уж тем более универсальным
    def __hash__(self):
        ans = 0
        max_p = np.max(self.data)
        for i in range(self.rows):
            for j in range(self.cols):
                ans = max_p * ans + self.data[i][j]
        return int(ans)
