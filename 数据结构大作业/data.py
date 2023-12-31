import pandas as pd


class Node:
    def __init__(self, username, password, excel_file):
        self.username = username
        self.password = password
        self.excel_file = excel_file
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_account(self, username, password, excel_file):
        new_node = Node(username, password, excel_file)
        new_node.next = self.head
        self.head = new_node

    def find_account(self, username):
        current = self.head
        while current:
            if current.username == username:
                return current
            current = current.next
        return None


accounts = LinkedList()
accounts.add_account("abc", "123456", "all_person/abc.xlsx")
accounts.add_account("def", "123456", "all_person/def.xlsx")
accounts.add_account("ghi", "123456", "all_person/ghi.xlsx")
accounts.add_account("", "", "all_person/ghi.xlsx")  # 开发者作弊路径，无需密码和用户名


# 歌曲总曲库
songs_df = pd.read_excel(r"all_person/songs.xlsx")
system_background = '0.png'
