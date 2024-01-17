import threading
import time

def worker():
    for i in range(5):
        print(f"工作线程: 正在执行任务 {i}")
        time.sleep(2)  # 模拟耗时任务
    print("工作线程: 完成所有任务")

def responder():
    while True:
        response = input("输入线程: 请输入您的回复: ")
        if response == "exit":
            print("输入线程: 结束")
            break
        else:
            print(f"输入线程: 您的回复是 '{response}'")

if __name__ == "__main__":
    worker_thread = threading.Thread(target=worker)
    responder_thread = threading.Thread(target=responder)

    worker_thread.start()
    responder_thread.start()

    worker_thread.join()
    responder_thread.join()
