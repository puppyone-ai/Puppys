import os
import json

def sense_local_env():
    """
    This function senses the local environment by listing all files and directories in the current directory recursively.
    It returns the structure in a JSON format.
    """

    print("current path:", os.getcwd())

    # Initialize the tree structure
    tree = {}

    # Recursively list all files and directories
    for dir_path, dir_names, filenames in os.walk('.'):
        path_parts = dir_path.split(os.sep)
        current_level = tree

        # Traverse the path and create the tree structure
        for part in path_parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # Add files and directories to the current level
        current_level['files'] = filenames
        current_level['directories'] = dir_names

    print(tree)

    # Return the tree structure in JSON format
    return json.dumps(tree, indent=4)
