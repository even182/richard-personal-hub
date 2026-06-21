# pages/Richard_Learning.py
# Richard's Learning Journey
# Streamlit page for a child's learning portfolio, awards, projects, reading log, skill growth, and yearly reviews.
#
# Suggested project structure:
# .
# ├─ Home.py
# ├─ pages/
# │  └─ Richard_Learning.py
# ├─ data/
# │  └─ learning_portfolio.xlsx
# └─ images/
#    ├─ awards/
#    ├─ projects/
#    ├─ learning/
#    ├─ profile/
#    └─ reviews/

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable, Optional
import html

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Page setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Richard's Learning Journey",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
def get_base_dir() -> Path:
    """Return project root when this file is placed under pages/."""
    current = Path(__file__).resolve()
    if current.parent.name.lower() == "pages":
        return current.parents[1]
    return current.parent


BASE_DIR = get_base_dir()
DATA_PATH = BASE_DIR / "data" / "learning_portfolio.xlsx"

IMAGE_DIRS = {
    "awards": BASE_DIR / "images" / "awards",
    "projects": BASE_DIR / "images" / "projects",
    "learning": BASE_DIR / "images" / "learning",
    "profile": BASE_DIR / "images" / "profile",
    "reviews": BASE_DIR / "images" / "reviews",
}


