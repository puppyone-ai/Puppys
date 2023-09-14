# @Time : Sep/12/2023
# @Author : Guanqun Mu


import threading
import time

def crashing_thread():
    time.sleep(2)
    A=1/0

def normal_thread():
    while True:
        print("This thread is working normally.")
        time.sleep(3)

# 创建并启动两个线程
thread1 = threading.Thread(target=crashing_thread)
thread2 = threading.Thread(target=normal_thread)

thread1.start()
thread2.start()
print("Main thread is still alive.")
time.sleep(5)
print("Main thread is still alive.")
thread1.join()
thread2.join()
