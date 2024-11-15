import os
import re
import pandas as pd
from streamlit_echarts import st_echarts
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
# Display rank legend
# 设置 Streamlit 页面
colored_header(
    label="人物-地点气泡图",
    color_name="violet-70",
    description="展现人物在各个地点出现的情况~"
)
st.balloons()
# 文件夹路径
folder_path = "./data"  # 替换为实际路径

# 定义角色和地点列表
characters = ["甄嬛", "皇后", "华妃", "陵容", "皇上", "敬妃", "祺贵人", "颂芝", 
              "富察贵人", "眉庄", "果郡王", "流朱", "浣碧", "玉娆", "甄远道", "淳儿", "齐妃","太后"]

locations = ["永寿宫", "坤宁宫", "碎玉轩", "景仁宫", "养心殿", "承乾宫", "长春宫", "储秀宫", "景阳宫", "翊坤宫", "甘露寺", "御花园", "咸福宫","寿康宫"]

# Define a color for each location
location_colors = {
    "永寿宫": "rgba(255, 0, 0, 0.8)",  # Red
    "坤宁宫": "rgba(0, 255, 0, 0.8)",  # Green
    "碎玉轩": "rgba(0, 0, 255, 0.8)",  # Blue
    "景仁宫": "rgba(255, 165, 0, 0.8)",  # Orange
    "养心殿": "rgba(0, 255, 255, 0.8)",  # Cyan
    "承乾宫": "rgba(255, 255, 0, 0.8)",  # Yellow
    "寿康宫": "rgba(128, 0, 128, 0.8)",  # Purple
    "长春宫": "rgba(255, 105, 180, 0.8)",  # Hot Pink
    "储秀宫": "rgba(75, 0, 130, 0.8)",  # Indigo
    "景阳宫": "rgba(255, 20, 147, 0.8)",  # Deep Pink
    "体元殿": "rgba(34, 139, 34, 0.8)",  # Forest Green
    "翊坤宫": "rgba(255, 99, 71, 0.8)",  # Tomato
    "甘露寺": "rgba(72, 61, 139, 0.8)",  # Dark Slate Blue
    "御花园": "rgba(255, 222, 173, 0.8)",  # Navajo White
    "咸福宫": "rgba(135, 206, 235, 0.8)"  # Sky Blue
}

# 创建字典来存储每个角色在每个地点的出现次数
appearance_counts = {character: {location: 0 for location in locations} for character in characters}

# 读取每个文件并统计角色在各个地点的出现次数
for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith(".txt"):
        # 读取文件内容
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
            content = file.read()

        # 统计每个角色在各个地点的出现次数
        for character in characters:
            for location in locations:
                pattern = f"{character}.*?{location}"
                count = len(re.findall(pattern, content))
                appearance_counts[character][location] += count

# 将数据转换为 DataFrame，便于后续处理
data = []
for character, loc_data in appearance_counts.items():
    for location, count in loc_data.items():
        if count > 0:  # 只记录有出现次数的点，避免空白气泡
            data.append({"Character": character, "Location": location, "Count": count})

df = pd.DataFrame(data)

# 准备 ECharts 气泡图数据格式
series_data = [
    {
        "name": row["Character"],
        "value": [characters.index(row["Character"]), locations.index(row["Location"]), row["Count"]],
        "itemStyle": {
            # 使用地点颜色
            "color": location_colors[row["Location"]]
        },
        "symbolSize": min(30, row["Count"] * 10)  # 气泡大小根据出现次数动态变化，最大为 30
    }
    for _, row in df.iterrows()
]

# ECharts 配置
options = {
    "title": {
        "text": "甄嬛传人物在不同地点的出现次数气泡图",
        "left": "center",
        "top": "5%"
    },
    "tooltip": {
        "trigger": "item",
        "formatter": '{c}'
    },
    "xAxis": {
        "type": "category",
        "name": "人物",
        "data": characters,
        "nameLocation": "center",
        "nameGap": 10,
        "axisLabel": {"color": "black", "fontWeight": "bold"}
    },
    "yAxis": {
        "type": "category",
        "name": "地点",
        "data": locations,
        "nameLocation": "center",
        "nameGap": 10,
        "axisLabel": {"color": "black", "fontWeight": "bold"}
    },
    "series": [
        {
            "name": "出现次数",
            "type": "scatter",
            "data": series_data,
        }
    ]
}

# 使用 Streamlit 显示图表
st.title("甄嬛传人物在不同地点的出现次数气泡图")
st_echarts(options=options, height="600px")
