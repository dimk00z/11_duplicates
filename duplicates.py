import argparse
import os
from filecmp import cmp


def read_path_from_args():
    args_parser = argparse.ArgumentParser(add_help=False)
    args_parser.add_argument("path_name", type=str, nargs='+',
                             help="Path for search for duplicates")
    return args_parser.parse_args().path_name


def get_files_in_path(path_name):
    files_list = []
    for top, dirs, files in os.walk(path_name):
        for name in files:
            files_list.append(os.path.join(top, name))
    return files_list


def are_files_equal(file1, file2):
    if file1 != file2 and cmp(file1, file2):
        return True


def is_not_duplicates_in_list(file1, file2, duplicates_files):
    if duplicates_files:
        for duplicates_for_file in duplicates_files:
            if file1 in duplicates_for_file and file2 in duplicates_for_file:
                return None
    return True


def get_duplicates_files(files_list):
    duplicates_files = []
    for file_path_1 in files_list:
        duplicates_for_file = []
        for file_path_2 in files_list:
            if is_not_duplicates_in_list(file_path_1,
                                         file_path_2, duplicates_files):
                if are_files_equal(file_path_1, file_path_2):
                    duplicates_for_file.append(file_path_2)
        if duplicates_for_file:
            duplicates_for_file.insert(0, file_path_1)
            duplicates_files.append(duplicates_for_file)
    return duplicates_files


def print_duplicates_files(duplicates_files, path):
    if not duplicates_files:
        print("\nДубликатов в папке {} не найдено:".format(path))
        return None
    print("\nНайдены следующие дубликаты в папке {}:\n".format(path))
    for duplicates in duplicates_files:
        print(", ".join(file_name for file_name in duplicates))


if __name__ == '__main__':
    path_names = read_path_from_args()
    for path_name in path_names:
        if not os.path.isdir(path_name):
            print('{} путь неверен'.format(path_name))
            continue
        files = get_files_in_path(path_name)
        print_duplicates_files(get_duplicates_files(files), path_name)
    print("\nПрограмма завершена")
