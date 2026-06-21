from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Richard Personal Hub",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
PAGES_DIR = APP_DIR / "pages"

RICHARD_PAGE = PAGES_DIR / "Richard.py"
FLIGHT_PAGE = PAGES_DIR / "Flight_Log.py"
RICHARD_LEARNING_PAGE = PAGES_DIR / "Richard_Learning.py"

st.markdown(
    """
<style>
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #334155 100%);
        border-radius: 24px;
        padding: 42px 48px;
        color: white;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.22);
        margin-bottom: 28px;
    }
    .hero-title {
        font-size: 42px;
        line-height: 1.15;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 0;
    }
    .section-title {
        font-size: 24px;
        font-weight: 800;
        margin: 22px 0 14px 0;
        color: #111827;
    }
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 28px 26px;
        min-height: 240px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
    }
    .card-icon {
        font-size: 38px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #111827;
    }
    .card-text {
        color: #4b5563;
        font-size: 15px;
        line-height: 1.65;
        margin-bottom: 16px;
    }
    .tag {
        display: inline-block;
        background: #eef2ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 5px 11px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .footer {
        margin-top: 30px;
        color: #6b7280;
        font-size: 13px;
        text-align: center;
    }
</style>
    """,
    unsafe_allow_html=True,
)


def render_card(icon: str, title: str, text: str, tags: list[str]):
    tag_html = "".join([f'<span class="tag">{t}</span>' for t in tags])
    st.markdown(
        f"""
<div class="card">
    <div class="card-icon">{icon}</div>
    <div class="card-title">{title}</div>
    <div class="card-text">{text}</div>
    {tag_html}
</div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
<div class="hero">
    <div class="hero-title">Richard Personal Hub</div>
    <div class="hero-subtitle">投資資產追蹤、個人飛行履歷、學習歷程與未來更多個人資料儀表板的入口網站。</div>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">目前頁面</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    render_card(
        "📈",
        "Richard 的投資儀表板",
        "追蹤 Richard 個人投資資產、台股 / 美股部位、收益變化與長期資產成長狀況。",
        ["Investment", "Portfolio", "Dashboard"],
    )
    if RICHARD_PAGE.exists():
        st.page_link("pages/Richard.py", label="前往投資儀表板", icon="📈")
    else:
        st.warning("找不到 pages/Richard.py，請先把 Richard 的投資儀表板檔案放到 pages 資料夾並命名為 Richard.py。")

with col2:
    render_card(
        "✈️",
        "Flight Log",
        "記錄個人飛行歷程、飛行距離、航線地圖、航空公司、機型與年度飛行統計。",
        ["Travel", "Flight", "Map"],
    )
    if FLIGHT_PAGE.exists():
        st.page_link("pages/Flight_Log.py", label="前往 Flight Log", icon="✈️")
    else:
        st.warning("找不到 pages/Flight_Log.py，請先把 Flight Log 檔案放到 pages 資料夾並命名為 Flight_Log.py。")

with col3:
    render_card(
        "🎓",
        "Richard's Learning Journey",
        "Record Richard's learning timeline, awards, projects, reading log, skill growth, and yearly review.",
        ["Learning", "Awards", "Portfolio"],
    )
    if RICHARD_LEARNING_PAGE.exists():
        st.page_link("pages/Richard_Learning.py", label="Go to Learning Journey", icon="🎓")
    else:
        st.warning("找不到 pages/Richard_Learning.py，請先把 Richard's Learning Journey 檔案放到 pages 資料夾並命名為 Richard_Learning.py。")

st.markdown(
    """
<div class="footer">
    Richard Personal Hub · Built with Streamlit
</div>
    """,
    unsafe_allow_html=True,
)
