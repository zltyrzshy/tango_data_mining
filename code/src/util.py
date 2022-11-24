import csv
import os
from datetime import datetime
from typing import List

import pandas as pd


def read_csv_to_list(file: str) -> list[list]:
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lst = list(reader)

    for lst_ in lst:
        while '' in lst_:
            lst_.remove('')
        while '?' in lst_:
            lst_.remove('?')
    return lst


def data_reader(data_file):
    data_set = []
    with open(data_file, 'r') as f:
        for line in f:
            data_set.append(line.split()[3:])
    return data_set


def load_data_set(file="../resource/out.csv"):
    """
    Load a sample data set (From Data Mining: Concepts and Techniques, 3th Edition)
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """
    # data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
    #             ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
    #             ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    return read_csv_to_list(file)


def get_delta_time(start: datetime):
    delta_time = datetime.now() - start
    return delta_time.seconds + delta_time.microseconds / 1000000


def str_frozenset(set_: frozenset) -> str:
    str_ = str(set_)
    return str_[10:-1]


def str_dict(dict_: dict) -> str:
    res = ''
    for kv in dict_:
        res += kv + '\n'
    return res


def str_iter(items) -> str:
    res = ''
    for val in items:
        res += '{}\n'.format(val)
    return res


def spilt_list(lst: List[str]) -> List[List[str]]:
    """
    分割列表

    Args:
        lst: 初始列表

    Returns: 分割后的列表

    """
    res: List[List[str]] = []
    i = 0

    temp_lst: List[str] = []
    for val in lst:
        if pd.isnull(val):
            if len(temp_lst) != 0:
                res.append(temp_lst)
                temp_lst = []
            if len(res) == i:  # 当前没有空列
                i += 1
        else:
            temp_lst.append(val)
    if len(temp_lst) != 0:
        res.append(temp_lst)
    return res


def str_dict_iter(dict_: dict) -> str:
    res = ''
    for key, val in dict_.items():
        res += '{}\n'.format(key)
        res += str_iter(val) + '\n'
    return res


def check_dir(dir_name: str) -> None:
    assert all([not os.path.isfile(dir_name),
                os.path.isdir(dir_name),
                os.path.exists(dir_name)]), dir_name


def check_file(file_name: str) -> None:
    assert all([not os.path.isdir(file_name),
                os.path.isfile(file_name),
                os.path.exists(file_name)]), file_name
