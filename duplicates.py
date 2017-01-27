import argparse
import os
from filecmp import cmp


def read_path_from_args():
    args_parser = argparse.ArgumentParser(add_help=False)
    args_parser.add_argument("path_name", type=str, nargs='+',
                             help="Path for search for duplicates")
    return args_parser.parse_args().path_name


def get_files_in_path(path_name):
    files_dict = {}
    for top, dirs, files in os.walk(path_name):
        for name in files:
            if name in files_dict.keys():
                files_dict[name].append(os.path.join(top, name))
            else:
                files_dict[name] = []
                files_dict[name].append(os.path.join(top, name))
    return files_dict


def remove_from_dict_single_files(files_dict):
    keys_for_remove = []
    for key in files_dict:
        if len(files_dict[key]) == 1:
            keys_for_remove.append(key)
    for key in keys_for_remove:
        files_dict.pop(key)
    return files_dict


def add_path_to_duplicates(paths, duplicate):
    for path in paths:
        if os.path.dirname(path) not in duplicate:
            duplicate.append(os.path.dirname(path))


def get_duplicates_files(files_dict):
    duplicates_files = {}
    for file_name in files_dict:
        for path1 in files_dict[file_name]:
            duplicates_for_file = []
            for path2 in files_dict[file_name]:
                if path1 == path2:
                    continue
                if cmp(path1, path2):
                    add_path_to_duplicates([path1, path2], duplicates_for_file)
            if duplicates_for_file:
                duplicates_files[file_name] = duplicates_for_file
    return duplicates_files


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
        files = get_files_in_path(path_name)
        files = remove_from_dict_single_files(files)
        duplicates = get_duplicates_files(files)
        print_duplicates_files(duplicates, path_name)
    print("\nПрограмма завершена")
