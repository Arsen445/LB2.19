#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import pathlib


def get_train(staff, dist, time, typ):
    """
    Запросить данные о поезде.
    """

    staff.append({
        "dist": dist,
        "time": time,
        "typ": typ,
    })

    return staff


def display_trains(staff):
    """
    Отобразить список поездов.
    """
    # Проверить, что список поездов не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4,
            "-" * 30,
            "-" * 20,
            "-" * 15
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^15} |".format(
                "No",
                "Пункт назначения",
                "время поезда",
                "Тип поезда"
            )
        )
        print(line)

        # Вывести данные о всех самолетах.
        for idx, train in enumerate(staff, 1):
            if isinstance(train, dict):
                print(
                    "| {:>4} | {:<30} | {:<20} | {:>15} |".format(
                        idx,
                        train.get('dist', ''),
                        train.get('time', 0),
                        train.get('typ', ''),
                    )
                )
            else:
                print("Error: Invalid train format.")

        print(line)

    else:
        print("Список поездов пуст")


def select_trains(staff, typ):
    """
    Выбрать поезда с заданным типом.
    """
    found = False
    for train in staff:
        if train.get('typ') == typ:
            found = True
            print(
                ' | {:<5} | {:<5} '.format(
                    train.get('dist', ''),
                    train.get('time', ''),
                )
            )

    if not found:
        print("Такого типа нет!")


def save_trains(file_name, staff):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))


def load_trains(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
    return loadfile


def main(command_line=None):
    """
    Главная функция программы.
    """

    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("staff")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления поезда.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add new train"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The station`s name"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        type=int,
        required=True,
        help="Train departure time"
    )
    add.add_argument(
        "-p",
        "--typ",
        action="store",
        help="The type of train"
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all trains"
    )
    # Создать субпарсер для выбора поездов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the trains"
    )
    select.add_argument(
        "-s",
        "--selected trains",
        required=True,
        help="The selected trains"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        staff = load_trains(args.filename)
    else:
        staff = []
    if args.command == "add":
        staff = get_train(
            staff,
            args.name,
            args.time,
            args.typ
        )
        is_dirty = True
    elif args.command == 'display':
        display_trains(staff)
    elif args.command == 'select':
        display_trains(select_trains(staff, args.typ))

    if is_dirty:
        save_trains(args.filename, staff)


if __name__ == '__main__':
    main()
