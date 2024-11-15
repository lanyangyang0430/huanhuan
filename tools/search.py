import re
import itertools
import pandas as pd
import streamlit as st
from streamlit_d3graph import d3graph
import os

# 获取所有剧本文件路径并排序，确保按照顺序排列
script_files = sorted([f for f in os.listdir("data") if f.startswith("甄嬛传剧本") and f.endswith(".txt")])

# 在左侧栏创建时间轴滑块，允许用户选择剧本文件区间
time_index = st.sidebar.slider("选择要查看的剧本时间点", min_value=0, max_value=len(script_files)-1, format="剧本章节 %d", step=1)
selected_script = script_files[time_index]

# 显示当前选择的剧本章节
st.write(f"当前选择的剧本章节：{selected_script}")

# 读取选定剧本文件内容
with open(os.path.join("data", selected_script), encoding='utf-8') as f:
    script_text = f.read()

# 分割成场景，假设每个“第x幕”表示一个新场景
scenes = re.split(r'第\d+幕', script_text)

# 完整的角色列表
characters = [
    "甄嬛", "皇帝", "皇后", "华妃", "敬妃", "沈眉庄", "安陵容", "端妃", "皇太后",
    "温实初", "苏培盛", "曹贵人", "齐妃", "祺贵人", "淳常在", "叶澜依", "富察贵人",
    "欣常在", "槿汐", "剪秋", "玉娆", "小允子", "流朱", "余答应", "欣贵人", "静妃",
    "敬贵人", "温仪", "舒太妃", "方淑仪", "孟静娴", "王爷", "王儇", "敬贵妃", 
    "十七爷", "太监", "太后", "年羹尧", "徐进良", "小厦子", "竹息", "官员甲", 
    "官员乙", "官员丙", "官员丁", "端贵妃", "曹琴默", "眉庄", "端敬", "妙音娘子"
]

# 生成共现统计
cooccurrence = pd.DataFrame(0, index=characters, columns=characters)

for scene in scenes:
    # 找出场景中出现的所有人物
    present_characters = [char for char in characters if char in scene]
    
    # 统计共现
    for char1, char2 in itertools.combinations(present_characters, 2):
        cooccurrence.loc[char1, char2] += 1
        cooccurrence.loc[char2, char1] += 1

# 初始化 d3graph
d3 = d3graph()

# 将共现矩阵转为邻接矩阵
adjmat = cooccurrence.values
non_zero_degrees = adjmat.sum(axis=1) > 0
df = pd.DataFrame({
    'label': [label if label in characters else "暂无" for label in cooccurrence.index[non_zero_degrees]],
    'degree': adjmat.sum(axis=1)[non_zero_degrees]
})

# 设置图的布局参数，使节点之间距离增大
d3.graph(adjmat[non_zero_degrees][:, non_zero_degrees])

# 设置节点属性和布局
d3.set_node_properties(label=df['label'].values, color=df['label'].values, cmap='Set1', size=df['degree'].values)

# 增大边的长度，使节点之间的间距更大
d3.set_edge_properties(directed=False, edge_distance=600)  # 600 可调整间距大小

# 显示图表
d3.show(figsize=(1500,1500))
