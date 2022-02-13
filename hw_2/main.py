from hw_2.latex import generate_tex, save_as_tex
from ast_drawer import process

if __name__ == "__main__":
    # process("""def fib(n):
    #     ans = [1]
    #     a = b = 1
    #     for i in range(0, n - 1):
    #         c = b
    #         b = a + b
    #         ans.append(b)
    #         a = c
    #
    #     return ans
    # """)
    b = generate_tex([[1, 2, 3], [12, 44, 42]], image="artifacts/ast.png")
    print(b)
    save_as_tex(b, should_generate=True)
