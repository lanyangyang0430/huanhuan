import streamlit as st

# 设置页面配置
st.set_page_config(page_title="甄嬛传数据可视化平台", layout="wide")

# 背景图片设置（此处使用内嵌CSS方式）
page_bg_img = '''
<style>
body {
    background-image: url("https://example.com/first_page_pic.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# 左侧可收缩菜单栏
with st.sidebar:
    st.markdown("### 甄嬛传导航")
    st.markdown("---")
    if st.button("故事河流图"):
        # 使用查询参数进行页面跳转
        st.experimental_set_query_params(page="story_river")

# 平台标题及艺术字设计
st.markdown("<h1 style='text-align: center; font-family: KaiTi; color: #5A3E36;'>甄嬛传数据可视化平台</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: KaiTi; color: #A68077;'>探索甄嬛传中的人物关系与情节发展</p>", unsafe_allow_html=True)

# 页面内容示例
st.markdown("""
    甄嬛传数据可视化平台致力于通过大数据分析甄嬛传中的角色、情节和用户互动。通过多维度数据呈现，
    帮助用户深入了解角色关系和剧情发展。导航栏可以帮助用户轻松切换不同分析模块。
""")

# 检查查询参数是否指向故事河流图页面
params = st.experimental_get_query_params()
if params.get("page") == ["story_river"]:
    st.write("跳转到故事河流图页面")
    # 导入故事河流图页面的内容
    import story_river
