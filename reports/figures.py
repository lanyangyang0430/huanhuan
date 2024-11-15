import streamlit as st
from streamlit_card import card
from streamlit_extras.colored_header import colored_header
colored_header(
    label="后妃判词:双击卡片查看",
    color_name="yellow-80",
    description="六宫位~"
)
# CSS 样式调整
st.markdown(
    """
    <style>
    .stApp {
        background-image: url(data:image/{side_bg_ext};base64,{base64.b64encode(open("./images/sidebar1.png", "rb").read()).decode()});; /* 替换为背景图 URL */
        background-size: cover;
        background-position: center;
    }
    .stColumn > div {
        padding: 0 !important; /* 移除列的内边距 */
    }
    .stContainer {
        margin: 0 !important; /* 移除卡片的外边距 */
        padding: 0 !important; /* 移除卡片的内边距 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# st.title("人物小卡")
# 人物信息列表，添加详细的简介信息
characters_info = [
    {
        "title": "甄嬛",
        "text": "深宫养成记",
        "detailed_text": "嬛嬛一袅楚宫腰，满腹才情离闺阁。愿得一心人终老，惊鸿归来复又空。",
        "image": "https://n.sinaimg.cn/sinakd10117/269/w640h429/20210823/d264-ffe9e6e111c5240b6561d9418ddbc43b.jpg",
    },
    {
        "title": "宜修",
        "text": "权谋的操控者",
        "detailed_text": "貌似恭谨心难测，因缘际会跃龙门。纵道情深迷人眼，不该错裁百花枝。",
        "image": f"https://ts1.cn.mm.bing.net/th/id/R-C.9a19953b66a65878d94c92fb7ddf8fc6?rik=CcVq%2bQGPM8%2fPtQ&riu=http%3a%2f%2fimage.yjcf360.com%2fu%2fcms%2fwww%2f202103%2f12103551vyt0.jpg&ehk=QWRJGBRLnj%2fiW054V%2bi5Vwth%2bv1ynmly6AbBFGgB%2fm8%3d&risl=&pid=ImgRaw&r=0",
    },
    {
        "title": "年世兰",
        "text": "心机深重",
        "detailed_text": "卿本佳人乐无忧，奈何情字断人肠。旧日浮华一朝尽，笑叹俗世众痴人。自古红颜多薄命，梦里花落知多少？唯一句，多情总为无情恼。",
        "image": f"https://ts1.cn.mm.bing.net/th/id/R-C.3a72a2dc9a8d8dad3e1c17d5e95ac492?rik=0zu0VgpSDjDMyw&riu=http%3a%2f%2fpix1.tvzhe.com%2fstills%2fdrama%2f11%2f372%2fb%2fL70tW7%3dkM%3d.jpg&ehk=39F84BXBw3%2b%2flT6De6H0Hzf1xzmrYL08h3kMep%2bLtEw%3d&risl=&pid=ImgRaw&r=0",
    },
    {
        "title": "安陵容",
        "text": "柔弱而隐忍",
        "detailed_text": "小家碧玉初长成，弱柳扶风惹人怜。一心直愿入九霄，命如纸薄终虚无。",
        "image": "https://pic2.zhimg.com/50/v2-f4a9cae96ccc3519428fde499ce53728_hd.jpg?source=1940ef5c",
    },
    {
        "title": "沈眉庄",
        "text": "温婉大气",
        "detailed_text": "银装素裹一枝梅，迎寒自开具傲骨。君若无情妾便休，从此一心付诗书。怎料树静而风急，人生何处惹尘埃。",
        "image": "https://pic2.zhimg.com/v2-4e29e7c1700f224cd25076247296754e_1440w.jpg?source=172ae18b",
    },
    {
        "title": "瓜尔佳文鸳",
        "text": "聪慧且隐忍",
        "detailed_text": "生是美人貌，行为却乖张。轻狂终招祸，身后太凄凉。",
        "image": f"https://ts1.cn.mm.bing.net/th/id/R-C.4e4e44d25e414d27e0719dc33287a4ef?rik=%2bVHW4%2f44GdwCuA&riu=http%3a%2f%2fn.sinaimg.cn%2fsinakd20220527ac%2f109%2fw1079h1430%2f20220527%2f6b5c-120c5fd5f52aef0eb56788b0821b5940.jpg&ehk=kj2W0DorXRDnAmxi88P5zQz9cHXE8e9qkrVjz9L9T%2fY%3d&risl=&pid=ImgRaw&r=0",
    }
]

# 初始化 session_state，用于存储选中的人物文本状态
if 'character_texts' not in st.session_state:
    st.session_state['character_texts'] = {character["title"]: character["text"] for character in characters_info}

# 点击卡片的回调函数
def update_character_text(title, detailed_text):
    # 更新选中卡片上的文本信息为详细简介
    st.session_state['character_texts'][title] = detailed_text

# 每行显示3个卡片
columns = st.columns(3)
for i, character in enumerate(characters_info):
    col = columns[i % 3]  # 循环排列卡片
    with col:
        # 使用 session_state 中的文本信息动态更新卡片文本
        card(
            title=character["title"],
            text=st.session_state['character_texts'][character["title"]],
            image=character["image"],
            styles={
                "card": {
                    "width": "100%",  # 让卡片占满列宽
                    "height": "400px",
                    "margin": "0px",  # 移除卡片的外边距
                    "padding": "0px",  # 移除卡片的内边距
                }
            },
            on_click=lambda char_title=character["title"], char_detailed_text=character["detailed_text"]: update_character_text(char_title, char_detailed_text)  # 设置点击回调
        )
