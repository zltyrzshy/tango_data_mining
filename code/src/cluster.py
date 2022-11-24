# code=utf-8
import glob
import os
from typing import List

import pandas as pd
import csv
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE


def make_corpus(year, keyword) -> list:
    corpus = []
    csv_files = glob.glob('../data/processed' + str(year) + '/*.csv')
    for csv_file in csv_files:
        data_list: List[str] = []
        # if csv_file == '../data/processed1/整体词频.csv':  # 不对整体词频.csv表格进行操作
        #     continue
        with open(csv_file, encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_list.append(row.get(keyword))
        # print(data_list)
        origin_str = ''
        for i in range(len(data_list)):  # 根据nan进行分割
            if data_list[i] == '' and len(origin_str) > 0:
                corpus.append(origin_str)
                origin_str = ''
            elif isinstance(data_list[i], str) and data_list[i] != '':
                origin_str = origin_str + data_list[i] + ' '
    # print(corpus)
    return corpus


def Kmeans(corpus, year, keyword, k):
    file_name = keyword + '_' + str(k) + '_' + str(year)
    font_path = '../result/' + file_name + '/' + file_name
    result_name = font_path + '.txt'
    os.mkdir('../result/' + file_name)
    doc = open(result_name, 'w', encoding='UTF-8')
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    frequent_matrix = vectorizer.fit_transform((corpus))  # 将文本转为词频矩阵
    tfidf = transformer.fit_transform(frequent_matrix)  # 计算tf-idf
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(weight)  # k=5
    centroid_list = kmeans.cluster_centers_  # 聚类中心
    labels = kmeans.labels_  # 聚类标签
    n_clusters_ = len(centroid_list)
    cluster_menmbers_list = []
    # 整理聚类结果
    for i in range(0, n_clusters_):
        menmbers_list = []
        for j in range(0, len(labels)):
            if labels[j] == i:
                menmbers_list.append(j)
        cluster_menmbers_list.append(menmbers_list)
    # 输出聚类结果
    for i in range(0, len(cluster_menmbers_list)):
        print('第' + str(i) + '类' + '---------------------', file=doc)
        for j in range(0, len(cluster_menmbers_list[i])):
            a = cluster_menmbers_list[i][j]
            print(corpus[a], file=doc)
    # 散点图数据准备，TSNE降维数，weight为tf-idf矩阵weight = tfidf.toarray()，
    tsne = TSNE(n_components=2)  # 使用TSNE降维
    decomposition_data = tsne.fit_transform(weight)
    x = []
    y = []
    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y, c=kmeans.labels_, marker="x")
    plt.xticks(())
    plt.yticks(())
    plt.savefig(font_path + '.png')
    plt.show()


if __name__ == '__main__':
    ks = [3,4]
    years = [1, 2, 3]
    keywords = ['关键词(我们的方法)', '关键词(TF-IDF)']
    for k in ks:
        for keyword in keywords:
            for year in years:
                corpus = make_corpus(year, keyword)
                Kmeans(corpus, year, keyword, k)
