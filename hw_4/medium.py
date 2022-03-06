import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import reduce


def integrate(f, a, b, start=0, n_iter=1000, silent_mode=False):
    t = time.time()
    acc = 0
    step = (b - a) / n_iter
    for i in range(start, n_iter):
        acc += f(a + i * step) * step
    # my_info = f"Thread:{threading.get_ident()}. At {t} started. Took {time.time() - t} s"
    if not silent_mode:
        t_ = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        my_info = f"Thread:{threading.get_ident()}. Started at {t_}."
    else:
        my_info = f"{time.time() - t}"
    return acc, my_info


def parallel_integrate(f, a, b, *c, n_jobs=1, n_iter=1000, silent_mode=False):
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

    futures = []
    thread_step = int(n_iter / n_jobs)

    t = time.time()

    with get_proper_manager() as executor:
        boarders = boarder_generator()
        nxt = next(boarders, None)
        while nxt is not None:
            a_ = nxt
            b_ = next(boarders, None)
            futures.append(executor.submit(integrate, f, a_, b_, start=0, n_iter=thread_step, silent_mode=silent_mode))
            nxt = next(boarders, None)
            if nxt is not None and abs(nxt - b) < 0.0000001:
                break

    ans = reduce(lambda lhs, rhs: (lhs[0] + rhs[0], '\n'.join([lhs[1], rhs[1]])), map(lambda x: x.result(), futures))
    total = time.time() - t
    # for i in futures:
    #     acc += i.result()

    return ans, total


def produce_results(inner_log_mode: bool, thread_count: int, mode: str, n_iter: int):
    def get_file_wrapper():
        if inner_log_mode:
            f = open(f"artifacts/medium_inner_logs_{mode}.txt", "w")
            f.write(f"Logs about task completion. Iterations: {n_iter}. Mode: {mode}\n")
            f.write("Threads\t\t\t\t Info\n")
            return f
        else:
            f = open(f"artifacts/medium_general_log_{mode}.txt", "w")
            f.write(f"Logs about general. Iterations: {n_iter}. Mode: {mode}\n")
            f.write("Threads\t\t\t\t Time\n")
            return f

    with get_file_wrapper() as f:
        if not inner_log_mode:
            t = integrate(math.cos, 0, math.pi / 2, silent_mode=True, n_iter=n_iter)
            f.write(f"Single-thread result. Time taken: {float(t[-1]):.6f} ms\n\n")

        for i in range(2, thread_count * 2 + 1):
            res = parallel_integrate(math.cos, 0, math.pi / 2, mode, n_jobs=i, n_iter=n_iter, silent_mode=not inner_log_mode)
            if inner_log_mode:
                f.write(f"{i}:\n{res[0][-1]}\n")
            else:
                f.write(f"{i}\t\t{float(res[-1]):.6f}\n")


if __name__ == "__main__":
    # print(integrate(math.cos, 0, math.pi / 2, n_iter=100000))
    # print(parallel_integrate(math.cos, 0, math.pi / 2, "async", n_jobs=6, n_iter=100000))
    produce_results(False, 8, "async", 100000)
    produce_results(False, 8, "process", 100000)
    produce_results(True, 8, "async", 100000)
    produce_results(True, 8, "process", 100000)
