import queue
import threading

def consumer(q):
    while True:
        item = q.get()
        # 处理项目
        print(f'处理: {item}')
        q.task_done()

q = queue.Queue()
# 启动消费者线程
t = threading.Thread(target=consumer, args=(q,))
t.daemon = True
t.start()

# 生产者添加项目到队列
for item in range(10):
    q.put(item)

# 等待队列中的所有项目都被处理
q.join()
print('所有项目已处理完毕。')
