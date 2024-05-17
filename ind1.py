#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from random import randint
import argparse
import json
from pathlib import Path

def parse_arguments():
    """
    Парсит аргументы командной строки.

    Returns:
    - argparse.Namespace: Пространство имен с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description="Управление списком поездов.")
    parser.add_argument(
        "command", choices=["add", "list", "select", "help", "exit"], help="Команда для выполнения"
    )
    parser.add_argument("destination", nargs="?", help="Пункт назначения для команды select")
    return parser.parse_args()

def save_trains(trains, filename):
    """
    Сохраняет список поездов в файл в формате JSON.

    Args:
    - trains (list): Список поездов.
    - filename (str): Имя файла для сохранения.
    """
    with open(filename, 'w') as file:
        json.dump(trains, file)

def load_trains(filename):
    """
    Загружает список поездов из файла в формате JSON.

    Args:
    - filename (str): Имя файла для загрузки.

    Returns:
    - list: Список поездов.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def add_train(trains):
    """
    Добавляет информацию о поезде в список trains.

    Args:
    - trains (list): Список поездов.
    """
    train_num = int(input('Введите номер поезда: '))
    destination = input('Введите пункт назначения: ')
    start_time = input('Введите время выезда: ')
    trains.append({'num': train_num, 'destination': destination, 'start_time': start_time})
    if len(trains) > 1:
        trains.sort(key=lambda item: item['start_time'])

def list_trains(trains):
    """
    Выводит список поездов на экран.

    Args:
    - trains (list): Список поездов.
    """
    line = f'+-{"-" * 15}-+-{"-" * 30}-+-{"-" * 25}-+'
    print(line)
    header = f"| {'№ поезда':^15} | {'Пункт назначения':^30} | {'Время отъезда':^25} |"
    print(header)
    print(line)
    for train in trains:
        num = train.get('num', randint(1000, 10000))
        destination = train.get('destination', 'None')
        start_time = train.get('start_time', 'None')
        recording = f"| {num:^15} | {destination:^30} | {start_time:^25} |"
        print(recording)
    print(line)

def select_train(trains, cmd_parts):
    """
    Выводит информацию о поездах, направляющихся в указанный пункт.

    Args:
    - trains (list): Список поездов.
    - cmd_parts (list): Список команды и параметра.
    """
    cmd_destination = cmd_parts[1]
    if select_trains := [
        train
        for train in trains
        if train['destination'].strip() == cmd_destination
    ]:
        for train in select_trains:
            print(f'{train["num"]:^15}: {train["start_time"]:^25}')
    else:
        print('Нет поездов едущих в данное место!', file=sys.stderr)

def show_help():
    """
    Выводит список доступных команд на экран.
    """
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select <пункт назначения> - запросить поезда с пунктом назначения;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")

def main():
    """
    Основная функция программы.
    """
    home_dir = Path.home()
    filename = home_dir / 'trains.json'
    trains = load_trains(filename)
    args = parse_arguments()
    if args.command == 'add':
        add_train(trains)
        save_trains(trains, filename)
    elif args.command == 'list':
        list_trains(trains)
    elif args.command == 'select':
        if args.destination:
            select_train(trains, [args.command, args.destination])
        else:
            print("Необходимо указать пункт назначения для команды select")
    elif args.command == 'help':
        show_help()
    elif args.command == 'exit':
        save_trains(trains, filename)

if __name__ == '__main__':
    main()