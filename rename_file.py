import os
import re
from pathlib import Path

# Translation dictionary
translations = {
    # C++ related
    "c++11新特性": "cpp11_new_features",
    "c++内存管理": "cpp_memory_management",
    "c++基础": "cpp_basics",
    "c++对象优化": "cpp_object_optimization",
    "从编译器理解 c++": "understanding_cpp_from_compiler",
    "从编译器角度理解c++的编译和链接过程": "understanding_cpp_compilation_and_linking_process",
    "函数的堆栈调用过程": "function_stack_call_process",
    "进程虚拟地址空间划分": "process_virtual_address_space_division",
    "设计模式": "design_patterns",
    # Database related
    "mysql 实战经验": "mysql_practical_experience",
    "从根上理解mysql": "understanding_mysql_fundamentals",
    # Leetcode translations (without numbers)
    "路径总和": "path_sum",
    "二叉树中的最大路径和": "binary_tree_maximum_path_sum",
    "岛屿数量": "number_of_islands",
    "K个一组翻转链表": "reverse_nodes_in_k_group",
    "无重复字符的最长子串": "longest_substring_without_repeating_characters",
    "下一个排列": "next_permutation",
    "缺失的第一个正数": "first_missing_positive",
    "使用递归及非递归两种方式实现快速排序": "quicksort_recursive_and_non_recursive",
    "10亿个数中如何高效地找到最大的一个数以及最大的第 K 个数": "find_largest_and_kth_largest_in_billion_numbers",
    # Python related
    "模块": "module",
    "常用函数": "common_functions",
    "装饰器": "decorators",
    "文件处理": "file_processing",
}


def normalize_filename(filepath, filename):
    """Normalize a filename according to rules"""
    try:
        # Get directory name
        dir_name = os.path.basename(os.path.dirname(filepath)).lower()
        name, ext = os.path.splitext(filename)

        # Special handling for leetcode directory
        if dir_name == "leetcode":
            # Try to extract number prefix
            match = re.match(r"^(\d+)\.(.+)", name)
            if match:
                number, remaining = match.groups()
                translated_remaining = translations.get(remaining, remaining)
                return f"{number}.{translated_remaining}{ext}"

        # Normal translation for other files
        new_name = translations.get(name, name)

        # Clean up the filename
        new_name = new_name.replace(" ", "_")
        new_name = re.sub(r"[^\w\-_.]", "_", new_name)
        new_name = new_name.lower()

        return f"{new_name}{ext}"
    except Exception as e:
        print(f"Error processing filename {filename}: {str(e)}")
        return filename


def rename_files(directory):
    """Rename files in the given directory"""
    print(f"Starting to process directory: {directory}")

    # Collect all changes first
    changes = []

    for root, dirs, files in os.walk(directory):
        print(f"\nProcessing directory: {root}")

        for filename in files:
            if filename.endswith(".md"):
                old_path = os.path.join(root, filename)

                try:
                    new_filename = normalize_filename(old_path, filename)
                    new_path = os.path.join(root, new_filename)

                    if old_path != new_path:
                        changes.append((old_path, new_path))
                        print(f"Found file to rename: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

    # If we have changes, show them and ask for confirmation
    if changes:
        print("\nThe following files will be renamed:")
        for old_path, new_path in changes:
            print(f"\nFrom: {old_path}")
            print(f"To:   {new_path}")

        response = input("\nDo you want to proceed with renaming? (y/n): ")

        if response.lower() == "y":
            print("\nStarting to rename files...")
            for old_path, new_path in changes:
                try:
                    os.rename(old_path, new_path)
                    print(f"Successfully renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")
            print("\nFile renaming completed!")
        else:
            print("\nOperation cancelled.")
    else:
        print("\nNo files need to be renamed.")


if __name__ == "__main__":
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current working directory: {current_dir}")

        # Execute the renaming
        rename_files(current_dir)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(
            "Please make sure you have the necessary permissions and are in the correct directory."
        )
