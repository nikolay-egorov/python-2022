import os
import time
from multiprocessing import Process
from threading import Thread

from hw_1.fib import fib


def runner(n: int, is_single_thread_setup=False):
    if is_single_thread_setup:
        start = time.time()
        for _ in range(10):
            fib(n)
        return time.time() - start
    fib(n)
    # t = time.time() - start
    # return t


def non_sync_runner(n: int, answer: list, mode):
    if mode == "async":
        subj = list([Thread(target=runner, args=(n,)) for _ in range(10)])
    else:
        subj = list([Process(target=runner, args=(n,)) for _ in range(10)])
    start = time.time()
    for i in subj:
        i.start()
    list(map(lambda x: x.join(), subj))
    answer.append(time.time() - start)


def create_results(n: int):
    times = [runner(n, is_single_thread_setup=True)]
    non_sync_runner(n, times, mode="async")
    non_sync_runner(n, times, mode="process")
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/easy.txt", "w", encoding="UTF-8") as text_file:
        text_file.write(f"Times measures for running fub func 10 times with argument= {n}\n")
        text_file.write(f"Sync: {int(times[0]):.2f} s\n")
        text_file.write(f"Multi-threaded version: {times[1]:.2f} s\n")
        text_file.write(f"Multi-processed version: {times[2]:.2f} s\n")


if __name__ == "__main__":
    create_results(100_000)
