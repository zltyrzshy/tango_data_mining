import os
from collections import deque
from typing import Deque, List

import pandas as pd

from src import util


def get_csv_s(dir_name: str) -> Deque[str]:
    """

    Args:
        dir_name: 文件根目录

    Returns: csv文件路径

    """
    csv_list: List[str] = []
    util.check_dir(dir_name)
    for path in os.listdir(dir_name):
        if any([os.path.isdir(path),
                not path.endswith('.csv'),
                path == '整体词频.csv']):
            continue

        csv_list.append(os.path.join(dir_name, path))
    csv_list.sort()
    return deque(csv_list)


def pre_process(csv_s: Deque[str], year_num: int, col_name: str) -> Deque[List[List[str]]]:
    """
    将临近几年的数据合为一个样本
    Args:
        csv_s: 文件根目录
        year_num: 几年合并成一个
        col_name: 列名称
    Returns: 若干二维矩阵

    """
    res: Deque[List[List[str]]] = deque()
    i = -1
    year_i = year_num
    for csv in csv_s:
        if year_i == year_num:  # 该下一个样本
            i += 1
            year_i = 0
            res.append([])
        series = pd.read_csv(csv)[col_name].values.tolist()
        spilt_lists = util.spilt_list(series)
        for row in spilt_lists:
            res[i].append(row)

        year_i += 1
    return res
