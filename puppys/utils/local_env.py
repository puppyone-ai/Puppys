import os


def sense_local_env():

    print("当前工作目录:", os.getcwd())

    # 递归式地列出当前目录下的所有文件
    tree = {}

    for dir_path, dir_names, filenames in os.walk('.'):

        path_parts = dir_path.split(os.sep)
        current_level = tree

        for part in path_parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        current_level['files'] = filenames
        current_level['directories'] = dir_names

    print(tree)

    import json
    return json.dumps(tree, indent=4)
