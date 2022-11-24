import csv
from datetime import datetime

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


def load_data_set(file):
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


def str_dict_iter(dict_: dict) -> str:
    res = ''
    for key, val in dict_.items():
        res += '{}\n'.format(key)
        res += str_iter(val) + '\n'
    return res


def xlsx_to_csv(file1, file2):
    data_xlsx = pd.read_excel(file1, index_col=0)
    # print(data_xlsx.info)
    data_xlsx.to_csv(file2, encoding='utf-8')


def frozenset_to_set(f):
    des_set = set([])
    for i in f:
        des_set.add(i)
    return des_set


# fp_growth算法关联规则输出格式
def tree_str_format(lists) -> str:
    des_str = ''
    for rule in lists:
        des_str += "{} -> {}, (conf={:.3f}, supp={:.3f}, lift={:.3f}, conv={:.3f})\n".format(frozenset_to_set(rule[0]),
                                                                                             frozenset_to_set(rule[1]),
                                                                                             rule[5], rule[4], rule[6],
                                                                                             rule[8])
    return des_str
