import sys
from codecs import encode
from multiprocessing import Queue, Pipe, Process
from time import sleep, gmtime, strftime


def a_routine(q: Queue, my_ins, b_out):
    while True:
        if not q.empty():
            msg = q.get()
            b_out.send(msg.lower())

        while my_ins.poll():
            q.put(my_ins.recv())
        sleep(5)


def b_routine(my_ins, m_out):
    while True:
        msg = my_ins.recv()
        if msg:
            m_out.send(encode(msg, 'rot_13'))


class MPCommunicator:
    def __init__(self):
        self.__q = Queue()
        self.__main_pipe = Pipe()
        self.__a_pipe = Pipe()
        self.__b_pipe = Pipe()
        self.__pipes = {
            'A': self.__a_pipe,
            'B': self.__b_pipe,
        }
        self.__processes = []

    def __create_start_sub(self):
        a = Process(target=a_routine, args=(self.__q, self.__a_pipe[0], self.__b_pipe[1]))
        b = Process(target=b_routine, args=(self.__b_pipe[0], self.__main_pipe[1]))
        self.__processes.append(a)
        self.__processes.append(b)
        a.daemon = True
        b.daemon = True
        a.start()
        b.start()

    def get_proper_file(self):
        return open("artifacts/communication.log", "w")

    def run_main(self):
        my_ins, my_out = self.__main_pipe
        a_ins, a_out = self.__pipes['A']
        self.__create_start_sub()
        with self.get_proper_file() as f:
            print("Enter msgs to begin communication:")
            while True:
                msg = sys.stdin.readline()
                if not msg:
                    t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    f.write(f"{t}. Exit signal from the user\n")
                    break
                t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                f.write(f"{t}. Send msg: '{msg.strip()}' to A\n")
                a_out.send(msg)
                ans = my_ins.recv()
                t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                f.write(f"{t}. Received msg: '{ans.strip()}' from B\n")

        # for p in self.__processes:
        #     p.join()


if __name__ == "__main__":
    C = MPCommunicator()
    C.run_main()
