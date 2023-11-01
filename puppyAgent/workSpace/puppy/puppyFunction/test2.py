import sys
import io

# 创建一个新的 StringIO 对象，并将其设置为标准输出
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout

# 运行你的代码
print("这是我的代码的输出")

# 重置标准输出
sys.stdout = old_stdout

# 获取输出并保存到一个字符串中
output = new_stdout.getvalue()

print("捕获的输出:", output)
