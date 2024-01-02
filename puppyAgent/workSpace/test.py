def split_string_by_hash(input_str):
    # 使用 split 方法按照 "##" 分割字符串
    parts = input_str.split("##")

    # 忽略第一个 "##" 之前的内容
    parts = parts[1:]

    # 为每个分割出的部分添加回 "##" 前缀，并存储到列表中
    results = ["##" + part for part in parts if part.strip()]

    return results

# 测试字符串
input_str = """
This is some introductory text.


## search the top 5 earphones in chinese market
print("hello")        



## send the top 5 earphones in chinese market to my email
# 所一定要有的包
print("sent")
"""

# 调用函数并打印结果
print(split_string_by_hash(input_str))

