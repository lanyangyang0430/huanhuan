import streamlit as st
from streamlit_agraph import Config, Edge, Node, agraph
from streamlit_card import card

# 定义两栏
c1, c2 = st.columns(spec=2)
c1.title('人物关系图谱')
c2.title('人物小卡')

# 定义节点和边
nodes = []
edges = []

# 皇上层级
nodes.append(Node(id="皇上", label="皇上", size=30, symbolType='circle'))

# 甄嬛战队
nodes.append(Node(id="甄嬛", label="甄嬛", size=25, image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png",symbolType='circle', group="甄嬛战队"))
nodes.append(Node(id="沈眉庄", label="沈眉庄", size=20, symbolType='circle', group="甄嬛战队"))
nodes.append(Node(id="安陵容", label="安陵容", size=20, symbolType='circle', group="甄嬛战队"))

# 甄嬛战队关系
edges.append(Edge(source="皇上", target="甄嬛", type="STRAIGHT", label="宠爱"))
edges.append(Edge(source="甄嬛", target="沈眉庄", type="STRAIGHT", label="姐妹"))
edges.append(Edge(source="甄嬛", target="安陵容", type="STRAIGHT", label="友谊"))

# 皇后战队
nodes.append(Node(id="皇后", label="皇后", size=25, symbolType='circle', group="皇后战队"))
nodes.append(Node(id="敬妃", label="敬妃", size=20, symbolType='circle', group="皇后战队"))
nodes.append(Node(id="祺贵人", label="祺贵人", size=20, symbolType='circle', group="皇后战队"))

# 皇后战队关系
edges.append(Edge(source="皇上", target="皇后", type="STRAIGHT", label="尊重"))
edges.append(Edge(source="皇后", target="敬妃", type="STRAIGHT", label="同盟"))
edges.append(Edge(source="皇后", target="祺贵人", type="STRAIGHT", label="利用"))

# 华妃战队
nodes.append(Node(id="华妃", label="华妃", size=25, symbolType='circle', group="华妃战队"))
nodes.append(Node(id="曹贵人", label="曹贵人", size=20, symbolType='circle', group="华妃战队"))
nodes.append(Node(id="颂芝", label="颂芝", size=15, symbolType='circle', group="华妃战队"))

# 华妃战队关系
edges.append(Edge(source="皇上", target="华妃", type="STRAIGHT", label="宠爱"))
edges.append(Edge(source="华妃", target="曹贵人", type="STRAIGHT", label="支持"))
edges.append(Edge(source="华妃", target="颂芝", type="STRAIGHT", label="信任"))

# 配置图表
config = Config(
    width=1000,
    height=800,
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    collapsible=True,
    node={'labelProperty': 'label'},
    link={'labelProperty': 'label', 'renderLabel': True},
    maxZoom=2,
    minZoom=0.5,
    initialZoom=1,
    staticGraphWithDragAndDrop=False,
    staticGraph=False,
    graphviz_layout="dot",
    graphviz_config={"rankdir": "TB"}  # 设置层次结构从上到下排列
)
# 初始化会话状态
if 'show_info' not in st.session_state:
    st.session_state.show_info = False


# 在c1中展示图表
with c1:
    return_value = agraph(nodes=nodes, edges=edges, config=config)
with c2:
    hasClicked = card(
    title="甄嬛",
    text="深宫养成记",
    image="https://n.sinaimg.cn/sinakd10117/269/w640h429/20210823/d264-ffe9e6e111c5240b6561d9418ddbc43b.jpg",
    url="https://github.com/gamcoh/st-card"
    )
    hasClicked1 = card(
    title="甄嬛",
    text="深宫养成记",
    image="https://n.sinaimg.cn/sinakd10117/269/w640h429/20210823/d264-ffe9e6e111c5240b6561d9418ddbc43b.jpg",
    url="https://github.com/gamcoh/st-card"
    )
   