import argparse
import os
from filecmp import cmp
from collections import defaultdict
from itertools import combinations


def read_path_from_args():
    args_parser = argparse.ArgumentParser(add_help=False)
    args_parser.add_argument("path_name", type=str, nargs='+',
                             help="Path for search for duplicates")
    return args_parser.parse_args().path_name


def get_files_in_path(path_name):
    files_dict = defaultdict(list)
    for top, dirs, files in os.walk(path_name):
        for name in files:
            files_dict[name].append(os.path.join(top, name))
    return files_dict


def get_duplicates_files_dict(files_dict):
    duplicates_dict = {file: files_dict[file]
                       for file in files_dict
                       if len(files_dict[file]) != 1}
    return duplicates_dict


def get_duplicates_files(duplicates_dict):
    duplicates = defaultdict(list)
    for file_name, paths_for_file in duplicates_dict.items():
        for path1, path2 in combinations(paths_for_file, 2):
            if cmp(path1, path2):
                duplicates[file_name] += [os.path.dirname(path1),
                                          os.path.dirname(path2)]
        duplicates[file_name] = set(duplicates[file_name])
    return duplicates


def print_duplicates_files(duplicates_files, path):
    if not duplicates_files:
        print("\nДубликатов в папке {} не найдено:".format(path))
        return None
    print("\nНайдены следующие дубликаты в папке {}:\n".format(path))
    for key, pathes in duplicates_files.items():
        print("\nФайл '{}' наден в следующих папках:".format(key))
        print(", ".join(path_name for path_name in pathes))


if __name__ == '__main__':
    path_names = read_path_from_args()
    for path_name in path_names:
        files_dict = get_files_in_path(path_name)
        duplicates_files_dict = get_duplicates_files_dict(files_dict)
        real_duplicates = get_duplicates_files(duplicates_files_dict)
        print_duplicates_files(real_duplicates, path_name)
    print("\nПрограмма завершена")
