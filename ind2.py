#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

def list_dir(path, level=0, max_depth=None, show_files=True, file_ext=None):
    """
    Рекурсивно обходит директорию, печатая её содержимое в виде дерева.

    :param path: Путь к директории.
    :param level: Текущий уровень вложенности (используется для форматирования вывода).
    :param max_depth: Максимальная глубина рекурсии.
    :param show_files: Флаг, указывающий, нужно ли отображать файлы.
    :param file_ext: Расширение файлов для фильтрации.
    """
    if max_depth is not None and level > max_depth:
        return

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{'|   ' * level}|-- [Permission Denied]")
        return

    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            print(f"{'|   ' * level}|-- {entry}/")
            list_dir(full_path, level + 1, max_depth, show_files, file_ext)
        elif show_files:
            if file_ext is None or entry.endswith(file_ext):
                print(f"{'|   ' * level}|-- {entry}")

def main():
    """
    Главная функция, которая настраивает парсер аргументов, обрабатывает аргументы
    и вызывает функцию list_dir для отображения дерева каталога.
    """
    # Создание и настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description='Display a directory tree.',
        epilog='Example usage: python tree.py /path/to/dir -f -e .txt -d 2'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Root directory of the tree (default is current directory)'
    )
    parser.add_argument(
        '-f', '--files',
        action='store_true',
        help='Show files as well as directories'
    )
    parser.add_argument(
        '-e', '--extension',
        type=str,
        help='Filter files by extension (e.g., ".txt" to display only text files)'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        help='Limit the depth of the tree (e.g., 2 for showing up to two levels deep)'
    )

    args = parser.parse_args()
    root_dir = args.directory
    show_files = args.files
    file_ext = args.extension
    max_depth = args.depth

    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        return

    list_dir(root_dir, show_files=show_files, file_ext=file_ext, max_depth=max_depth)

if __name__ == '__main__':
    main()

