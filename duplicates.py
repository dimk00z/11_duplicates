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
    if [file1, file2] not in duplicates_files and \
       [file2, file1] not in duplicates_files:
        return True


def get_duplicates_files(files_list):
    duplicates_files = []
    for file_path_1 in files_list:
        for file_path_2 in files_list:
            checked_duplicates = are_files_equal(file_path_1, file_path_2)
            if checked_duplicates and \
                    is_not_duplicates_in_list(file_path_1,
                                              file_path_2, duplicates_files):
                duplicates_files.append([file_path_1, file_path_2])
    return duplicates_files


def print_duplicates_files(duplicates_files, path):
    if not duplicates_files:
        print("\nДубликатов в папке {} не найдено:".format(path))
        return None
    print("\nНайдены следующие дубликаты в папке {}:".format(path))
    for duplicates in duplicates_files:
        print('{} и {}'.format(duplicates[0], duplicates[1]))


if __name__ == '__main__':
    path_names = read_path_from_args()
    for path_name in path_names:
        if not os.path.isdir(path_name):
            print('{} путь неверен'.format(path_name))
            continue
        print('Путь {}'.format(path_name))
        files = get_files_in_path(path_name)
        print_duplicates_files(get_duplicates_files(files), path_name)
    print("\nПрограмма завершена")
