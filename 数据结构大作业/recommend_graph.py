import random

import pandas as pd
import numpy as np
# name = input()
name = 'p1'
df = pd.read_excel(f'all_person/{name}.xlsx')
# df = pd.read_excel(r'C:/Users/H16/Desktop/songs.xlsx')
# 读取所有歌名（f1, f2, f3），去重后作为一个列表
unique_songs = pd.unique(df[['f1', 'f2', 'f3']].values.ravel('K')).tolist()
# 移除 NaN 值
unique_songs = [song for song in unique_songs if pd.notna(song)]

class AdjMat:
    def __init__(self, vertices):
        self.num_vertices = len(vertices)
        self.adj_mat = np.zeros((self.num_vertices, self.num_vertices))
        self.vertices = vertices
        self.vertex_to_index = {vertex: i for i, vertex in enumerate(vertices)}

    def add_count(self, v1, v2):
        index1 = self.vertex_to_index[v1]
        index2 = self.vertex_to_index[v2]
        if index1 != index2:
            self.adj_mat[index1][index2] += 1
            self.adj_mat[index2][index1] += 1

    def show_mat(self):
        print(self.adj_mat)

    def get_top_cooccurrences(self, n):
        # Flatten and sort the upper triangle of the matrix
        upper_triangle_indices = np.triu_indices(self.num_vertices, k=1)
        cooccurrences = self.adj_mat[upper_triangle_indices]
        sorted_indices = np.argsort(cooccurrences)[::-1]

        top_pairs = []
        for index in sorted_indices[:n]:
            i, j = upper_triangle_indices[0][index], upper_triangle_indices[1][index]
            top_pairs.append((self.vertices[i], self.vertices[j], cooccurrences[index]))

        return top_pairs

# 假设 df 已经加载并处理 unique_songs
vertexs = unique_songs
adjmat = AdjMat(vertexs)

# 遍历 DataFrame 的每一行，更新共现矩阵
for _, row in df.iterrows():
    valid_songs = [song for song in row[['f1', 'f2', 'f3']] if pd.notna(song)]
    for i in range(len(valid_songs)):
        for j in range(i + 1, len(valid_songs)):
            adjmat.add_count(valid_songs[i], valid_songs[j])

# 输出共现矩阵
adjmat.show_mat()
top_cooccurrences = adjmat.get_top_cooccurrences(5)
print(top_cooccurrences)

# 将前三组的特征去重并保存在一个列表中
top_features = set()
for pair in top_cooccurrences:
    top_features.update(pair[:2])  # 只取前两个元素，即特征对

# 将 set 转换为 list
top_features_list = list(top_features)

# 从这个列表中随机抽取三个特征
random_selection1 = random.sample(top_features_list, min(3, len(top_features_list)))
print(random_selection1)
random_selection2 = random.sample(top_features_list, min(3, len(top_features_list)))
print(random_selection2)
random_selection3 = random.sample(top_features_list, min(3, len(top_features_list)))
print(random_selection3)

non_zero_count = np.count_nonzero(adjmat.adj_mat)

print("非零元素的个数:", 3 * non_zero_count//2, len(unique_songs) * len(unique_songs))