import glob
import logging

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from efficient_apriori import apriori
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud

import util

logging.basicConfig(filename='../../log/apriori.log', encoding='utf-8', filemode='w',
                    level=logging.DEBUG, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%I:%M:%S')
logging.info('Apriori Algorithm:\n')
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
        # 每三个文件单独进行规则挖掘
        item_sets, rules = apriori(datas, min_support=minsup, min_confidence=minconf)
        logging.info('item_sets: \n{}'.format(util.str_dict_iter(item_sets)))
        logging.info('rules: \n{}'.format(util.str_iter(rules)))
        summ = [rules]
        datas = []
        # 准备可视化数据
        col = ['support', 'confidence']
        all_rule = []
        df = pd.DataFrame(columns=col)
        for ans in summ:
            for rule in ans:
                df.loc[len(df.index)] = [rule.support, rule.confidence]
                onerule = '{' + str(rule.lhs) + '}->{' + str(rule.rhs) + '}'
                all_rule.append(str(rule.lhs))
                all_rule.append(str(rule.rhs))
        df.info()
        # 绘制支持度和置信度的散点图
        fonts = FontProperties(fname="../../resources/word.ttf", size=14)
        df.plot(kind="scatter", x="support", c="r",
                y="confidence", s=20, figsize=(8, 5))
        plt.grid("on")
        plt.xlabel("support", fontproperties=fonts, size=12)
        plt.ylabel("confidence", fontproperties=fonts, size=12)
        plt.title("散点图", fontproperties=fonts)
        plt.show()
        # 词云（可视化）
        s = ''.join(all_rule)
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace("'", '')
        wordcloud = WordCloud(background_color='white', font_path='../../../data/word.ttf', width=1000, height=860,
                              margin=2).generate(s)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        # 规则之间的网图连线（可视化）
        plt.figure(figsize=(12, 12))
        G = nx.DiGraph()
        for ans in summ:
            for rule in ans:
                G.add_edge(rule.lhs, rule.rhs, weight=rule.support)
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.3]
        emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] <= 0.3) & (d['weight'] >= 0.2)]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.2]
        pos = nx.circular_layout(G)
        nx.draw_networkx_nodes(G, pos, alpha=0.4, node_size=300)
        nx.draw_networkx_edges(G, pos, edgelist=elarge,
                               width=2, alpha=0.6, edge_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=emidle,
                               width=2, alpha=0.6, edge_color='g', style='dashdot')
        nx.draw_networkx_edges(G, pos, edgelist=esmall,
                               width=2, alpha=0.6, edge_color='b', style='dashed')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='simhei')
        plt.axis('off')
        plt.show()
