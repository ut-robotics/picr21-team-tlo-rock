import multiprocessing as mp
import time

def f(n, a):
    while True:
        n.value = 3.1415927
        time.sleep(1)
        n.value = 0.0
        time.sleep(1)

def f2(n, a):
    while True:
        print(n.value)
        time.sleep(0.1)

def f3(n, a):
    while True:
        n.value = 22.6
        time.sleep(0.4)
        n.value = 16.6
        time.sleep(0.4)


if __name__ == '__main__':
    num = mp.Value('d', 0.0)
    arr = mp.Array('i', range(10))

    p = mp.Process(target=f, args=(num, arr))
    p2 = mp.Process(target=f2, args=(num, arr))
    p3 = mp.Process(target=f3, args=(num, arr))

    p3.start()
    p2.start()
    p.start()

    time.sleep(10)

    p.kill()
    p2.kill()
    p3.kill()

    print(num.value)
    print(arr[:])