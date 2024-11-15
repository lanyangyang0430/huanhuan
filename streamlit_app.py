import streamlit as st
import base64
st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("登录"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("登出"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="登录", icon=":material/login:")
logout_page = st.Page(logout, title="登出", icon=":material/logout:")

dashboard = st.Page(
    "reports/figure_relation.py", title="人物关系图谱", icon=":material/dashboard:", default=True
)
bugs = st.Page("reports/bugs.py", title="人物出场次数", icon=":material/bug_report:")
alerts = st.Page(
    "reports/alerts.py", title="后妃位份变化", icon=":material/notification_important:"
)

search = st.Page("tools/search.py", title="众里寻卿：历史人物关系图谱", icon=":material/search:")
history = st.Page("tools/history_copy.py", title="蓦然回首：他她的一生", icon=":material/history:")
figures = st.Page("reports/figures.py", title="人物小卡", icon=":material/history:")
place_figure = st.Page("reports/place_figure.py", title="人物-地点-气泡图", icon=":material/history:")
if st.session_state.logged_in:
    side_bg_ext = 'png'
    st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] > div:first-child {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open("./images/sidebar1.png", "rb").read()).decode()});
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )
    main_bg_ext = 'png'

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open("./images/background1.png", "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

    pg = st.navigation(
        {
            "账户": [logout_page],
            "人物": [dashboard, bugs, alerts,figures,place_figure],
            "群像": [search, history],
        },
    )
else:
    
    pg = st.navigation([login_page])
pg.run()