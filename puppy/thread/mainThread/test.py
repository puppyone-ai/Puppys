from halo import Halo
import time

# 定义一个函数来显示加载动画和已等待的时间
def waiting_with_timer(seconds):
    spinner = Halo(text='Loading', spinner='dots')
    start_time = time.time()

    spinner.start()
    for _ in range(seconds):
        # 更新spinner的文本来显示已经过去的时间
        elapsed_time = int(time.time() - start_time)
        spinner.text = f'Loading (已等待 {elapsed_time} 秒)'
        time.sleep(1)
    spinner.succeed('完成')

# 使用函数，例如等待5秒
waiting_with_timer(5)
