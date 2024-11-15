import re
import itertools
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st
import os

# 读取剧本文件
with open("data/甄嬛传剧本01-10.txt", encoding='utf-8') as f:
    script_text = f.read()

# 分割成场景，假设每个“第x幕”表示一个新场景
scenes = re.split(r'第\d+幕', script_text)

# 人物列表（可以根据实际人物名单修改）
characters = ["太监", "苏培盛", "皇帝", "皇后", "年羹尧", "太后", "徐进良", "小厦子", "竹息", "官员甲", "官员乙", "官员丙", "官员丁", "华妃", "剪秋", "绘春", "颂芝", "福子"]

# 生成共现统计
cooccurrence = pd.DataFrame(0, index=characters, columns=characters)

for scene in scenes:
    # 找出场景中出现的所有人物
    present_characters = [char for char in characters if char in scene]
    
    # 统计共现
    for char1, char2 in itertools.combinations(present_characters, 2):
        cooccurrence.loc[char1, char2] += 1
        cooccurrence.loc[char2, char1] += 1

# 创建 NetworkX 图
G = nx.Graph()

# 添加节点和边
for i, char1 in enumerate(characters):
    for j, char2 in enumerate(characters):
        if i < j and cooccurrence.loc[char1, char2] > 0:
            # 将 int64 转为 int
            weight = int(cooccurrence.loc[char1, char2])
            G.add_edge(char1, char2, weight=weight)


# 使用 Pyvis 创建可视化网络
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# 将 NetworkX 图导入 Pyvis
net.from_nx(G)

# 为每个节点设置头像图像
avatar_path = "images/"
for node in net.nodes:
    char_name = node['id']  # 人物名字
    image_file = os.path.join(avatar_path, f"{char_name}.png")
    print(image_file)
    if os.path.exists(image_file):  # 检查图片文件是否存在
        print("yes")
        node.shape = 'circularImage'
        node['image'] = image_file  # 设置头像路径

# 设置节点的物理效果，使其可以持续浮动
net.toggle_physics(True)

# 保存图为 HTML 文件
net.save_graph("network_graph.html")

# Streamlit 展示页面标题
st.title("《甄嬛传》人物共现知识图谱")

# 读取生成的 HTML 并嵌入到 Streamlit
with open("network_graph.html", "r", encoding="utf-8") as f:
    html_content = f.read()
    
# 使用 Streamlit 的组件显示 HTML 文件
st.components.v1.html(html_content, height=750)
