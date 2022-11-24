import os
import pandas as pd


def xlsx_to_csv_pd():
    file_dir = r'..\data\raw'
    # 获得文件完整路径
    for root, dirs, files in os.walk(file_dir):
        for name in files:
            # 生成至同一目录下
            data_xls = pd.read_excel(os.path.join(root, name), index_col=0)
            data_xls.to_csv(os.path.join(root, name).replace('xlsx', 'csv'), encoding='utf-8')\



if __name__ == '__main__':
    xlsx_to_csv_pd()
