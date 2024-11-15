import os
import re
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_extras.colored_header import colored_header
colored_header(
    label="人物出场次数变化",
    color_name="orange-70",
    description="展现各个人物随时间的出场次数变化~"
)
# 设置页面布局
# st.set_page_config(layout="wide")

# 文件夹路径
folder_path = "./data"  # 替换为实际路径

# 定义角色列表
characters = ["甄嬛", "皇后", "华妃", "沈眉庄", "安陵容", "皇上", "敬妃", "祺贵人", "曹贵人", "颂芝", 
              "夏冬春", "富察贵人", "曹琴默", "端妃", "果郡王", "流朱", "浣碧", "玉娆", "甄远道"]

# 创建数据框来存储每集数的出现次数
character_counts = {character: [] for character in characters}
episode_range = []

# 读取每个文件并统计角色出现次数
for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith(".txt"):
        # 记录集数范围
        episode_range.append(file_name.split("甄嬛传剧本")[-1].replace(".txt", ""))
        
        # 读取文件内容
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
            content = file.read()
        
        # 统计每个角色出现次数
        for character in characters:
            count = len(re.findall(character, content))
            character_counts[character].append(count)

# 将数据转换为 DataFrame
df = pd.DataFrame(character_counts, index=episode_range).reset_index()
df = df.melt(id_vars="index", var_name="Character", value_name="Count")
df.rename(columns={"index": "Episode"}, inplace=True)

# 将 Episode 列转换为字符串类型
df["Episode"] = df["Episode"].astype(str)

# 设置 ECharts 配置项
options = {
    "title": {
        "text": "",
        "left": "center",
        "top": "5%",
        "textStyle": {"fontSize": 24}
    },
    "tooltip": {
        "trigger": "axis"
    },
    "legend": {
        "data": characters,
        "bottom": "0%",
        "left": "center"
    },
    "xAxis": {
        "type": "category",
        "data": list(df["Episode"].unique()),
        "name": "集数",
        "nameLocation": "center",
        "nameGap": 30,
        "axisLabel": {"color":"black","fontWeight":"bold"}
    },
    "yAxis": {
        "type": "value",
        "name": "出场次数",
        "axisLabel": {"color":"black","fontWeight":"bold"}
    },
    "series": []
}

# 为每个角色创建一条曲线
for character in characters:
    character_data = df[df["Character"] == character]["Count"].tolist()
    options["series"].append({
        "name": character,
        "type": "line",
        "smooth": True,
        "data": character_data
    })

# 在 Streamlit 中显示图表
# st.title("甄嬛传人物在不同剧本集数中的出现次数")
st_echarts(options=options, height="800px")

# 在 Streamlit 中显示数据表格（可选，用于检查数据）
# st.write("数据表格：")
# st.dataframe(df)
