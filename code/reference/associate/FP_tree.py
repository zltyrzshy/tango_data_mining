import glob
import logging

import pandas as pd
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder  # 传入模型的数据需要满足特定的格式，可以用这种方法来转换为bool值，也可以用函数转换为0、1

import util

logging.basicConfig(filename='../../log/fp-growth.log', encoding='utf-8', filemode='w',
                    level=logging.DEBUG, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%I:%M:%S')
logging.info("FP-Grouth Algorithm : \n")
minsup = 0.2  # 最小支持度
minconf = 0.4  # 最小置信度
# 将所有xlsx表格中的 关键词(我们的方法) 列数据转换为二维列表
datas = []
xlsx_files = glob.glob('../../resources/*.xlsx')
i = 0
for xlsx_file in xlsx_files:
    if xlsx_file == '../../resources\\整体词频.xlsx':
        continue
    df = pd.read_excel(xlsx_file)
    words_list = df['关键词(我们的方法)'].values.tolist()  # 使用 关键词(我们的方法) 列数据进行操作
    words = []
    for word in words_list:
        if isinstance(word, float) and len(words) > 0:
            datas.append(words)
            words = []
        elif isinstance(word, str):
            words.append(word)
        else:
            pass
    i += 1
    if i % 3 == 0 or i == 11:
        df = pd.DataFrame(data=datas)
        df_arr = df.stack().groupby(level=0).apply(list).tolist()
        # 转换数据的模式
        te = TransactionEncoder()  # 定义模型
        df_tf = te.fit_transform(df_arr)
        df = pd.DataFrame(df_tf, columns=te.columns_)
        # 求频繁项集：
        frequent_itemsets = fpgrowth(df, min_support=minsup,
                                     use_colnames=True)  # use_colnames=True 表示使用元素名字，默认的False使用列名代表元素
        # 求关联规则： (metric可以有很多的度量选项，返回的表列名都可以作为参数)
        association_rule = association_rules(frequent_itemsets, metric='confidence', min_threshold=minconf)
        association_rule.sort_values(by='confidence', ascending=False, inplace=True)  # 关联规则可以按leverage排序
        rules_list = association_rule.values.tolist()
        logging.info('items:\n{}'.format(frequent_itemsets))
        logging.info('rules:\n{}'.format(util.tree_str_format(rules_list)))
        datas = []
