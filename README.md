# -music-information-manage-system
来自本人结构科学大作业，基于paddlenlp实现用户歌曲推荐

一、问题描述  
本项目为针对音乐应用层的信息管理系统。  
其应用无向图实现关联共现次数的统计，使用三元组降低空间储存成本，利用无序排序的加速算法Q实现运行速度的优化，并结合了预训练的大语言模型SimBert-Base-Chinese实现了用户相似度分析和歌曲智能推荐。最后考虑了用户的个性化需求基于tinker模块进行下游可视化呈现和交互。  

考虑用户需求，初始化窗口会自动全屏调整为最大；  
若在python环境内运行，数据存放结构如下：  
----music_project  
	----all_person  
		----person_name1.xlsx  
		----person_name2.xlsx  
		----person_name3.xlsx  
		----……  
	----0.png  
	----1.png  
  	----data.py  
	----音乐信息系统.py  
其中0.png和1.png为默认的登录背景与用户背景的图片命名  
Paddle下载链接：https://www.paddlepaddle.org.cn/install/quick  
本项目采用gpu版，若部署电脑没有独立显卡，可下载cpu版本  
Paddle版本：paddlepaddle-gpu 2.5.2.post116  
Cuda版本：11.6  
paddlenlp版本：2.6.1  
python版本：3.8  
