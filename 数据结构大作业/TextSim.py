"""https://paddlenlp.readthedocs.io/zh/latest/model_zoo/taskflow.html#%E6%96%87%E6%9C%AC%E7%9B%B8%E4%BC%BC%E5%BA%A6"""
from paddlenlp import Taskflow
similarity = Taskflow("text_similarity")
sim = similarity([["SAT考试崩溃了啊","CET4考试好难"],
                  ["自考经验谈：自考生毕业论文选题技巧","本科未录取还有这些路可以走"],
                  ["本科未录取还有这些路可以走", "北京市  海淀区09年高考第二次模拟考试题"],
                  ["北京市海淀区09年高考第二次模拟考试题", "淘宝联手89家国际大牌打击侵权"],
                  ["淘宝联手89家国际大牌打击侵权", "腾讯联合360公司进行色情推广"]])
for e in sim:
    print(e["similarity"])
# print(similarity([["一", "1"],["大","小"]]))

