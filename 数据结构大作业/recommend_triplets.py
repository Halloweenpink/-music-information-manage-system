import random
import pandas as pd
import numpy as np
import pandas as pd

name = 'p1'
# df = pd.read_excel(f'all_person/{name}.xlsx')
df = pd.read_excel(r'all_person/songs.xlsx')

unique_songs = pd.unique(df[['f1', 'f2', 'f3']].values.ravel('K')).tolist()
unique_songs = [song for song in unique_songs if pd.notna(song)]

class Triplet:
    def __init__(self, song1, song2, count):
        self.song1 = song1
        self.song2 = song2
        self.count = count


class TripletsList:
    def __init__(self):
        self.triplets = []

    def add_triplet(self, song1, song2):
        for triplet in self.triplets:
            if triplet.song1 == song1 and triplet.song2 == song2:
                triplet.count += 1
                return
        self.triplets.append(Triplet(song1, song2, 1))

    def get_top_triplets(self, n):
        top_triplets = []
        all_triplets = self.triplets.copy()

        for _ in range(min(n, len(all_triplets))):
            max_count = -1
            max_triplet = None
            for triplet in all_triplets:
                if triplet.count > max_count:
                    max_count = triplet.count
                    max_triplet = triplet

            top_triplets.append(max_triplet)
            all_triplets.remove(max_triplet)

        return top_triplets



triplets_list = TripletsList()

for _, row in df.iterrows():
    valid_songs = [song for song in row[['f1', 'f2', 'f3']] if pd.notna(song)]
    for i in range(len(valid_songs)):
        for j in range(i + 1, len(valid_songs)):
            triplets_list.add_triplet(valid_songs[i], valid_songs[j])

top_triplets = triplets_list.get_top_triplets(5)

# Display the top triplets
print("最高相关性的特征对:")
for triplet in top_triplets:
    print(f"{triplet.song1} - {triplet.song2}: {triplet.count}")

top_features = set()
for triplet in top_triplets:
    top_features.add(triplet.song1)
    top_features.add(triplet.song2)

top_features_list = list(top_features)

random_selection1 = random.sample(top_features_list, min(3, len(top_features_list)))
print("Random Selection 1:", "".join(random_selection1))
random_selection2 = random.sample(top_features_list, min(3, len(top_features_list)))
print("Random Selection 2:", "".join(random_selection2))
random_selection3 = random.sample(top_features_list, min(3, len(top_features_list)))
print("Random Selection 3:", "".join(random_selection3))

non_zero_count = len(triplets_list.triplets) * 3
print("三元组存储的内存占用:", non_zero_count)
print("邻接矩阵存储的内存占用:", len(unique_songs) * len(unique_songs))