# -----------------------------------------------------------------------------
# Visual style
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --rlj-bg: #fbf7ef;
        --rlj-card: #ffffff;
        --rlj-text: #2f3437;
        --rlj-muted: #6b7280;
        --rlj-green: #6b8f71;
        --rlj-green-dark: #4f7356;
        --rlj-blue: #8fb3c9;
        --rlj-orange: #e8b86d;
        --rlj-cream: #f2e8cf;
        --rlj-border: #eadfce;
    }

    .stApp {
        background: linear-gradient(180deg, #fbf7ef 0%, #ffffff 42%, #fbf7ef 100%);
        color: var(--rlj-text);
    }

    section[data-testid="stSidebar"] {
        background: #fffaf0;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .rlj-hero {
        border-radius: 28px;
        background: linear-gradient(135deg, #f2e8cf 0%, #dbead7 52%, #dcebf3 100%);
        padding: 34px 34px 28px 34px;
        border: 1px solid rgba(107, 143, 113, 0.22);
        box-shadow: 0 16px 40px rgba(47, 52, 55, 0.08);
        margin-bottom: 22px;
    }

    .rlj-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
        color: #2f3437;
        margin-bottom: 8px;
    }

    .rlj-subtitle {
        font-size: 1.25rem;
        color: #4b5563;
        margin-bottom: 18px;
        line-height: 1.55;
    }

    .rlj-pill {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px 6px 4px 0;
        border-radius: 999px;
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(107, 143, 113, 0.28);
        font-size: 0.92rem;
        color: #36523d;
        font-weight: 600;
    }

    .rlj-section-title {
        font-size: 1.55rem;
        font-weight: 780;
        letter-spacing: -0.02em;
        margin: 24px 0 10px 0;
        color: #2f3437;
    }

    .rlj-section-note {
        color: #6b7280;
        font-size: 0.98rem;
        line-height: 1.55;
        margin-bottom: 12px;
    }

    .rlj-kpi-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid var(--rlj-border);
        border-radius: 20px;
        padding: 20px 18px;
        box-shadow: 0 8px 24px rgba(47, 52, 55, 0.06);
        min-height: 126px;
    }

    .rlj-kpi-value {
        font-size: 2.25rem;
        font-weight: 850;
        color: var(--rlj-green-dark);
        line-height: 1.0;
        margin-bottom: 6px;
    }

    .rlj-kpi-label {
        font-size: 0.95rem;
        color: var(--rlj-muted);
        font-weight: 650;
    }

    .rlj-card {
        background: var(--rlj-card);
        border: 1px solid var(--rlj-border);
        border-radius: 22px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 10px 28px rgba(47, 52, 55, 0.06);
        margin-bottom: 14px;
        min-height: 150px;
    }

    .rlj-card-title {
        font-size: 1.12rem;
        font-weight: 780;
        color: #2f3437;
        margin-bottom: 4px;
        line-height: 1.35;
    }

    .rlj-card-meta {
        color: #6b7280;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 8px;
        line-height: 1.45;
    }

    .rlj-card-body {
        color: #374151;
        font-size: 0.96rem;
        line-height: 1.55;
    }

    .rlj-tag {
        display: inline-block;
        background: #f2e8cf;
        color: #5f4b23;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 5px;
        margin-bottom: 5px;
    }

    .rlj-tag-green {
        background: #dbead7;
        color: #36523d;
    }

    .rlj-tag-blue {
        background: #dcebf3;
        color: #31556d;
    }

    .rlj-timeline-item {
        position: relative;
        padding-left: 20px;
        border-left: 4px solid #dbead7;
        margin-bottom: 16px;
    }

    .rlj-timeline-item::before {
        content: "";
        position: absolute;
        left: -9px;
        top: 6px;
        width: 14px;
        height: 14px;
        background: var(--rlj-green);
        border-radius: 999px;
        border: 3px solid #ffffff;
        box-shadow: 0 0 0 2px #dbead7;
    }

    .rlj-small {
        font-size: 0.86rem;
        color: #6b7280;
    }

    .rlj-privacy-box {
        background: #fffaf0;
        border: 1px solid #eadfce;
        border-radius: 20px;
        padding: 18px;
        color: #374151;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.86);
        border: 1px solid var(--rlj-border);
        border-radius: 18px;
        padding: 14px 16px;
        box-shadow: 0 6px 18px rgba(47,52,55,0.045);
    }

    div[data-testid="stTabs"] button {
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def esc(value: object) -> str:
    return html.escape("" if pd.isna(value) else str(value))


def yes(value: object) -> bool:
    return str(value).strip().lower() in {"yes", "y", "true", "1", "featured"}


def safe_int(value: object, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.columns:
        if col.lower() in {"date", "lastupdated"}:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif col.lower() == "year":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        else:
            df[col] = df[col].fillna("")
    return df


def format_date(value: object) -> str:
    if pd.isna(value) or value == "":
        return ""
    try:
        return pd.to_datetime(value).strftime("%Y-%m-%d")
    except Exception:
        return str(value)


def get_year_options(*dfs: pd.DataFrame) -> list[str]:
    years: set[int] = set()
    for df in dfs:
        if "Year" in df.columns:
            for item in df["Year"].dropna().tolist():
                try:
                    years.add(int(item))
                except Exception:
                    pass
        elif "Date" in df.columns:
            dates = pd.to_datetime(df["Date"], errors="coerce").dropna()
            years.update(dates.dt.year.astype(int).tolist())

    return ["All"] + [str(y) for y in sorted(years, reverse=True)]


def filter_by_year(df: pd.DataFrame, selected_year: str) -> pd.DataFrame:
    if selected_year == "All" or df.empty:
        return df

    target = int(selected_year)
    if "Year" in df.columns:
        return df[df["Year"].astype("Int64") == target]
    if "Date" in df.columns:
        dates = pd.to_datetime(df["Date"], errors="coerce")
        return df[dates.dt.year == target]
    return df


def category_options(df: pd.DataFrame, column: str = "Category") -> list[str]:
    if df.empty or column not in df.columns:
        return ["All"]
    values = sorted([str(v) for v in df[column].dropna().unique() if str(v).strip()])
    return ["All"] + values


def filter_by_category(df: pd.DataFrame, selected_category: str, column: str = "Category") -> pd.DataFrame:
    if selected_category == "All" or df.empty or column not in df.columns:
        return df
    return df[df[column].astype(str) == selected_category]


def resolve_image(filename: object, search_groups: Iterable[str]) -> Optional[Path]:
    name = str(filename).strip()
    if not name:
        return None

    raw_path = Path(name)
    if raw_path.is_absolute() and raw_path.exists():
        return raw_path

    candidates: list[Path] = []
    candidates.append(BASE_DIR / name)
    for group in search_groups:
        img_dir = IMAGE_DIRS.get(group)
        if img_dir:
            candidates.append(img_dir / name)

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


@st.cache_data(show_spinner=False)
def load_workbook(path: str) -> dict[str, pd.DataFrame]:
    file_path = Path(path)
    if not file_path.exists():
        return {}

    sheets = {
        "Profile": ["Field", "Value"],
        "LearningTimeline": ["Date", "Year", "Category", "Title", "Description", "Reflection", "Image", "Link", "Featured", "Privacy"],
        "Awards": ["Date", "Year", "Category", "AwardName", "AwardLevel", "Organizer", "Description", "Image", "Link", "Featured"],
        "Projects": ["Date", "Year", "Category", "ProjectName", "Description", "Tools", "Image", "VideoLink", "Link", "Featured"],
        "ReadingLog": ["Date", "Year", "BookTitle", "Author", "Category", "Reflection", "Rating", "Image", "Link"],
        "SkillGrowth": ["Year", "English", "Math", "Reading", "Expression", "SelfLearning", "Creativity", "Notes"],
        "YearlyReview": ["Year", "MostImportantProgress", "FavoriteProject", "ImportantAwards", "NextYearGoals", "Summary", "CoverImage"],
    }

    loaded: dict[str, pd.DataFrame] = {}
    for sheet_name, columns in sheets.items():
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            loaded[sheet_name] = clean_df(df)
        except Exception:
            loaded[sheet_name] = pd.DataFrame(columns=columns)
    return loaded


def get_profile_value(profile_df: pd.DataFrame, field: str, default: str = "") -> str:
    if profile_df.empty or not {"Field", "Value"}.issubset(profile_df.columns):
        return default

    matched = profile_df[profile_df["Field"].astype(str).str.strip().str.lower() == field.lower()]
    if matched.empty:
        return default

    value = matched.iloc[0]["Value"]
    if pd.isna(value):
        return default
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    return str(value)


def render_kpi(value: object, label: str) -> None:
    st.markdown(
        f"""
        <div class="rlj-kpi-card">
            <div class="rlj-kpi-value">{esc(value)}</div>
            <div class="rlj-kpi-label">{esc(label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_basic_card(
    title: object,
    meta: object = "",
    body: object = "",
    tags: Optional[list[str]] = None,
    link: object = "",
) -> None:
    tag_html = ""
    if tags:
        tag_html = "".join([f'<span class="rlj-tag">{esc(tag)}</span>' for tag in tags if str(tag).strip()])

    link_html = ""
    if str(link).strip():
        link_html = f'<div style="margin-top:10px;"><a href="{esc(link)}" target="_blank">Open link</a></div>'

    st.markdown(
        f"""
        <div class="rlj-card">
            {tag_html}
            <div class="rlj-card-title">{esc(title)}</div>
            <div class="rlj-card-meta">{esc(meta)}</div>
            <div class="rlj-card-body">{esc(body)}</div>
            {link_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_image_card(
    row: pd.Series,
    title_col: str,
    body_col: str,
    image_groups: Iterable[str],
    meta_parts: list[str],
    tag_parts: Optional[list[str]] = None,
    link_col: str = "Link",
    image_col: str = "Image",
) -> None:
    title = row.get(title_col, "")
    body = row.get(body_col, "")
    link = row.get(link_col, "")
    meta = " · ".join([str(part) for part in meta_parts if str(part).strip()])
    tags = [str(row.get(part, "")) for part in (tag_parts or []) if str(row.get(part, "")).strip()]
    image_path = resolve_image(row.get(image_col, ""), image_groups)

    if image_path:
        col_img, col_text = st.columns([0.9, 2.1], gap="medium")
        with col_img:
            st.image(str(image_path), use_container_width=True)
        with col_text:
            render_basic_card(title, meta, body, tags, link)
    else:
        render_basic_card(title, meta, body, tags, link)


def sort_newest(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    result = df.copy()
    if "Date" in result.columns:
        result["_sort_date"] = pd.to_datetime(result["Date"], errors="coerce")
        result = result.sort_values("_sort_date", ascending=False).drop(columns=["_sort_date"])
    elif "Year" in result.columns:
        result = result.sort_values("Year", ascending=False)
    return result


def featured(df: pd.DataFrame, limit: int = 3) -> pd.DataFrame:
    if df.empty or "Featured" not in df.columns:
        return sort_newest(df).head(limit)
    picked = df[df["Featured"].apply(yes)]
    if picked.empty:
        picked = df
    return sort_newest(picked).head(limit)


def show_missing_setup() -> None:
    st.title("Richard's Learning Journey")
    st.warning("The Excel data file was not found.")
    st.markdown(
        f"""
        Please create this file first:

        ```text
        {DATA_PATH}
        ```

        Suggested folders:

        ```text
        images/awards/
        images/projects/
        images/learning/
        images/profile/
        images/reviews/
        ```

        This page expects the workbook to include these sheets:

        ```text
        Profile
        LearningTimeline
        Awards
        Projects
        ReadingLog
        SkillGrowth
        YearlyReview
        ```
        """
    )


# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data = load_workbook(str(DATA_PATH))
if not data:
    show_missing_setup()
    st.stop()

profile = data["Profile"]
learning = data["LearningTimeline"]
awards = data["Awards"]
projects = data["Projects"]
reading = data["ReadingLog"]
skills = data["SkillGrowth"]
reviews = data["YearlyReview"]


display_name = get_profile_value(profile, "DisplayName", "Richard")
site_title = get_profile_value(profile, "Title", "Richard's Learning Journey")
tagline = get_profile_value(profile, "Tagline", "Learning, Projects, and Awards")
intro = get_profile_value(profile, "Intro", "A warm portfolio that records learning, works, awards, reading, and yearly growth.")
current_grade = get_profile_value(profile, "CurrentGrade", "")
interests = get_profile_value(profile, "Interests", "")
hero_image = get_profile_value(profile, "HeroImage", "")
privacy_note = get_profile_value(profile, "PrivacyNote", "Use nickname only and avoid sensitive personal information.")
last_updated = get_profile_value(profile, "LastUpdated", "")


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
hero_col_text, hero_col_image = st.columns([2.2, 0.8], gap="large")

with hero_col_text:
    interest_pills = "".join(
        f'<span class="rlj-pill">{esc(item.strip())}</span>'
        for item in interests.split(",")
        if item.strip()
    )
    st.markdown(
        f"""
        <div class="rlj-hero">
            <div class="rlj-title">{esc(site_title)}</div>
            <div class="rlj-subtitle">{esc(intro)}</div>
            <div>
                <span class="rlj-pill">🌱 {esc(tagline)}</span>
                {f'<span class="rlj-pill">🎒 {esc(current_grade)}</span>' if current_grade else ''}
                {interest_pills}
            </div>
            <div class="rlj-small" style="margin-top:14px;">
                Last updated: {esc(last_updated or date.today().strftime("%Y-%m-%d"))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_col_image:
    image_path = resolve_image(hero_image, ["profile", "projects", "learning"])
    if image_path:
        st.image(str(image_path), use_container_width=True)
    else:
        st.markdown(
            """
            <div class="rlj-kpi-card" style="text-align:center; min-height:240px; display:flex; flex-direction:column; justify-content:center;">
                <div style="font-size:4rem;">🌱</div>
                <div class="rlj-kpi-label">Add a hero image in images/profile/</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# Sidebar filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Portfolio Filters")
    year_filter = st.selectbox("Year", get_year_options(learning, awards, projects, reading, reviews), index=0)
    st.caption("Use the filters inside each tab for category-level views.")
    st.divider()
    st.subheader("Data Source")
    st.write(str(DATA_PATH))
    st.caption("Update the Excel file, then refresh the page.")


# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab_overview, tab_timeline, tab_awards, tab_projects, tab_reading, tab_growth, tab_reviews, tab_setup = st.tabs(
    [
        "Overview",
        "Learning Timeline",
        "Awards",
        "Portfolio",
        "Reading Log",
        "Skill Growth",
        "Yearly Review",
        "Setup & Privacy",
    ]
)


# -----------------------------------------------------------------------------
# Overview
# -----------------------------------------------------------------------------
with tab_overview:
    filtered_learning = filter_by_year(learning, year_filter)
    filtered_awards = filter_by_year(awards, year_filter)
    filtered_projects = filter_by_year(projects, year_filter)
    filtered_reading = filter_by_year(reading, year_filter)

    st.markdown('<div class="rlj-section-title">Growth Snapshot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">A quick view of learning records, awards, projects, and reading progress.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi(len(filtered_learning), "Learning records")
    with c2:
        render_kpi(len(filtered_awards), "Awards")
    with c3:
        render_kpi(len(filtered_projects), "Projects")
    with c4:
        render_kpi(len(filtered_reading), "Books read")

    st.markdown('<div class="rlj-section-title">Featured Projects</div>', unsafe_allow_html=True)
    featured_projects = featured(filtered_projects, limit=3)
    if featured_projects.empty:
        st.info("No project records yet.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(featured_projects.iterrows()):
            with cols[idx % 3]:
                image_path = resolve_image(row.get("Image", ""), ["projects"])
                if image_path:
                    st.image(str(image_path), use_container_width=True)
                render_basic_card(
                    title=row.get("ProjectName", ""),
                    meta=" · ".join(
                        [
                            format_date(row.get("Date", "")),
                            str(row.get("Category", "")),
                            str(row.get("Tools", "")),
                        ]
                    ),
                    body=row.get("Description", ""),
                    tags=[str(row.get("Category", ""))],
                    link=row.get("Link", "") or row.get("VideoLink", ""),
                )

    st.markdown('<div class="rlj-section-title">Featured Awards</div>', unsafe_allow_html=True)
    featured_awards = featured(filtered_awards, limit=3)
    if featured_awards.empty:
        st.info("No award records yet.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(featured_awards.iterrows()):
            with cols[idx % 3]:
                image_path = resolve_image(row.get("Image", ""), ["awards"])
                if image_path:
                    st.image(str(image_path), use_container_width=True)
                render_basic_card(
                    title=row.get("AwardName", ""),
                    meta=" · ".join(
                        [
                            format_date(row.get("Date", "")),
                            str(row.get("AwardLevel", "")),
                            str(row.get("Organizer", "")),
                        ]
                    ),
                    body=row.get("Description", ""),
                    tags=[str(row.get("Category", ""))],
                    link=row.get("Link", ""),
                )

    st.markdown('<div class="rlj-section-title">Latest Learning Updates</div>', unsafe_allow_html=True)
    latest_updates = sort_newest(filtered_learning).head(5)
    if latest_updates.empty:
        st.info("No learning records yet.")
    else:
        for _, row in latest_updates.iterrows():
            render_basic_card(
                title=row.get("Title", ""),
                meta=" · ".join([format_date(row.get("Date", "")), str(row.get("Category", ""))]),
                body=row.get("Description", ""),
                tags=[str(row.get("Category", "")), str(row.get("Privacy", ""))],
                link=row.get("Link", ""),
            )


# -----------------------------------------------------------------------------
# Learning Timeline
# -----------------------------------------------------------------------------
with tab_timeline:
    st.markdown('<div class="rlj-section-title">Learning Timeline</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">A chronological story of learning moments, activities, reflections, and milestones.</div>',
        unsafe_allow_html=True,
    )

    category = st.selectbox("Learning category", category_options(learning), key="learning_category")
    filtered = filter_by_category(filter_by_year(learning, year_filter), category)

    if filtered.empty:
        st.info("No learning records match the selected filters.")
    else:
        for _, row in sort_newest(filtered).iterrows():
            st.markdown('<div class="rlj-timeline-item">', unsafe_allow_html=True)
            render_image_card(
                row=row,
                title_col="Title",
                body_col="Description",
                image_groups=["learning", "projects"],
                meta_parts=[format_date(row.get("Date", "")), row.get("Category", ""), row.get("Privacy", "")],
                tag_parts=["Category", "Privacy"],
                link_col="Link",
            )
            if str(row.get("Reflection", "")).strip():
                st.markdown(
                    f"""
                    <div class="rlj-card" style="background:#fffaf0;">
                        <div class="rlj-card-meta">Reflection</div>
                        <div class="rlj-card-body">{esc(row.get("Reflection", ""))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Awards
# -----------------------------------------------------------------------------
with tab_awards:
    st.markdown('<div class="rlj-section-title">Awards & Recognition</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">Awards are recorded with context, so the page shows effort and growth, not only certificates.</div>',
        unsafe_allow_html=True,
    )

    category = st.selectbox("Award category", category_options(awards), key="award_category")
    filtered = filter_by_category(filter_by_year(awards, year_filter), category)

    if filtered.empty:
        st.info("No award records match the selected filters.")
    else:
        for _, row in sort_newest(filtered).iterrows():
            render_image_card(
                row=row,
                title_col="AwardName",
                body_col="Description",
                image_groups=["awards"],
                meta_parts=[format_date(row.get("Date", "")), row.get("AwardLevel", ""), row.get("Organizer", "")],
                tag_parts=["Category", "AwardLevel"],
                link_col="Link",
            )


# -----------------------------------------------------------------------------
# Portfolio / Projects
# -----------------------------------------------------------------------------
with tab_projects:
    st.markdown('<div class="rlj-section-title">Project Portfolio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">A gallery of works, creative projects, science projects, coding projects, presentations, and performances.</div>',
        unsafe_allow_html=True,
    )

    category = st.selectbox("Project category", category_options(projects), key="project_category")
    filtered = filter_by_category(filter_by_year(projects, year_filter), category)

    if filtered.empty:
        st.info("No project records match the selected filters.")
    else:
        for _, row in sort_newest(filtered).iterrows():
            link_value = row.get("Link", "") or row.get("VideoLink", "")
            render_image_card(
                row=row,
                title_col="ProjectName",
                body_col="Description",
                image_groups=["projects"],
                meta_parts=[format_date(row.get("Date", "")), row.get("Category", ""), row.get("Tools", "")],
                tag_parts=["Category", "Tools"],
                link_col="Link",
            )
            if str(row.get("VideoLink", "")).strip():
                st.markdown(f"[Open video link]({row.get('VideoLink')})")


# -----------------------------------------------------------------------------
# Reading Log
# -----------------------------------------------------------------------------
with tab_reading:
    st.markdown('<div class="rlj-section-title">Reading Log</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">Reading records include book title, category, reflection, and rating.</div>',
        unsafe_allow_html=True,
    )

    category = st.selectbox("Reading category", category_options(reading), key="reading_category")
    filtered = filter_by_category(filter_by_year(reading, year_filter), category)

    if filtered.empty:
        st.info("No reading records match the selected filters.")
    else:
        chart_df = filtered.copy()
        if "Date" in chart_df.columns:
            chart_df["Month"] = pd.to_datetime(chart_df["Date"], errors="coerce").dt.to_period("M").astype(str)
            monthly = chart_df.groupby("Month", dropna=True).size().reset_index(name="Books")
            if not monthly.empty:
                st.markdown("#### Monthly reading count")
                st.bar_chart(monthly.set_index("Month"))

        for _, row in sort_newest(filtered).iterrows():
            stars = "⭐" * max(0, min(5, safe_int(row.get("Rating", 0))))
            image_path = resolve_image(row.get("Image", ""), ["learning", "projects"])
            if image_path:
                col_img, col_text = st.columns([0.8, 2.2], gap="medium")
                with col_img:
                    st.image(str(image_path), use_container_width=True)
                with col_text:
                    render_basic_card(
                        title=row.get("BookTitle", ""),
                        meta=" · ".join([format_date(row.get("Date", "")), row.get("Author", ""), stars]),
                        body=row.get("Reflection", ""),
                        tags=[str(row.get("Category", ""))],
                        link=row.get("Link", ""),
                    )
            else:
                render_basic_card(
                    title=row.get("BookTitle", ""),
                    meta=" · ".join([format_date(row.get("Date", "")), row.get("Author", ""), stars]),
                    body=row.get("Reflection", ""),
                    tags=[str(row.get("Category", ""))],
                    link=row.get("Link", ""),
                )


# -----------------------------------------------------------------------------
# Skill Growth
# -----------------------------------------------------------------------------
with tab_growth:
    st.markdown('<div class="rlj-section-title">Skill Growth</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">A simple year-by-year view of growth areas. Scores are subjective and should be used as a family reflection tool.</div>',
        unsafe_allow_html=True,
    )

    if skills.empty:
        st.info("No skill growth records yet.")
    else:
        skills_display = skills.copy()
        numeric_cols = ["English", "Math", "Reading", "Expression", "SelfLearning", "Creativity"]
        for col in numeric_cols:
            if col in skills_display.columns:
                skills_display[col] = pd.to_numeric(skills_display[col], errors="coerce")

        if "Year" in skills_display.columns:
            chart_data = skills_display.set_index("Year")[[c for c in numeric_cols if c in skills_display.columns]]
            st.line_chart(chart_data)
            st.dataframe(
                skills_display[["Year"] + [c for c in numeric_cols if c in skills_display.columns] + ["Notes"]],
                use_container_width=True,
                hide_index=True,
            )

        latest = sort_newest(skills).head(1)
        if not latest.empty:
            row = latest.iloc[0]
            st.markdown("#### Latest reflection")
            render_basic_card(
                title=f"Growth review - {row.get('Year', '')}",
                meta="English · Math · Reading · Expression · Self-learning · Creativity",
                body=row.get("Notes", ""),
                tags=["Growth", "Reflection"],
            )


# -----------------------------------------------------------------------------
# Yearly Review
# -----------------------------------------------------------------------------
with tab_reviews:
    st.markdown('<div class="rlj-section-title">Yearly Review</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rlj-section-note">A warm annual summary: progress, favorite work, important awards, and next-year goals.</div>',
        unsafe_allow_html=True,
    )

    filtered = filter_by_year(reviews, year_filter)
    if filtered.empty:
        st.info("No yearly review records match the selected filters.")
    else:
        for _, row in sort_newest(filtered).iterrows():
            image_path = resolve_image(row.get("CoverImage", ""), ["reviews", "projects", "learning"])
            if image_path:
                col_img, col_text = st.columns([0.9, 2.1], gap="medium")
                with col_img:
                    st.image(str(image_path), use_container_width=True)
                with col_text:
                    render_basic_card(
                        title=f"Year {row.get('Year', '')}",
                        meta=row.get("Summary", ""),
                        body=row.get("MostImportantProgress", ""),
                        tags=["Yearly Review"],
                    )
            else:
                render_basic_card(
                    title=f"Year {row.get('Year', '')}",
                    meta=row.get("Summary", ""),
                    body=row.get("MostImportantProgress", ""),
                    tags=["Yearly Review"],
                )

            col1, col2, col3 = st.columns(3)
            with col1:
                render_basic_card("Favorite project", "", row.get("FavoriteProject", ""), ["Project"])
            with col2:
                render_basic_card("Important awards", "", row.get("ImportantAwards", ""), ["Award"])
            with col3:
                render_basic_card("Next-year goals", "", row.get("NextYearGoals", ""), ["Goal"])


# -----------------------------------------------------------------------------
# Setup & Privacy
# -----------------------------------------------------------------------------
with tab_setup:
    st.markdown('<div class="rlj-section-title">Setup & Privacy</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rlj-privacy-box">
            <b>Recommended folder structure</b><br><br>
            <code>data/learning_portfolio.xlsx</code><br>
            <code>images/awards/</code><br>
            <code>images/projects/</code><br>
            <code>images/learning/</code><br>
            <code>images/profile/</code><br>
            <code>images/reviews/</code>
            <br><br>
            <b>Privacy checklist</b><br>
            □ Use nickname or English name only<br>
            □ Avoid full school name, class, address, birthday, and phone number<br>
            □ Blur other children's faces before uploading group photos<br>
            □ Remove location metadata from photos before publishing<br>
            □ Crop certificates if they include personal information<br>
            □ Mark sensitive records as Private in the Excel file
            <br><br>
            <b>Design principle</b><br>
            Keep the page warm, clean, and story-based. The goal is to show learning progress, curiosity, confidence, and effort.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Workbook sheets")
    st.code(
        """Profile
LearningTimeline
Awards
Projects
ReadingLog
SkillGrowth
YearlyReview
Settings
Dashboard""",
        language="text",
    )

    st.markdown("#### Image file rules")
    st.markdown(
        """
        Put only the file name in Excel, not the full path.

        Example:

        ```text
        award_001.jpg
        project_001.jpg
        profile_avatar.png
        ```

        The page will automatically search the matching folder.
        """
    )

    st.markdown("#### Current data path")
    st.code(str(DATA_PATH), language="text")

    with st.expander("Show raw Excel data"):
        st.dataframe(profile, use_container_width=True, hide_index=True)
        st.dataframe(learning, use_container_width=True, hide_index=True)
        st.dataframe(awards, use_container_width=True, hide_index=True)
        st.dataframe(projects, use_container_width=True, hide_index=True)
        st.dataframe(reading, use_container_width=True, hide_index=True)
        st.dataframe(skills, use_container_width=True, hide_index=True)
        st.dataframe(reviews, use_container_width=True, hide_index=True)
