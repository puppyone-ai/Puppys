# 示例：改变文本颜色

# 定义颜色
RED = "\033[31m"  # 红色
GREEN = "\033[32m"  # 绿色
YELLOW = "\033[33m"  # 黄色
RESET = "\033[0m"  # 重置颜色，回到默认颜色

# 使用颜色
print(RED + "这是红色的文字。" + RESET)
print(GREEN + "这是绿色的文字。" + RESET)
print(YELLOW + "这是黄色的文字。" + RESET)
