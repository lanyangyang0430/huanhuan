import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
# Display rank legend
# 设置 Streamlit 页面
colored_header(
    label="后妃位份变化",
    color_name="violet-70",
    description="展现后妃的位份更迭过程~"
)

with st.expander("点击查看位份说明",icon="🔥"):
    st.markdown("""
    - **10**: 太后 (Empress Dowager)
    - **9**: 皇后 (Empress)
    - **8**: 皇贵妃 (Imperial Noble Consort)
    - **7**: 贵妃 (Noble Consort)
    - **6**: 妃 (Consort)
    - **5**: 嫔 (Concubine)
    - **4**: 贵人 (Noble Lady)
    - **3**: 常在 (First-Class Female Attendant)
    - **2**: 答应 (Second-Class Female Attendant)
    - **1**: 官女子 (Palace Maid)
    - **0**: 出家 (Left Palace)
    """)

# 数据准备
data = {
    "Character": [
        "甄嬛", "甄嬛", "甄嬛", "甄嬛", "甄嬛", "甄嬛", "甄嬛", "甄嬛",
        "齐月宾", "齐月宾", "齐月宾","齐月宾", "齐月宾", "齐月宾","齐月宾", "齐月宾",
        "冯若昭", "冯若昭", "冯若昭", "冯若昭","冯若昭", "冯若昭", "冯若昭", "冯若昭",
        "郭盈风", "郭盈风", "郭盈风", "郭盈风","郭盈风", "郭盈风", "郭盈风", "郭盈风",
        "贞", "贞",
        "康", "康",
        "年世兰", "年世兰", "年世兰", "年世兰", "年世兰",
        "沈眉庄", "沈眉庄", "沈眉庄", "沈眉庄", "沈眉庄", "沈眉庄",
        "安陵容", "安陵容", "安陵容", "安陵容", "安陵容","安陵容","安陵容",
        "夏冬春",
        "宜修", "宜修", "宜修", "宜修", "宜修", "宜修", "宜修", "宜修"
    ],
    "Title": [
        "莞常在", "莞贵人", "莞嫔", "莞妃", "莫愁（出家）", "熹妃", "熹贵妃", "圣母皇太后",
        "端妃", "端妃","端妃","端妃","端妃","端妃","皇贵妃", "皇贵太妃",
        "敬嫔", "敬嫔","敬嫔","敬妃","敬妃","敬妃", "敬贵妃", "敬贵太妃",
        "欣常在", "欣贵人", "欣贵人","欣贵人","欣贵人","欣贵人","欣嫔", "欣太嫔",
        "贞嫔", "贞太嫔",
        "康常在", "康太嫔",
        "华妃", "华贵妃", "年妃", "华妃", "年答应（卒）",
        "沈贵人", "惠贵人", "沈答应", "惠贵人", "惠嫔", "惠妃（卒）",
        "安答应", "安常在", "安贵人", "安贵人","安贵人","安嫔", "鹂妃（卒）",
        "夏冬春",
        "皇后", "皇后", "皇后", "皇后", "皇后", "皇后", "皇后", "废后（卒）"
    ],
    "Time_Period": [
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8",
        "T1", "T2",
        "T1", "T2",
        "T1", "T2", "T3", "T4", "T5",
        "T1", "T2", "T3", "T4", "T5", "T6",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7",
        "T1",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"
    ],
    "Rank": [
        3, 4, 5, 6, 0, 6, 8, 10,
        6, 8, 8,8,8,8,8,9,
        5, 6, 5, 8, 8, 8, 8, 9,
        3, 4, 4, 4, 4, 4, 5, 5,
        5, 5,
        3, 5,
        7, 8, 6, 7, 2,
        4, 4, 2, 4, 5, 6,
        2, 3, 4, 4, 4, 5, 6,
        0,
        9, 9, 9, 9, 9, 9, 9, 9
    ]
}

# 转换数据为 DataFrame
df = pd.DataFrame(data)



# 颜色映射字典，为每个角色分配颜色
character_colors = {character: f"hsl({i * 20}, 70%, 50%)" for i, character in enumerate(df["Character"].unique())}

# 构建 ECharts timeline 数据
timeline_data = []
time_periods = sorted(df["Time_Period"].unique())

for period in time_periods:
    period_data = df[df["Time_Period"] == period]
    # 按位份排序，使高位份的在上方
    period_data = period_data.sort_values(by="Rank", ascending=False)
    series_data = [{"value": [row["Rank"], row["Character"] + " - " + row["Title"]], "itemStyle": {"color": character_colors[row["Character"]]}} for _, row in period_data.iterrows()]
    y_axis_data = [row["Character"] + " - " + row["Title"] for _, row in period_data.iterrows()]
    
    timeline_data.append({
        "title": {"text": f"时间段：{period}"},
        "yAxis": {"type": "category", "data": y_axis_data},  # 动态设置 yAxis 数据
        "series": [{
            "data": series_data,
            "type": "bar",
            "label": {"show": True, "position": "right"},
        }]
    })

# ECharts 配置项
options = {
    "baseOption": {
        "timeline": {
            "axisType": "category",
            "data": time_periods,
            "autoPlay": True,
            "playInterval": 2000,
            "bottom": "5%"
        },
        "title": {"text": "后妃位份变化动态图", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "value",
            "name": "位份",
            "max": 10,
            "min": 0,
            "inverse": True,  # 反转 x 轴方向，使位份高的在右侧,
            "axisLabel": {"color":"black","fontWeight":"bold"}
        },
        "yAxis": {"type": "category",
                   "axisLabel": {"color":"black","fontWeight":"bold"}
                  },  # 默认 yAxis 类型
        "series": [{
            "type": "bar",
            "encode": {"x": "Rank", "y": "Character_Title"},
            "label": {"show": True, "position": "right"}
        }]
    },
    "options": timeline_data
}

# 显示 ECharts 图表
st_echarts(options=options, height="600px")

# 下雨效果
rain(
    emoji="🍂",
    font_size=54,
    falling_speed=5,
    animation_length="infinite",
)
