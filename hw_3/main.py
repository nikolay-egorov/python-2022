from hw_3.matrix import Matrix
from hw_3.util import Writer

if __name__ == "__main__":
    writer = Writer()
    a = Matrix([[1, 2, 3], [4, 5, 6]])
    b = Matrix([[1, 2, 3], [-4, -5, -6]])
    print(a + b)
    a += b
    print(a)
    print(a @ b)
    writer.write_results()
