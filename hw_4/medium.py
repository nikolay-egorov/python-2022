import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import reduce


# 0.50039259627 - goal for 2, 1000
# 0.25019629813 - goal for 4, 1000
def integrate(f, a, b, start=0, n_iter=1000):
    t = time.time_ns()
    acc = 0
    step = (b - a) / n_iter
    for i in range(start, n_iter):
        acc += f(a + i * step) * step
    # my_info = f"Thread:{threading.get_ident()}. At {t} started. Took {time.time() - t} s"
    my_info = f"Thread:{threading.get_ident()}. Started at {time.time()}."
    return acc, my_info


def parallel_integrate(f, a, b, *c, n_jobs=1, n_iter=1000):
    def boarder_generator():
        st = (b - a) / n_jobs
        cur = a
        made_twice = False
        while cur != b:
            if made_twice:
                made_twice = False
                cur += st
                yield cur
            else:
                made_twice = True
                yield cur

    def get_proper_manager():
        if len(c) == 1 and c[0] == "async":
            return ThreadPoolExecutor()
        else:
            return ProcessPoolExecutor()

    acc = 0
    futures = []
    thread_step = int(n_iter / n_jobs)

    # print(a)
    # print(b/ 2)
    # print(b/ 2)
    # print(b)
    # print("---")
    # for i in boarder_generator():
    #     print(i)
    # print("---")
    # return 0

    with get_proper_manager() as executor:
        boarders = boarder_generator()
        nxt = next(boarders, None)
        while nxt is not None:
            a_ = nxt
            b_ = next(boarders, None)
            futures.append(executor.submit(integrate, f, a_, b_, start=0, n_iter=thread_step))
            nxt = next(boarders, None)

        # for i in range(0, n_iter, thread_step):
        #     futures.append(executor.submit(integrate, f, a_, b_, start=0, n_iter=500))

        # futures.append(executor.submit(integrate, f, a, b / 2, start=0, n_iter=500))
        # futures.append(executor.submit(integrate, f, b / 2, b, start=0, n_iter=500))

    ans = reduce(lambda lhs, rhs: (lhs[0] + rhs[0], '\n'.join([lhs[1], rhs[1]])), map(lambda x: x.result(), futures))
    # for i in futures:
    #     acc += i.result()

    return ans


if __name__ == "__main__":
    print(integrate(math.cos, 0, math.pi / 2))
    print(parallel_integrate(math.cos, 0, math.pi / 2, "async", n_jobs=3))
