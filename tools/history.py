import networkx as nx
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import streamlit as st
import time
from matplotlib import font_manager

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体 SimHei 显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 初始化角色和关系数据
characters = [
    "甄嬛", "皇帝", "皇后", "华妃", "敬妃", "沈眉庄", "安陵容", "端妃", "皇太后",
    "温实初", "苏培盛", "曹贵人", "齐妃", "祺贵人", "淳常在", "叶澜依", "富察贵人",
    "欣常在", "槿汐", "剪秋", "玉娆", "小允子", "流朱", "余答应", "欣贵人", "静妃",
    "敬贵人", "温仪", "舒太妃", "方淑仪", "孟静娴", "王爷", "王儇", "敬贵妃", 
    "十七爷", "太监", "太后", "年羹尧", "徐进良", "小厦子", "竹息", "官员甲", 
    "官员乙", "官员丙", "官员丁", "端贵妃", "曹琴默", "眉庄", "端敬", "妙音娘子"
]

# 示例共现数据
cooccurrence = pd.DataFrame(0, index=characters, columns=characters)

# 设置示例共现关系（此处可以加载真实的数据）
for char1, char2 in itertools.combinations(characters[:10], 2):  # 示例使用部分角色
    cooccurrence.loc[char1, char2] = 1
    cooccurrence.loc[char2, char1] = 1

# 初始化图对象
G = nx.Graph()

# 计算角色组合的总数
character_combinations = list(itertools.combinations(characters[:10], 2))

# Streamlit 图像显示容器
graph_placeholder = st.empty()

# 逐步绘制图谱并显示每一帧
nodes_added = set()
edges_added = set()

for idx, (char1, char2) in enumerate(character_combinations):
    if cooccurrence.loc[char1, char2] > 0:
        G.add_node(char1)
        G.add_node(char2)
        G.add_edge(char1, char2, weight=cooccurrence.loc[char1, char2])

        nodes_added.add(char1)
        nodes_added.add(char2)
        edges_added.add((char1, char2))

    # 重新计算布局
    pos = nx.spring_layout(G, seed=22)
    
    # 清空并绘制图形
    plt.figure(figsize=(5, 5))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=500, edge_color="gray", font_size=10)
    plt.title(f"角色关系图谱动态展示 - 步骤 {idx + 1}")
    
    # 将当前帧显示在 Streamlit 页面中
    graph_placeholder.pyplot(plt)
    plt.close()  # 关闭图像以防内存泄露
    
    # time.sleep(0.5)  # 延迟用于模拟动画效果
