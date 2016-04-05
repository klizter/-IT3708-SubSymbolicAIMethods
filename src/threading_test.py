from multiprocessing import Pool, TimeoutError
import time
import os

def do_work(i):
    return i+1

def main():
    pool = Pool(processes=4)

    print pool.map(do_work, range(10))

main()