# main.py

from file2 import exec_with_globals
import file1  # 导入file1，但不直接使用，主要是为了让file1里的代码执行

if __name__ == "__main__":
    # 调用exec_with_globals，并传递file1的globals
    # 这里传递的globals是main.py的，因为我们想要避免直接从file1传递，可以根据需要调整
    exec_with_globals(globals())
