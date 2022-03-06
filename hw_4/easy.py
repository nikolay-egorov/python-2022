import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from hw_1.fib import fib


def runner(n: int, is_single_thread_setup=False):
    start = time.time()
    if is_single_thread_setup:
        for _ in range(10):
            fib(n)
    else:
        fib(n)
    t = time.time() - start
    return t


def non_sync_runner(n: int, answer: list, mode):
    if mode == "async":
        with ThreadPoolExecutor() as executor:
            answer.append(list(executor.map(runner, [n] * 10)))
    else:
        with ProcessPoolExecutor() as executor:
            answer.append(list(executor.map(runner, [n] * 10)))


def create_results(n: int):
    times = [runner(n, is_single_thread_setup=True)]
    non_sync_runner(n, times, mode="async")
    non_sync_runner(n, times, mode="process")
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/easy.txt", "w", encoding="UTF-8") as text_file:
        text_file.write(f"Times measures for running fub func 10 times with argument= {n}\n")
        text_file.write(f"Sync: {int(times[0]):.2f} s\n")
        text_file.write(f"Multi-threaded version: {sum(times[1])/len(times[1]):.2f} s\n")
        text_file.write(f"Multi-processed version: {sum(times[2])/len(times[2]):.2f} s\n")


if __name__ == "__main__":
    create_results(100_000)
