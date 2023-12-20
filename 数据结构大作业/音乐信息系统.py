# 两大功能模块
# 1.1基于总曲库信息的“我的喜欢”歌单模糊搜索、歌曲添加及删除功能
# 1.1.1“我的喜欢”歌单信息展现
# 1.1.2总曲库模糊搜索歌曲
# 1.1.3向"我的喜欢"歌单中进行歌曲添加及删除
# 1.2基于百度paddlepaddle大模型（simbert-base-chinese）文本相似度分析的“今日推荐”功能
# 1.2.1利用无向图和展现目前用户“我的喜欢”歌单中所有歌曲的标签分析结果，给出当前用户的听歌偏好关联分析
# 1.2.2利用无序排序的加速算法Q按文本相似度进行排名，并依据这个给出用户的今日推荐歌曲
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from paddlenlp import Taskflow
from data import *


# 创建MusicAnalysisApp类来管理应用程序界面和功能，即GUI设计
class MusicAnalysisApp:
    def __init__(self, master):
        # GUI主框架
        self.master = master
        self.master.title("音节科技 - 个性化音乐推荐系统")
        # 设置窗口为全屏
        self.master.state('zoomed')
        self.text_display = tk.Text()
        self.vertexs = set()
        self.triplets_list = TripletsList()
        self.current_user = None
        # 打开登入界面
        self.create_login_widgets()
        # 加载背景图片
        self.background_image = tk.PhotoImage(file=system_background)
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # 触发函数
        self.create_login_widgets()

    # 创建登录界面
    def create_login_widgets(self):
        self.login_frame = tk.Frame(self.master, bg="")
        # 登陆界面上方的Title
        title_label = tk.Label(self.login_frame, text="音节科技", font=("Microsoft YaHei", 20))
        subtitle_label = tk.Label(self.login_frame, text="个性化音乐推荐App", font=("Microsoft YaHei", 12))
        # 放置账号密码输入框，密码用*掩饰
        self.label_username = tk.Label(self.login_frame, text="Username:")
        self.label_password = tk.Label(self.login_frame, text="Password:")
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.label_username.grid(row=2, column=0, pady=5)
        self.entry_username.grid(row=2, column=1, pady=5)
        self.label_password.grid(row=3, column=0, pady=5)
        self.entry_password.grid(row=3, column=1, pady=5)
        # 创建登入按钮，点击触发下方的 def login：
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.login_frame.pack(pady=50)

    # 用户账号密码信息与库匹配
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        account = accounts.find_account(username)
        if account and password == account.password:
            # 成功匹配则进入主界面
            self.current_user = username
            # 调用def load_data:  加载用户所有信息
            self.load_data()
            self.create_main_widgets()
        else:
            # 账号密码不匹配则报错
            messagebox.showerror("Login Failed", "密码错误或未找到该用户账号！")

    # 创建主界面
    def create_main_widgets(self):
        # 更换为图片的实际路径
        self.background_image = tk.PhotoImage(file='1.png')
        # 使用标签来显示背景图片
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # 原来的登入界面用主页面取代
        self.login_frame.destroy()
        self.main_frame = ttk.Notebook(self.master)
        # 设置 Combobox 的字体和大小
        large_font = ('Microsoft YaHei', 14)  # 您可以根据需要调整字体和大小
        # 设置listbox来存放功能模块：“我的喜欢”与“今日推荐”
        self.listbox1 = ttk.Combobox(self.master, values=["我的喜欢", "今日推荐"], font=large_font, width=20)
        self.listbox1.bind("<<ComboboxSelected>>", self.on_listbox1_select)
        self.listbox1.set("选择功能模块")
        self.listbox1.pack(pady=10)
        # 放置文本框
        self.text_display = tk.Text(self.master, height=25, width=60)
        self.text_display.pack(pady=10)
        # 公告栏信息设置
        self.text_display.insert(tk.END, "亲爱的公主与王子，欢迎收听音节科技！")
        # 放置删除、添加按钮
        self.add_song_button = tk.Button(self.main_frame, text=" Add ", command=self.add_song)
        self.add_song_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.delete_song_button = tk.Button(self.main_frame, text=" Del ", command=self.delete_song)
        self.delete_song_button.pack(side=tk.RIGHT)
        # 这里专门针对搜索框设计了GUI
        self.show_song_search()
        self.main_frame.pack(pady=50)

    # 处理选择列表框的功能设计，展示喜欢的歌单与今日推荐
    def on_listbox1_select(self, event):
        selected_option = self.listbox1.get()
        if selected_option == "我的喜欢":
            self.show_my_songs()
        elif selected_option == "今日推荐":
            self.show_today_recommend()

    # 显示"我的喜欢"歌单
    # 依次对用户信息表中的歌曲name与三个特征 f1 f2 f3进行输出
    def show_my_songs(self):
        # 先清空公告栏的文本信息，用以显示新的歌单信息
        self.text_display.delete(1.0, tk.END)
        # 使用self.df.iterrows()来循环遍历经过DataFrame转化的歌单信息的每一行；
        # 并对每个歌曲提取歌曲名称和标签信息；
        # index变量存储当前行的索引，row变量包含当前行的三个特征；
        for index, row in self.df.iterrows():
            song_name = row['song_name']
            labels = [row['f1'], row['f2'], row['f3']]
            labels_str = ', '.join(filter(None, map(str, labels)))
            display_text = f"Song{index + 1}: {song_name}\nLabels: {labels_str}\n"
            self.text_display.insert(tk.END, display_text)
            self.text_display.insert(tk.END, "________________________________________\n")

    # 显示歌曲搜索界面，这个函数只用在搜索框中，不用在"今日推荐"的搜索中
    # 这是搜索歌曲的GUI设计
    def show_song_search(self):
        self.search_frame = tk.Frame(self.main_frame)
        self.search_entry = tk.Entry(self.search_frame, font=("Microsoft YaHei", 12))
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=0, column=1)
        self.search_results_text = tk.Text(self.search_frame, height=5, width=40)
        self.search_results_text.grid(row=1, column=0, columnspan=2, pady=10)
        self.search_frame.pack(side=tk.LEFT, padx=(10, 0))

    # 歌曲搜索
    # 衔接调用pandas的DataFrame进行歌曲搜索
    def perform_search(self):
        search_query = self.search_entry.get()
        self.search_songs(search_query)

    # DataFrame 是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔型值）。
    # DataFrame 既有行索引也有列索引，在涉及到批量处理二维列表中众多数据的场景中有较高的便利性。
    # 使用DataFrame的str.contains来实现模糊匹配，找到包含搜索查询信息的歌曲名。
    # 通过遍历匹配的结果，获取每首歌曲的相关信息（歌曲名或标签）。
    def search_songs(self, search_query):
        self.search_results_text.delete(1.0, tk.END)
        matches = self.df[self.df['song_name'].str.contains(search_query, case=False)]
        if not matches.empty:
            for index, row in matches.iterrows():
                song_name = row['song_name']
                labels = [row['f1'], row['f2'], row['f3']]
                labels_str = ', '.join(filter(None, map(str, labels)))
                display_text = f"Song: {song_name}\nLabels: {labels_str}\n"
                self.search_results_text.insert(tk.END, display_text)
        else:
            self.search_results_text.insert(tk.END, "没有找到这个歌曲.\n")

    # 删除歌曲的函数delete_song
    # 查询song_name，在信息表中实现删除并直接更新信息表
    def delete_song(self):
        song_name = simpledialog.askstring("Delete Song", "Enter the song name to delete:")
        if song_name:
            if song_name in self.df['name'].values:
                self.df = self.df[self.df['name'] != song_name]
                self.df.to_excel(accounts[self.current_user]["excel_file"], index=False)
                messagebox.showinfo("Song Deleted", f"{song_name} deleted successfully!")
                self.show_my_songs()
            else:
                messagebox.showerror("Error", f"{song_name} not found in the list.")

    # 添加歌曲的函数add_song
    def add_song(self):
        song_name = simpledialog.askstring("Add Song", "Enter the song name:")
        # 第一步输入歌曲名字
        if song_name:
            label_input = simpledialog.askstring("添加歌曲",
                                                 f"Enter three labels for {song_name} (separated by spaces):")
            # 第二步输入歌曲标签，且必须为3
            if label_input:
                labels = label_input.split()
                if len(labels) == 3:
                    new_data = pd.DataFrame(
                        {"name": [song_name], "f1": [labels[0]], "f2": [labels[1]], "f3": [labels[2]]})
                    # 满足条件则录入信息表，用concat方法实现数据连接
                    self.df = pd.concat([self.df, new_data], ignore_index=True)
                    self.df.to_excel(accounts[self.current_user]["excel_file"], index=False)
                    messagebox.showinfo("Song Added",
                                        f"{song_name} with labels {labels[0]}, {labels[1]}, {labels[2]} 添加成功！")
                else:
                    messagebox.showerror("出错了", "请至少添加三个标签")

    # 加载数据的函数load_data
    def load_data(self):
        account = accounts.find_account(self.current_user)
        if account:
            file_path = account.excel_file
            self.df = pd.read_excel(file_path)
            self.vertexs = set(self.df['f1'].unique()) | set(self.df['f2'].unique()) | set(self.df['f3'].unique())

    # 对于歌曲的曲风关联，均feature1、feature2等命名
    def show_today_recommend(self):
        self.text_display.delete(1.0, tk.END)
        # 创建实例对象
        triplets_list = TripletsList()
        # 依次遍历用户信息表中所有的歌曲包含三个特征
        for _, row in self.df.iterrows():
            valid_songs = [song for song in row[['f1', 'f2', 'f3']] if pd.notna(song)]
            # 将所有的符合条件的歌曲的特征进行两两配对，并添加到三元组列表中，进行计数统计
            for i in range(len(valid_songs)):
                for j in range(i + 1, len(valid_songs)):
                    triplets_list.add_triplet(valid_songs[i], valid_songs[j])
        # 获得特征关联数量排名最高的三元组(这里用取前5)
        top_triplets = triplets_list.get_top_triplets(5)

        # 展示总的曲库风格
        self.text_display.insert(tk.END, f"您的曲库风格总结：\n")
        for triplet in top_triplets:
            self.text_display.insert(tk.END, f"{triplet.feature1} - {triplet.feature2}: {triplet.count}\n")
        self.text_display.insert(tk.END, "\n\n")
        # 遍历 top_triplets，将每个三元组的特征1和特征2添加到集合top_features中。
        # 这个集合将包含所有出现在top_triplets中的特征，而且不会有重复。
        top_features = set()
        for triplet in top_triplets:
            top_features.add(triplet.feature1)
            top_features.add(triplet.feature2)
        # 转化为文本，用以后续文本相似度分析
        top_features_list = list(top_features)
        top_features_str = "".join(top_features_list)

        # 去除重复项，确保关联标签是唯一的
        result = []
        merged_df = pd.concat([songs_df, self.df])
        unique_df = merged_df.drop_duplicates(keep=False)
        # 使用文本相似度进行歌曲特征的相似度计算（simbert-base-chinese）
        similarity = Taskflow("text_similarity")
        counter = 0  # 初始化计数器
        for _, f in unique_df.iloc[:, 1:].iterrows():
            f = "".join(f.values)
            t = similarity([[f, top_features_str]])
            sim = similarity([[f, top_features_str]])[0]["similarity"]
            # 使用计数器而非原始索引
            result.append([counter, sim])
            # 更新计数器
            counter += 1
        # 对文本相似度得分进行排序
        result.sort(key=lambda x: x[-1], reverse=True)
        # 取前15名
        scores = list(x[0] for x in result[:15])
        recommand_songs = unique_df.iloc[scores, :].values
        # 依次展示推荐的歌曲
        for i, recommended_song in enumerate(recommand_songs):
            self.text_display.insert(tk.END,
                                     f"今日推荐歌曲{i + 1}: {recommended_song[0]} 曲风：{' '.join(recommended_song[1:])}\n")


# 创建Triplet类来表示三元组（feature1，feature2，count）
class Triplet:
    def __init__(self, feature1, feature2, count):
        self.feature1 = feature1
        self.feature2 = feature2
        self.count = count


# 创建TripletsList类来管理多个三元组对象
class TripletsList:
    def __init__(self):
        self.triplets = []

    # 添加或更新三元组的计数，如果已存在相同的feature1和feature2，则增加计数
    def add_triplet(self, feature1, feature2):
        for triplet in self.triplets:
            if triplet.feature1 == feature1 and triplet.feature2 == feature2:
                triplet.count += 1
                return
        # 否则创建新的三元组对象，并将其添加到列表中
        self.triplets.append(Triplet(feature1, feature2, 1))

    # 返回计数最高的n个三元组
    # 无序排序的加速算法Q
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


def main():
    root = tk.Tk()
    app = MusicAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
