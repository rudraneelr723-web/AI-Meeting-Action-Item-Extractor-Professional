import re
from io import BytesIO
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MINUTES | Meeting Assistant", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&family=DM+Mono:wght@400;500&display=swap');
:root{--cream:#f7f1e7;--cream2:#fffaf1;--paper:#fffdf8;--espresso:#2b1c14;--brown:#593923;--cocoa:#79563b;--sand:#e9dcc9;--line:#e7dac8;--muted:#897b6d;--gold:#b78a52;--sage:#5d755e}
.stApp{background:var(--cream);color:var(--espresso);font-family:'DM Sans',sans-serif}
.block-container{padding:1.15rem 1.7rem 3rem;max-width:1600px}
header[data-testid="stHeader"]{background:transparent}
section[data-testid="stSidebar"]{background:#2b1c14;border-right:1px solid #4b3325}
section[data-testid="stSidebar"] *{color:#f7f0e6}
section[data-testid="stSidebar"] .block-container{padding:1.45rem 1.05rem}
.brand{font-family:'Playfair Display',serif;font-size:23px;letter-spacing:.07em;color:#fff8ed!important;display:flex;align-items:center;gap:10px}
.brandmark{width:33px;height:33px;border:1px solid #b78a52;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#e8c99d!important;font-size:18px}
.brandmeta{font:9px 'DM Mono';letter-spacing:.16em;color:#c3ad94!important;margin:5px 0 31px 44px}
.side-label{font:9px 'DM Mono';letter-spacing:.17em;color:#bba58e!important;margin:22px 0 9px}
.side-active{background:#4a3020;border:1px solid #78563a;border-radius:9px;padding:10px 11px;color:#fff8ed!important;font-size:12px;font-weight:700}
.side-link{padding:10px 11px;color:#d0bda8!important;font-size:12px}
.side-foot{margin-top:48px;border:1px solid #60452f;border-radius:12px;padding:16px 13px;color:#c9b49b!important;font:italic 15px 'Playfair Display';line-height:1.5}
.side-version{font:9px 'DM Mono';color:#bba58e!important;letter-spacing:.12em;margin-top:25px}
.topline{display:flex;justify-content:space-between;align-items:center;margin:3px 0 15px}
.crumb{font:9px 'DM Mono';letter-spacing:.13em;color:#8b7966}
.live{font:9px 'DM Mono';color:#49634b;background:#e6eddf;border:1px solid #d1ddc7;padding:6px 9px;border-radius:20px}
.hero{background:linear-gradient(100deg,#fffaf1 0%,#f8efe1 61%,#ead8bd 100%);border:1px solid #e6d7c1;border-radius:15px;padding:25px 28px 24px;position:relative;overflow:hidden;margin-bottom:15px;min-height:178px}
.hero:after{content:"";position:absolute;width:330px;height:330px;border:1px solid #d9c5a9;border-radius:50%;right:-90px;top:-180px;box-shadow:0 0 0 25px #f1e4d1,0 0 0 26px #d9c5a9,0 0 0 52px #f5eadb,0 0 0 53px #d9c5a9}
.eyebrow{font:9px 'DM Mono';letter-spacing:.19em;color:#967044;margin-bottom:10px}
.herotitle{font:600 31px 'Playfair Display',serif;letter-spacing:-.025em;line-height:1.15;color:#342116;margin:0 0 8px;max-width:670px}
.herosub{font-size:12px;color:#756453;margin:0;max-width:690px;line-height:1.6}
.hero-tag{position:absolute;right:25px;bottom:20px;font:italic 14px 'Playfair Display';color:#715238;z-index:2;transform:rotate(-7deg);text-align:center}
.kpi{background:#fffdf8;border:1px solid #e7dac8;border-radius:11px;padding:13px 15px;min-height:87px;box-shadow:0 3px 12px #3b28140a}
.kpi-top{display:flex;justify-content:space-between;align-items:center;color:#8a7b6b;font:9px 'DM Mono';letter-spacing:.11em}
.kpi-num{font:600 27px 'Playfair Display',serif;color:#342116;margin-top:5px}
.kpi-foot{font-size:10px;color:#938575;margin-top:0}
.sectionhead{display:flex;justify-content:space-between;align-items:end;margin:18px 0 9px}
.sectiontitle{font:600 17px 'Playfair Display',serif;color:#342116}
.sectionsub{font-size:10px;color:#8a7b6b;margin-top:3px}
.card{background:#fffdf8;border:1px solid #e7dac8;border-radius:12px;padding:15px 16px;box-shadow:0 3px 12px #3b28140a}
.cardlabel{font:9px 'DM Mono';letter-spacing:.14em;color:#8d755b;margin-bottom:9px}
.stTextArea textarea{background:#fffaf2!important;border:1px solid #e2d4c1!important;border-radius:9px!important;font:12px 'DM Sans'!important;line-height:1.6!important;color:#342116!important}
.stTextArea textarea:focus{border-color:#a77b4d!important;box-shadow:0 0 0 1px #a77b4d!important}
.stButton>button{border-radius:8px;font-size:11px;font-weight:700;min-height:39px;border:1px solid #d9c6ad;background:#f6eee2;color:#49301f}
.stButton>button[kind="primary"]{background:#593923;border-color:#593923;color:#fff8ed}
.stButton>button[kind="primary"]:hover{background:#3f2819;border-color:#3f2819;color:#fff8ed}
.stDownloadButton>button{border-radius:8px;font-size:10px;font-weight:700;min-height:37px;background:#f6eee2;color:#49301f;border:1px solid #d9c6ad}
div[data-testid="stDataEditor"]{border:1px solid #e7dac8;border-radius:9px;overflow:hidden;background:#fffdf8}
div[data-testid="stFileUploader"]{border:1px dashed #cdb99e;border-radius:9px;background:#fffaf2;padding:8px}
div[data-testid="stTabs"] button{font-size:11px;font-weight:700;color:#72573d}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#593923}
div[data-testid="stAlert"]{border-radius:9px}
hr{border-color:#e7dac8!important}
.smallnote{font-size:9px;color:#968777}
</style>
""", unsafe_allow_html=True)

DEFAULT = """Maya: We need to update the onboarding guide before Friday. Arjun, can you own that?
Arjun: Yes, I'll finish the guide by Thursday afternoon.
Maya: Great. Priya, please check the analytics dashboard and send me the broken events list by October 5.
Priya: I'll take it.
Sam: I can schedule the customer interviews next week.
Maya: Sam, please book them by Monday. Also, we should revisit the pricing page, but nobody owns that yet.
"""

def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
def extract_owner(text):
    for p in [r"\b([A-Z][a-z]+)\s*,?\s*(?:can you|please|could you|will you)\b",r"\b([A-Z][a-z]+)\s+(?:will|should|needs to|must|can)\b",r"\b([A-Z][a-z]+)\s*,\s*(?:please|you)\b"]:
        m=re.search(p,text)
        if m:return m.group(1)
    return ""
def extract_deadline(text):
    patterns=[r"\b(?:by|before|until)\s+((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(?:\s+(?:morning|afternoon|evening))?)\b",r"\b(?:by|before|until)\s+((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?)\b",r"\b(?:by|before|until)\s+(\d{4}-\d{2}-\d{2})\b",r"\b(next week|tomorrow|today|this week|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"]
    for p in patterns:
        m=re.search(p,text,re.I)
        if m:return m.group(1)
    return ""
def is_action(s):
    return bool(re.search(r"\b(please|will|I'll|i'll|can you|could you|need to|needs to|should|must|own|finish|complete|send|update|check|review|schedule|book|create|prepare|deliver|follow up|follow-up)\b",s,re.I))
def clean_task(s):
    s=re.sub(r"^[A-Z][A-Za-z0-9 _-]{0,30}:\s*","",s).strip()
    s=re.sub(r"^(?:please\s+)","",s,flags=re.I)
    s=re.sub(r"^[A-Z][a-z]+\s*,\s*(?:please\s+)?","",s)
    s=re.sub(r"^(?:can you|could you|will you)\s+","",s,flags=re.I)
    return re.sub(r"\s+"," ",s).rstrip(" .")
def extract_items(transcript):
    out=[];seen=set()
    for s in split_sentences(transcript):
        if not is_action(s):continue
        task=clean_task(s)
        if len(task)<5:continue
        owner=extract_owner(s)
        speaker=re.match(r"^([A-Z][A-Za-z0-9 _-]{0,30}):",s)
        if not owner and speaker and re.search(r"\b(I'll|I will|I can|I need to)\b",s,re.I):owner=speaker.group(1).strip()
        due=extract_deadline(s)
        key=(task.lower(),owner.lower())
        if key in seen:continue
        seen.add(key)
        out.append({"Task":task,"Owner":owner,"Deadline":due,"Status":"Not started","Confidence":"High" if owner and due else ("Medium" if owner or due else "Low"),"Source sentence":s})
    return out

with st.sidebar:
    st.markdown('<div class="brand"><span class="brandmark">◈</span> MINUTES</div><div class="brandmeta">AI MEETING ASSISTANT</div>',unsafe_allow_html=True)
    st.markdown('<div class="side-label">WORKSPACE</div><div class="side-active">▦ &nbsp; Dashboard</div><div class="side-link">▤ &nbsp; Process meeting</div><div class="side-link">☑ &nbsp; Action items</div><div class="side-link">▤ &nbsp; Summary</div><div class="side-link">⇩ &nbsp; Export</div>',unsafe_allow_html=True)
    st.markdown('<div class="side-label">PREFERENCES</div><div class="side-link">⚙ &nbsp; Settings</div>',unsafe_allow_html=True)
    st.markdown('<div class="side-foot">“Turn conversations<br>into progress.”</div><div class="side-version">MINUTES v1.0<br>BUILT FOR TEAMS THAT SHIP</div>',unsafe_allow_html=True)

st.markdown('<div class="topline"><div class="crumb">MEETINGS &nbsp; → &nbsp; CLARITY &nbsp; → &nbsp; ACTION</div><div class="live">● &nbsp; LOCAL WORKSPACE</div></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">MEETING INTELLIGENCE &nbsp; / &nbsp; WORKSPACE</div><div class="herotitle">Turn meeting conversations<br>into real progress.</div><p class="herosub">Upload a transcript or paste your meeting notes. Extract action items, identify owners, and keep follow-ups moving.</p><div class="hero-tag">Ideas<br>↓<br>Discussions<br>↓<br>Action results</div></div>',unsafe_allow_html=True)

items=st.session_state.get("items",[])
m1,m2,m3,m4=st.columns(4)
metrics=[("ACTION ITEMS",len(items),"Captured from transcript","☑"),("PEOPLE INVOLVED",len(set(x.get("Owner") for x in items if x.get("Owner"))),"Identified owners","♙"),("KEY DECISIONS",0,"Decision extraction not enabled","▤"),("FOLLOW-UPS",sum(bool(x.get("Deadline")) for x in items),"Items with deadlines","◷")]
for col,(label,num,foot,ico) in zip([m1,m2,m3,m4],metrics):
    with col:st.markdown(f'<div class="kpi"><div class="kpi-top"><span>{label}</span><span>{ico}</span></div><div class="kpi-num">{num:02d}</div><div class="kpi-foot">{foot}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="sectionhead"><div><div class="sectiontitle">Process a meeting</div><div class="sectionsub">Add source material and generate a reviewable action register.</div></div><div class="smallnote">SUPPORTED FORMAT · TXT</div></div>',unsafe_allow_html=True)
left,right=st.columns([1.15,.85],gap="medium")
with left:
    st.markdown('<div class="cardlabel">01 / TRANSCRIPT</div>',unsafe_allow_html=True)
    transcript=st.text_area("Transcript",value=st.session_state.get("transcript",DEFAULT),height=260,label_visibility="collapsed",placeholder="Speaker: Please send the report by Friday...")
    uploaded=st.file_uploader("Upload transcript (.txt)",type=["txt"],label_visibility="collapsed")
    if uploaded is not None:transcript=uploaded.getvalue().decode("utf-8",errors="replace")
    b1,b2=st.columns([1,1])
    with b1:
        if st.button("✦  Extract action items",type="primary",use_container_width=True):
            st.session_state["items"]=extract_items(transcript);st.session_state["transcript"]=transcript;st.rerun()
    with b2:
        if st.button("Reset workspace",use_container_width=True):
            st.session_state.pop("items",None);st.session_state.pop("transcript",None);st.rerun()
with right:
    st.markdown('<div class="cardlabel">02 / MEETING DETAILS (OPTIONAL)</div>',unsafe_allow_html=True)
    meeting_title=st.text_input("Meeting title",placeholder="e.g. Product Planning Meeting")
    meeting_date=st.date_input("Date",value=None)
    team=st.text_input("Team / Project",placeholder="e.g. Core Platform")
    st.markdown('<div style="border:1px solid #e8dac6;background:#f8f0e4;border-radius:9px;padding:11px 12px;margin-top:8px;font-size:10px;color:#76634f;line-height:1.5"><b style="color:#553923">Private by design</b><br>Transcript text is processed locally. No API key or external AI service is required.</div>',unsafe_allow_html=True)

st.markdown('<div class="sectionhead"><div><div class="sectiontitle">Extracted action items</div><div class="sectionsub">Review, update, and export the follow-up list.</div></div><div class="smallnote">EDITABLE REGISTER</div></div>',unsafe_allow_html=True)
if not items:
    st.markdown('<div class="card" style="text-align:center;padding:25px"><div style="font-size:22px;color:#bba58b;margin-bottom:7px">◈</div><div style="font:600 15px Playfair Display;color:#49301f">Your action register is ready</div><div style="font-size:10px;color:#938575;margin-top:5px">Add a transcript above and select “Extract action items”.</div></div>',unsafe_allow_html=True)
else:
    df=pd.DataFrame(items)
    edited=st.data_editor(df,use_container_width=True,hide_index=True,num_rows="dynamic",column_config={
        "Task":st.column_config.TextColumn("Action item",required=True,width="large"),
        "Owner":st.column_config.TextColumn("Owner",width="small"),
        "Deadline":st.column_config.TextColumn("Deadline",width="small"),
        "Status":st.column_config.SelectboxColumn("Status",options=["Not started","In progress","Done","Blocked"],width="medium"),
        "Confidence":st.column_config.SelectboxColumn("Confidence",options=["High","Medium","Low"],width="small"),
        "Source sentence":st.column_config.TextColumn("Source sentence",disabled=True,width="large")})
    st.markdown("<br>",unsafe_allow_html=True)
    x,y,z=st.columns([1,1,3])
    with x:st.download_button("↓  Export CSV",edited.to_csv(index=False).encode("utf-8"),"action_items.csv","text/csv",use_container_width=True)
    with y:
        buf=BytesIO()
        with pd.ExcelWriter(buf,engine="openpyxl") as writer:edited.to_excel(writer,index=False,sheet_name="Action Items")
        st.download_button("↓  Export Excel",buf.getvalue(),"action_items.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
    with z:st.caption("Confidence is a heuristic based on detected ownership and deadline. Review suggestions before sharing.")
