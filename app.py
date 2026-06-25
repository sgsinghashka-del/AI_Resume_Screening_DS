import streamlit as st
import pandas as pd
import hashlib
from PyPDF2 import PdfReader
from docx import Document
import sqlite3
import spacy
from datetime import datetime
import tempfile, os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise ATS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# ENTERPRISE THEME (INPUTS DARKER & CLEAR)
# --------------------------------------------------
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    background-color: #eef3f9;
    color: #0f172a;
    font-family: "Segoe UI", sans-serif;
}

/* ================= LOGIN CARD ================= */
.login-card {
    background: white;
    padding: 2.5rem;
    border-radius: 18px;
    box-shadow: 0 18px 40px rgba(15,23,42,0.12);
    max-width: 420px;
    margin: auto;
}

/* ================= INPUT FIELDS (DARKER) ================= */
input, textarea {
    background-color: #e2e8f0 !important;   /* darker shade */
    border: 2px solid #94a3b8 !important;
    border-radius: 10px !important;
    padding: 12px !important;
    color: #0f172a !important;
    font-size: 0.95rem !important;
}

/* Focus state */
input:focus, textarea:focus {
    background-color: #e2e8f0 !important;
    border-color: #4f6bed !important;
    box-shadow: 0 0 0 4px rgba(79,107,237,0.25) !important;
    outline: none !important;
}

/* ================= SELECTBOX (TARGET ROLE) ================= */
[data-baseweb="select"] > div {
    background-color: #e2e8f0 !important;
    border: 2px solid #94a3b8 !important;
    border-radius: 10px !important;
    min-height: 48px;
}

[data-baseweb="select"] span {
    color: #0f172a !important;
    font-weight: 600;
}

