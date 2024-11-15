import streamlit as st
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(page_title="故事河流图", layout="wide")

# 页面标题
st.markdown("<h1 style='text-align: center; font-family: KaiTi; color: #5A3E36;'>故事河流图</h1>", unsafe_allow_html=True)

# 定义时间轴和数据
time_points = ["甄嬛入宫", "初次得宠", "被贬冷宫", "复宠", "登上后位"]
zhen_huan = [3, 8, 1, 7, 10]
emperor = [7, 8, 3, 9, 10]
hua_fei = [8, 4, 0, 2, 1]
an_ling_rong = [5, 7, 5, 3, 0]

# 创建故事河流图
fig = go.Figure()
fig.add_trace(go.Scatter(x=time_points, y=zhen_huan, mode='lines+markers', name='甄嬛', line=dict(shape='spline', width=4)))
fig.add_trace(go.Scatter(x=time_points, y=emperor, mode='lines+markers', name='皇帝', line=dict(shape='spline', width=4)))
fig.add_trace(go.Scatter(x=time_points, y=hua_fei, mode='lines+markers', name='华妃', line=dict(shape='spline', width=4)))
fig.add_trace(go.Scatter(x=time_points, y=an_ling_rong, mode='lines+markers', name='安陵容', line=dict(shape='spline', width=4)))

# 设置布局
fig.update_layout(
    title="《甄嬛传》角色关系故事河流图",
    xaxis_title="时间节点",
    yaxis_title="关系紧密度",
    yaxis=dict(range=[0, 10]),
    hovermode="x unified",
    template="simple_white"
)

# 显示图表
st.plotly_chart(fig, use_container_width=True)
