import time
import multiprocessing


class A:
    l = []

    def insert(self, n):
        for i in range(n, n+n):
            self.l.append(i)
            print(self.l)


def square(num):
    """Squares a number and prints the result."""
    time.sleep(1)
    for i in range(500):
        print(i, end=" ")
    print()
    return num * num


if __name__ == "__main__":
    # Define processes
    ob = A()
    process1 = multiprocessing.Process(target=ob.insert, args=(5,))
    process2 = multiprocessing.Process(target=ob.insert, args=(10,))

    # Start processes
    process1.start()
    process2.start()

    # Wait for processes to finish
    process1.join()
    process2.join()

    # Print results (may not be in order due to parallel execution)
    # exitcode is 0 if successful
    print("Process 1 result:", process1.exitcode)
    print("Process 2 result:", process2.exitcode)
