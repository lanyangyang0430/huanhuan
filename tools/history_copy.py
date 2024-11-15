import re
import itertools
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import os
import time

# 获取所有剧本文件路径并排序，确保按照顺序排列
script_files = sorted([f for f in os.listdir("data") if f.startswith("甄嬛传剧本") and f.endswith(".txt")])

# 完整的角色列表
characters = [
    "甄嬛", "皇帝", "皇后", "华妃", "敬妃", "沈眉庄", "安陵容", "端妃", "皇太后",
    "温实初", "苏培盛", "曹贵人", "齐妃", "祺贵人", "淳常在", "叶澜依", "富察贵人",
    "欣常在", "槿汐", "剪秋", "玉娆", "小允子", "流朱", "余答应", "欣贵人", "静妃",
    "敬贵人", "温仪", "舒太妃", "方淑仪", "孟静娴", "王爷", "王儇", "敬贵妃", 
    "十七爷", "太监", "太后", "年羹尧", "徐进良", "小厦子", "竹息", "官员甲", 
    "官员乙", "官员丙", "官员丁", "端贵妃", "曹琴默", "眉庄", "端敬", "妙音娘子",
]

# 人物简介字典（可以补充完整）
character_descriptions = {
    "甄嬛": "甄嬛，剧中主角，后宫之中从低位到高位的代表。",
    "皇帝": "雍正皇帝，清朝第五位皇帝，后宫之主。",
    "皇后": "雍正的皇后，掌管后宫，是剧中主要的反派之一。",
    "华妃": "华妃，年羹尧之妹，深受皇帝宠爱，但性格跋扈。",
    "沈眉庄": "甄嬛的好友，温柔端庄，后因权谋陷害而失宠。",
    "安陵容": "甄嬛的另一位朋友，后被利用并对甄嬛怀有敌意。",
    "端妃": "端妃，性格平和，对甄嬛持友好态度。",
    "温实初": "太医院的御医，对甄嬛有情。",
}

# 用户选择一个人物来进行动画展示
selected_character = st.selectbox("选择要查看的角色", characters)

# 创建一个按钮来启动动画播放
if st.button("开始播放人物关系随剧本的变化"):
    # 创建进度条
    progress_bar = st.progress(0)
    
    # 创建一个空的容器用于动态刷新图谱
    graph_placeholder = st.empty()
    
    total_files = len(script_files)
    
    for idx, selected_script in enumerate(script_files):
        # 计算进度条的百分比
        progress = (idx + 1) / total_files
        progress_bar.progress(progress)

        # 读取选定剧本文件内容
        with open(os.path.join("data", selected_script), encoding='utf-8') as f:
            script_text = f.read()

        # 分割成场景，假设每个“第x幕”表示一个新场景
        scenes = re.split(r'第\d+幕', script_text)

        # 生成共现统计
        cooccurrence = pd.DataFrame(0, index=characters, columns=characters)
        for scene in scenes:
            # 找出场景中出现的所有人物
            present_characters = [char for char in characters if char in scene]
            
            # 统计共现
            for char1, char2 in itertools.combinations(present_characters, 2):
                cooccurrence.loc[char1, char2] += 1
                cooccurrence.loc[char2, char1] += 1

        # 创建节点和边的列表
        nodes_dict = {char: Node(id=char, label=char, size=20, title=character_descriptions.get(char, "暂无简介")) for char in characters}
        edges_dict = {}
        for i, char1 in enumerate(characters):
            for j, char2 in enumerate(characters):
                if i < j and cooccurrence.loc[char1, char2] > 0:
                    weight = int(cooccurrence.loc[char1, char2])
                    edges_dict[(char1, char2)] = Edge(source=char1, target=char2, label=str(weight), width=weight)

        # 只显示与选定人物相关的节点和边
        nodes = [nodes_dict[selected_character]]
        edges = []
        for (src, tgt), edge in edges_dict.items():
            if src == selected_character or tgt == selected_character:
                edges.append(edge)
                nodes.append(nodes_dict[src])
                nodes.append(nodes_dict[tgt])
        # 去重
        nodes = list({node.id: node for node in nodes}.values())

        # 使用 AGraph 配置，每次更改配置的一些参数（如 `springLength`）确保唯一性
        config = Config(
            width=750, 
            height=400, 
            directed=False, 
            physics=True, 
            hierarchical=False,
            springLength=300 + idx,    # 增加变化
            springStrength=0.01,       # 弱化弹簧强度，增加浮动感
            gravity=-200,              # 设置负重力值以产生排斥力
            charge=-500,               # 增加节点间排斥力
            animate=True,              # 允许动画效果
            animationSpeed=1           # 适度放慢动画速度
        )

        # 清空图表容器并渲染新的图表
        with graph_placeholder:
            graph_placeholder.empty()  # 清空图表
            agraph(nodes=nodes, edges=edges, config=config)

        # 添加时间延迟以实现动画效果
        time.sleep(0.5)  # 2 秒延迟，可根据需要调整

    st.write("动画播放完成！")
    progress_bar.empty()  # 清除进度条
