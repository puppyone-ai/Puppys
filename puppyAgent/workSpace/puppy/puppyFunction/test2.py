import threading
import time

# 共享变量
shared_number = 0

# 创建一个条件变量
condition = threading.Condition()

# 第一个线程的函数：每秒数字加一
def increment_number():
    global shared_number
    while shared_number < 3:  # 限制循环直到 shared_number 达到 3
        with condition:  # 进入条件变量的上下文管理器
            time.sleep(1)  # 模拟工作
            shared_number += 1  # 增加数字
            print(f"Thread 1: Number incremented to {shared_number}")
            condition.notify_all()  # 通知所有等待的线程

# 第二个线程的函数：等待数字变为3
def wait_for_three():
    with condition:  # 进入条件变量的上下文管理器
        while shared_number < 3:
            condition.wait()  # 等待通知
        print(f"Thread 2: Number is {shared_number}, as expected")

# 创建线程
thread1 = threading.Thread(target=increment_number)
thread2 = threading.Thread(target=wait_for_three)

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("Both threads have finished their work.")