/* ================= BUTTON ================= */
.stButton button {
    width: 100%;
    background: linear-gradient(90deg,#4f6bed,#6b85f5);
    color: white;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.65rem;
    border: none;
}

/* ================= TOP NAV ================= */
.top-nav {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(90deg,#4f6bed,#6b85f5);
    padding: 1rem 1.4rem;
    border-radius: 16px;
    margin-bottom: 1.6rem;
    box-shadow: 0 10px 22px rgba(0,0,0,0.14);
}

.nav-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AUTH
# --------------------------------------------------
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

USERS = {
    "admin@company.com": ("admin123","Admin"),
    "hr@company.com": ("hr123","HR"),
    "recruiter@company.com": ("rec123","Recruiter"),
    "demo@client.com": ("demo","Client")
}
USERS = {k:(hash_pw(v[0]),v[1]) for k,v in USERS.items()}

if "auth" not in st.session_state:
    st.session_state.auth={"ok":False}

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
if not st.session_state.auth["ok"]:

    st.markdown("<br><br>", unsafe_allow_html=True)
    left, center, right = st.columns([1,2,1])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### Enterprise ATS Login")
        st.caption("Secure Talent Screening Platform")

        email = st.text_input("Email address")
        pw = st.text_input("Password", type="password")

        if st.button("Login"):
            if email in USERS and hash_pw(pw)==USERS[email][0]:
                st.session_state.auth={"ok":True,"role":USERS[email][1]}
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

role = st.session_state.auth["role"]

# --------------------------------------------------
# TOP NAVIGATION
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

pages = [
    "Dashboard",
    "Resume Processing",
    "Recruiter Board",
    "Interview Pipeline",
    "Compliance Audit",
    "Export Shortlist",
    "Logout"
]

st.markdown('<div class="top-nav">', unsafe_allow_html=True)
cols = st.columns([2]+[1]*len(pages))
cols[0].markdown('<div class="nav-title">Enterprise ATS Platform</div>',unsafe_allow_html=True)
for i,p in enumerate(pages):
    if cols[i+1].button(p):
        st.session_state.page=p
st.markdown('</div>', unsafe_allow_html=True)

menu = st.session_state.page

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
conn = sqlite3.connect("ats.db", check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, role TEXT, score REAL,
    stage TEXT, interview TEXT,
    skills TEXT, experience INTEGER,
    similarity_flag TEXT,
    path TEXT, uploaded TEXT
)
""")
conn.commit()

def load_df():
    return pd.read_sql("SELECT * FROM candidates", conn)

def insert_candidate(row):
    pd.DataFrame([row]).to_sql("candidates", conn, if_exists="append", index=False)

# --------------------------------------------------
# NLP
# --------------------------------------------------
ROLE_SKILLS = {
    "Backend Engineer":["python","api","database","microservices"],
    "Frontend Engineer":["javascript","react","html","css"],
    "DevOps Engineer":["aws","docker","kubernetes"],
    "Data Scientist":["python","machine learning","sql"],
    "HR Specialist":["recruitment","onboarding"],
    "Sales Executive":["sales","crm"]
}

nlp = spacy.load("en_core_web_sm")
ALL_SKILLS = set(sum(ROLE_SKILLS.values(), []))

def parse_resume(path):
    text=""
    if path.endswith(".pdf"):
        for p in PdfReader(path).pages:
            text+=p.extract_text() or ""
    else:
        for p in Document(path).paragraphs:
            text+=p.text
    doc = nlp(text.lower())
    return {t.text for t in doc if t.text in ALL_SKILLS}

# --------------------------------------------------
# PAGES
# --------------------------------------------------
if menu=="Dashboard":
    df = load_df()
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Applications", len(df))
    c2.metric("Avg Match %", round(df.score.mean(),1) if not df.empty else 0)
    c3.metric("Interviews", sum(df.interview=="Yes") if not df.empty else 0)

if menu=="Resume Processing":
    st.subheader("Resume Upload & Skill Matching")
    name = st.text_input("Candidate Name")
    role_sel = st.selectbox("Target Role", list(ROLE_SKILLS.keys()))
    resume = st.file_uploader("Upload Resume", type=["pdf","docx"])

    if resume and name:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(resume.read())
            path = tmp.name

        skills_found = parse_resume(path)
        required = set(ROLE_SKILLS[role_sel])
        score = round(len(skills_found & required)/len(required)*100,1)

        st.success(f"Match Score: {score}%")
        st.write("Skills Found:", ", ".join(skills_found))

        if st.button("Save Candidate"):
            insert_candidate({
                "name":name,"role":role_sel,"score":score,
                "stage":"Applied","interview":"No",
                "skills":",".join(skills_found),
                "experience":0,"similarity_flag":"Unique",
                "path":path,
                "uploaded":datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Candidate added")

if menu=="Recruiter Board":
    st.dataframe(load_df(), use_container_width=True)

if menu=="Interview Pipeline":
    df = load_df()
    stages = ["Applied","Shortlisted","Interview","Offer"]
    if not df.empty:
        cols = st.columns(len(stages))
        for i,s in enumerate(stages):
            with cols[i]:
                st.markdown(f"### {s}")
                for _,r in df[df.stage==s].iterrows():
                    ns = st.selectbox(r["name"], stages, stages.index(s), key=r["id"])
                    if ns!=s:
                        conn.execute("UPDATE candidates SET stage=? WHERE id=?", (ns,r["id"]))
                        conn.commit()
                        st.rerun()

if menu=="Compliance Audit":
    df = load_df()
    if not df.empty:
        df["bias_risk"] = df.score.apply(lambda x:"Low" if x>=50 else "Review")
        st.dataframe(df[["name","role","score","bias_risk"]])

if menu=="Export Shortlist":
    df = load_df()
    for _,r in df[df.interview=="Yes"].iterrows():
        with open(r["path"],"rb") as f:
            st.download_button(f"Download {r['name']}", f.read(), file_name=r["name"])

if menu=="Logout":
    st.session_state.clear()
    st.rerun()