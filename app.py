import streamlit as st
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="TaskFlow - To-Do List",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path(__file__).parent / "to_dolist.txt"

# ----------------------------------------------------------------------------
# THEME STATE
# ----------------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

is_dark = st.session_state.theme == "dark"

# Color tokens for each theme
if is_dark:
    C = {
        "text": "#e5e7eb",
        "subtext": "#9ca3af",
        "card_border": "#262b36",
        "app_bg": "#0f1117",
        "input_bg": "#1a1d27",
        "task_pending_bg": "#241f14",
        "task_done_bg": "#12241c",
        "hover_shadow": "rgba(255,255,255,0.05)",
        "empty_text": "#6b7280",
        "button_hover_text": "#ffffff",
    }
else:
    C = {
        "text": "#111827",
        "subtext": "#6b7280",
        "card_border": "#eeeeee",
        "app_bg": "#ffffff",
        "input_bg": "#ffffff",
        "task_pending_bg": "#fffaf0",
        "task_done_bg": "#f0fdf4",
        "hover_shadow": "rgba(0,0,0,0.06)",
        "empty_text": "#9ca3af",
        "button_hover_text": "#111827",
    }

# ----------------------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
    #MainMenu, footer, header {{visibility: hidden;}}

    html, body, [class*="css"] {{
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {C['app_bg']};
        color: {C['text']};
    }}

    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {C['app_bg']};
    }}

    .stMarkdown, .stCaption, p, span, label, .stRadio label {{
        color: {C['text']};
    }}

    .app-header {{
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }}
    .app-header h1 {{
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }}
    .app-header p {{
        color: {C['subtext']};
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }}

    .stats-row {{
        display: flex;
        gap: 12px;
        margin: 1.2rem 0;
    }}
    .stat-box {{
        flex: 1;
        border-radius: 14px;
        padding: 14px 10px;
        text-align: center;
        color: white;
    }}
    .stat-total {{ background: linear-gradient(135deg, #6366f1, #818cf8); }}
    .stat-pending {{ background: linear-gradient(135deg, #f59e0b, #fbbf24); }}
    .stat-done {{ background: linear-gradient(135deg, #10b981, #34d399); }}
    .stat-box .num {{ font-size: 1.6rem; font-weight: 800; line-height: 1; }}
    .stat-box .lbl {{ font-size: 0.75rem; opacity: 0.9; margin-top: 4px; }}

    .task-card {{
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border: 1px solid {C['card_border']};
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: 0.2s;
    }}
    .task-card:hover {{
        box-shadow: 0 4px 14px {C['hover_shadow']};
    }}
    .task-pending {{ background: {C['task_pending_bg']}; border-left: 5px solid #f59e0b; }}
    .task-done {{ background: {C['task_done_bg']}; border-left: 5px solid #10b981; }}

    .task-text {{
        font-size: 1rem;
        font-weight: 500;
        color: {C['text']};
    }}
    .task-done .task-text {{
        text-decoration: line-through;
        color: {C['subtext']};
    }}

    .badge {{
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
    }}
    .badge-pending {{ background: #fef3c7; color: #b45309; }}
    .badge-done {{ background: #d1fae5; color: #047857; }}

    .empty-state {{
        text-align: center;
        padding: 3rem 1rem;
        color: {C['empty_text']};
    }}
    .empty-state .emoji {{ font-size: 3rem; }}

    div.stButton > button {{
        border-radius: 10px;
        font-weight: 600;
    }}

    div.stButton > button *,
    div.stFormSubmitButton > button,
    div.stFormSubmitButton > button * {{
        color: #111827 !important;
    }}

    div.stButton > button:hover,
    div.stButton > button:hover *,
    div.stFormSubmitButton > button:hover,
    div.stFormSubmitButton > button:hover * {{
        color: {C['button_hover_text']} !important;
    }}

    div[data-baseweb="tooltip"],
    div[data-baseweb="tooltip"] * {{
        color: #111827 !important;
    }}

    div[data-testid="stTextInput"] input {{
        background-color: {C['input_bg']};
        color: {C['text']};
    }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# FILE HANDLING (core logic)
# ----------------------------------------------------------------------------
def load_tasks():
    """Read tasks from the txt file into a list of dicts: {name, status}"""
    if not DATA_FILE.exists():
        return []

    tasks = []
    with open(DATA_FILE, "r", encoding="utf-8") as fs:
        for line in fs.readlines():
            line = line.strip()
            if not line:
                continue
            if " - " in line:
                name, status = line.rsplit(" - ", 1)
            else:
                name, status = line, "pending"
            tasks.append({"name": name, "status": status})
    return tasks


def save_tasks(tasks):
    """Write the full task list back to the txt file"""
    with open(DATA_FILE, "w", encoding="utf-8") as fs:
        for t in tasks:
            fs.write(f"{t['name']} - {t['status']}\n")


def add_task(name):
    tasks = load_tasks()
    tasks.append({"name": name, "status": "pending"})
    save_tasks(tasks)


def toggle_task(index, tasks):
    tasks[index]["status"] = "completed" if tasks[index]["status"] == "pending" else "pending"
    save_tasks(tasks)


def delete_task(index, tasks):
    tasks.pop(index)
    save_tasks(tasks)


# ----------------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------------
header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.markdown("""
    <div class="app-header" style="text-align:left; padding-left: 4px;">
        <h1>✅ TaskFlow</h1>
        <p>A simple file-based To-Do list, built with Python + Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    st.markdown("<div style='padding-top: 1.6rem;'></div>", unsafe_allow_html=True)
    st.button(
        "☀️ Light" if is_dark else "🌙 Dark",
        on_click=toggle_theme,
        use_container_width=True,
    )

# --- Add task form ---
with st.form("add_task_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        new_task = st.text_input(
            "Add a task", placeholder="e.g. Finish the React Native bug fix...",
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button("➕ Add", use_container_width=True)

    if submitted:
        if new_task.strip():
            add_task(new_task.strip())
            st.toast("Task added!", icon="✅")
            st.rerun()
        else:
            st.warning("Please enter a task before adding.")

# --- Load current tasks ---
tasks = load_tasks()
total = len(tasks)
done = sum(1 for t in tasks if t["status"] == "completed")
pending = total - done

# --- Stats row ---
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box stat-total"><div class="num">{total}</div><div class="lbl">TOTAL</div></div>
    <div class="stat-box stat-pending"><div class="num">{pending}</div><div class="lbl">PENDING</div></div>
    <div class="stat-box stat-done"><div class="num">{done}</div><div class="lbl">COMPLETED</div></div>
</div>
""", unsafe_allow_html=True)

if total > 0:
    st.progress(done / total, text=f"{done}/{total} tasks completed")

st.markdown("<br>", unsafe_allow_html=True)

# --- Filter ---
filter_choice = st.radio(
    "Filter", ["All", "Pending", "Completed"], horizontal=True, label_visibility="collapsed"
)

if filter_choice == "Pending":
    visible_indices = [i for i, t in enumerate(tasks) if t["status"] == "pending"]
elif filter_choice == "Completed":
    visible_indices = [i for i, t in enumerate(tasks) if t["status"] == "completed"]
else:
    visible_indices = list(range(len(tasks)))

# --- Task list ---
if total == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="emoji">🗒️</div>
        <p>No tasks yet - add your first one above!</p>
    </div>
    """, unsafe_allow_html=True)
elif not visible_indices:
    st.markdown("""
    <div class="empty-state">
        <div class="emoji">🔍</div>
        <p>No tasks match this filter.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for i in visible_indices:
        task = tasks[i]
        is_done = task["status"] == "completed"
        card_class = "task-done" if is_done else "task-pending"
        badge_class = "badge-done" if is_done else "badge-pending"
        badge_text = "COMPLETED" if is_done else "PENDING"

        c1, c2, c3 = st.columns([7, 1, 1])
        with c1:
            st.markdown(f"""
            <div class="task-card {card_class}">
                <span class="task-text">{task['name']}</span>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("↩️" if is_done else "✔️", key=f"toggle_{i}", help="Toggle complete"):
                toggle_task(i, tasks)
                st.rerun()
        with c3:
            if st.button("🗑️", key=f"delete_{i}", help="Delete task"):
                delete_task(i, tasks)
                st.toast("Task deleted", icon="🗑️")
                st.rerun()

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Built with ❤️ using Python & Streamlit - file-based storage, no database needed.")