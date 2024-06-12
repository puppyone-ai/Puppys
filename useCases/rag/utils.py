def remove_duplicates(input_list):

    return list(dict.fromkeys(input_list))


if __name__ == "__main__":
    original_list = ["apple", "banana", "apple", "orange", "banana"]
    unique_list = remove_duplicates(original_list)
    print(unique_list)  # 输出: ['apple', 'banana', 'orange']