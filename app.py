import random
import streamlit as st
from data.content import (
    STUDENT, ANTONYMS, GRAMMAR_QA, ESSAYS, POEMS, AAMI_SENTENCES
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="অধিরাজের বাংলা",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans Bengali', sans-serif;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
    padding: 18px 24px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255,107,53,0.3);
}
.main-header h1 {
    color: white;
    font-size: clamp(1.4rem, 4vw, 2.2rem);
    margin: 0;
    text-shadow: 1px 2px 4px rgba(0,0,0,0.2);
}
.main-header p {
    color: rgba(255,255,255,0.92);
    font-size: clamp(0.85rem, 2vw, 1rem);
    margin: 4px 0 0 0;
}

/* Score bar */
.score-bar {
    background: linear-gradient(90deg, #56CCF2, #2F80ED);
    color: white;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(47,128,237,0.3);
}

/* Cards */
.topic-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #FF6B35;
}
.essay-text {
    background: #FFFDF0;
    border-left: 4px solid #FFD700;
    padding: 16px 20px;
    border-radius: 8px;
    font-size: 1.05rem;
    line-height: 1.9;
    margin-bottom: 16px;
}
.poem-line {
    font-size: 1.1rem;
    line-height: 2;
    color: #333;
}
.meaning-box {
    background: #E8F5E9;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 12px;
    border-left: 4px solid #4CAF50;
}

/* Quiz */
.quiz-question {
    font-size: 1.15rem;
    font-weight: 600;
    color: #2D2D2D;
    margin-bottom: 12px;
}
.correct-answer {
    background: #E8F5E9;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 12px 16px;
    color: #2E7D32;
    font-weight: 600;
}
.wrong-answer {
    background: #FFEBEE;
    border: 2px solid #EF5350;
    border-radius: 10px;
    padding: 12px 16px;
    color: #C62828;
    font-weight: 600;
}

/* Celebration */
.celebration {
    text-align: center;
    font-size: 2rem;
    padding: 16px;
    background: linear-gradient(135deg, #FFD700, #FF6B35);
    border-radius: 16px;
    color: white;
    font-weight: 700;
    margin: 12px 0;
    animation: pulse 0.5s ease-in-out;
}

/* Antonym card */
.antonym-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    margin-bottom: 12px;
}

/* Progress */
.progress-text {
    font-size: 0.9rem;
    color: #666;
    text-align: right;
    margin-bottom: 4px;
}

/* Sidebar nav buttons */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border-radius: 10px;
    font-size: 1rem;
    padding: 10px;
    margin-bottom: 4px;
    font-family: 'Noto Sans Bengali', sans-serif;
}

/* Responsive */
@media (max-width: 640px) {
    .antonym-card { font-size: 1.4rem; padding: 16px; }
    .essay-text { font-size: 0.97rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
def _init():
    defaults = {
        "page": "🏠 হোম",
        "stars": 0,
        "streak": 0,
        "antonym_idx": 0,
        "antonym_pool": random.sample(ANTONYMS, len(ANTONYMS)),
        "antonym_score": 0,
        "antonym_total": 0,
        "grammar_idx": 0,
        "grammar_revealed": False,
        "essay_topic": list(ESSAYS.keys())[0],
        "essay_q_idx": 0,
        "essay_revealed": False,
        "poem_title": list(POEMS.keys())[0],
        "poem_q_idx": 0,
        "poem_revealed": False,
        "aami_idx": 0,
        "aami_revealed": False,
        "match_selected": None,
        "match_pairs": [],
        "match_matched": set(),
        "match_wrong": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>📚 অধিরাজের বাংলা 📚</h1>
  <p>তৃতীয় শ্রেণি · সেকশন ডি · রোল ২৯ · সেন্ট জেভিয়ার্স কলেজিয়েট স্কুল</p>
</div>
""", unsafe_allow_html=True)

# ── Score bar ─────────────────────────────────────────────────────────────────
streak_emoji = "🔥" * min(st.session_state.streak, 5) if st.session_state.streak > 0 else ""
st.markdown(f"""
<div class="score-bar">
  ⭐ মোট তারা: {st.session_state.stars} &nbsp;|&nbsp;
  🎯 ধারা: {st.session_state.streak} {streak_emoji}
</div>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
PAGES = [
    "🏠 হোম",
    "👤 আমি",
    "🔤 বিপরীতার্থক শব্দ",
    "🎯 শব্দ মেলাও",
    "📖 ব্যাকরণ",
    "✍️ অনুচ্ছেদ",
    "🎵 কবিতা",
    "🏆 ফলাফল",
]

with st.sidebar:
    st.markdown("### 📋 বিষয় বেছে নাও")
    for p in PAGES:
        if st.button(p, key=f"nav_{p}"):
            st.session_state.page = p
            st.rerun()
    st.markdown("---")
    st.markdown(f"**{STUDENT['name']}**")
    st.markdown(f"শ্রেণি {STUDENT['class']} | সেকশন {STUDENT['section']}")

page = st.session_state.page

# ── Helper ────────────────────────────────────────────────────────────────────
def award(n=1):
    st.session_state.stars += n
    st.session_state.streak += 1

def wrong():
    st.session_state.streak = 0

def celebrate(msg="সাবাশ অধিরাজ! 🎉"):
    st.markdown(f'<div class="celebration">{msg}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 হোম":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="topic-card" style="text-align:center; border-left-color:#FFD700;">
          <div style="font-size:4rem;">🌟</div>
          <h2 style="color:#FF6B35;">নমস্কার অধিরাজ!</h2>
          <p style="font-size:1.1rem;">আজ কী পড়তে চাও?</p>
          <p style="color:#888; font-size:0.9rem;">বাম দিকের মেনু থেকে বিষয় বেছে নাও।</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📌 আজকের বিষয়গুলি")
    cols = st.columns(2)
    topics = [
        ("👤", "আমি", "নিজের পরিচয়"),
        ("🔤", "বিপরীতার্থক শব্দ", "উল্টো শব্দ শেখো"),
        ("📖", "ভাষা ও ব্যাকরণ", "ভাষার নিয়ম"),
        ("✍️", "অনুচ্ছেদ", "বিড়াল, গ্রীষ্মকাল..."),
        ("🎵", "কবিতা", "কোমল ও চেষ্টার ফল"),
        ("🎯", "শব্দ মেলাও", "মিলিয়ে দেখো"),
    ]
    for i, (emoji, title, desc) in enumerate(topics):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="topic-card">
              <span style="font-size:1.8rem;">{emoji}</span>
              <strong style="font-size:1.1rem; margin-left:8px;">{title}</strong>
              <p style="color:#666; margin:4px 0 0 0; font-size:0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# আমি
# ════════════════════════════════════════════════════════════════════════════
elif page == "👤 আমি":
    st.markdown("## 👤 আমি — নিজের পরিচয়")

    tab1, tab2 = st.tabs(["📖 পড়ো", "✏️ অনুশীলন"])

    with tab1:
        st.markdown('<div class="essay-text">', unsafe_allow_html=True)
        for i, (sentence, answer) in enumerate(AAMI_SENTENCES):
            full = sentence.replace("___", f"**{answer}**")
            st.markdown(f"**{i+1})** {full}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        idx = st.session_state.aami_idx
        if idx >= len(AAMI_SENTENCES):
            celebrate("সব প্রশ্ন হয়ে গেছে! দারুণ করেছ! 🌟")
            if st.button("🔄 আবার শুরু করো"):
                st.session_state.aami_idx = 0
                st.session_state.aami_revealed = False
                st.rerun()
        else:
            sentence, answer = AAMI_SENTENCES[idx]
            st.markdown(f'<div class="quiz-question">প্রশ্ন {idx+1}/{len(AAMI_SENTENCES)}: শূন্যস্থান পূরণ করো —<br><br><em>{sentence}</em></div>', unsafe_allow_html=True)
            st.progress((idx) / len(AAMI_SENTENCES))

            if not st.session_state.aami_revealed:
                if st.button("💡 উত্তর দেখো"):
                    st.session_state.aami_revealed = True
                    st.rerun()
            else:
                st.markdown(f'<div class="correct-answer">✅ উত্তর: {answer}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ পারলাম!", key="aami_correct"):
                        award()
                        st.session_state.aami_idx += 1
                        st.session_state.aami_revealed = False
                        st.rerun()
                with c2:
                    if st.button("❌ পারিনি", key="aami_wrong"):
                        wrong()
                        st.session_state.aami_idx += 1
                        st.session_state.aami_revealed = False
                        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# বিপরীতার্থক শব্দ — Flashcard
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔤 বিপরীতার্থক শব্দ":
    st.markdown("## 🔤 বিপরীতার্থক শব্দ")

    tab1, tab2 = st.tabs(["📇 ফ্ল্যাশকার্ড", "📋 সম্পূর্ণ তালিকা"])

    with tab1:
        pool = st.session_state.antonym_pool
        idx = st.session_state.antonym_idx % len(pool)
        word, opposite = pool[idx]

        st.markdown(f'<div class="antonym-card">🔤 {word}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-text">{idx+1} / {len(pool)}</div>', unsafe_allow_html=True)
        st.progress((idx + 1) / len(pool))

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            user_ans = st.text_input("বিপরীত শব্দ লেখো:", key=f"ant_{idx}", label_visibility="collapsed", placeholder="বিপরীত শব্দ লেখো...")
        with col2:
            if st.button("✅ পরীক্ষা করো", key=f"check_{idx}"):
                if user_ans.strip() == opposite:
                    award()
                    st.session_state.antonym_score += 1
                    st.session_state.antonym_total += 1
                    st.markdown(f'<div class="correct-answer">✅ একদম ঠিক! বিপরীত হল — {opposite} 🌟</div>', unsafe_allow_html=True)
                else:
                    wrong()
                    st.session_state.antonym_total += 1
                    st.markdown(f'<div class="wrong-answer">❌ ঠিক উত্তর হল — {opposite}</div>', unsafe_allow_html=True)
        with col3:
            if st.button("⏭️ পরের"):
                st.session_state.antonym_idx += 1
                st.rerun()

        score = st.session_state.antonym_score
        total = st.session_state.antonym_total
        if total > 0:
            st.info(f"এই রাউন্ডে: {score}/{total} সঠিক")

        if st.button("🔀 নতুন করে শুরু"):
            st.session_state.antonym_pool = random.sample(ANTONYMS, len(ANTONYMS))
            st.session_state.antonym_idx = 0
            st.session_state.antonym_score = 0
            st.session_state.antonym_total = 0
            st.rerun()

    with tab2:
        cols = st.columns(3)
        for i, (w, o) in enumerate(sorted(ANTONYMS, key=lambda x: x[0])):
            with cols[i % 3]:
                st.markdown(f"**{w}** → {o}")

# ════════════════════════════════════════════════════════════════════════════
# শব্দ মেলাও — Matching Game
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎯 শব্দ মেলাও":
    st.markdown("## 🎯 শব্দ মেলাও — বিপরীত শব্দ খুঁজে বের করো")

    MATCH_SIZE = 6

    if len(st.session_state.match_pairs) == 0 or st.button("🔀 নতুন খেলা"):
        pairs = random.sample(ANTONYMS, MATCH_SIZE)
        st.session_state.match_pairs = pairs
        st.session_state.match_matched = set()
        st.session_state.match_wrong = set()
        st.session_state.match_selected = None
        st.rerun()

    pairs = st.session_state.match_pairs
    matched = st.session_state.match_matched
    selected = st.session_state.match_selected

    words = [w for w, _ in pairs]
    opposites = [o for _, o in pairs]
    all_items = words + opposites
    if "match_order" not in st.session_state or len(st.session_state.match_order) != len(all_items):
        order = list(range(len(all_items)))
        random.shuffle(order)
        st.session_state.match_order = order

    order = st.session_state.match_order
    display = [all_items[i] for i in order]

    if len(matched) == MATCH_SIZE:
        celebrate(f"দারুণ! সব {MATCH_SIZE}টি জুটি মিলিয়েছ! 🎊")
        award(MATCH_SIZE)
    else:
        st.markdown(f"**মিলেছে: {len(matched)}/{MATCH_SIZE}**")
        cols = st.columns(4)
        for pos, word in enumerate(display):
            orig_idx = order[pos]
            is_word = orig_idx < MATCH_SIZE
            pair_key = orig_idx if is_word else orig_idx - MATCH_SIZE

            already_matched = pair_key in matched
            is_selected = selected == (pos, word, pair_key, is_word)

            col = cols[pos % 4]
            with col:
                if already_matched:
                    st.markdown(f'<div style="background:#C8E6C9;border-radius:10px;padding:12px;text-align:center;margin:4px;font-weight:600;color:#2E7D32;">✅ {word}</div>', unsafe_allow_html=True)
                elif is_selected:
                    st.markdown(f'<div style="background:#FFF9C4;border:2px solid #FF6B35;border-radius:10px;padding:12px;text-align:center;margin:4px;font-weight:700;">{word}</div>', unsafe_allow_html=True)
                    if st.button("✖ বাতিল", key=f"cancel_{pos}"):
                        st.session_state.match_selected = None
                        st.rerun()
                else:
                    if st.button(word, key=f"match_{pos}"):
                        if selected is None:
                            st.session_state.match_selected = (pos, word, pair_key, is_word)
                            st.rerun()
                        else:
                            s_pos, s_word, s_key, s_is_word = selected
                            # valid pair: one from words, one from opposites, same pair_key
                            if s_key == pair_key and s_is_word != is_word:
                                st.session_state.match_matched.add(pair_key)
                                award()
                                st.session_state.match_selected = None
                                st.success(f"✅ সঠিক! {s_word} ↔ {word}")
                            else:
                                wrong()
                                st.session_state.match_selected = None
                                st.error(f"❌ ভুল! আবার চেষ্টা করো।")
                            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ব্যাকরণ
# ════════════════════════════════════════════════════════════════════════════
elif page == "📖 ব্যাকরণ":
    st.markdown("## 📖 ভাষা ও ব্যাকরণ")

    tab1, tab2 = st.tabs(["📖 পড়ো ও শেখো", "✏️ প্রশ্নোত্তর অনুশীলন"])

    with tab1:
        for i, item in enumerate(GRAMMAR_QA):
            with st.expander(f"**প্রশ্ন {i+1}:** {item['q']}"):
                st.markdown(f'<div class="correct-answer">উত্তর: {item["a"]}</div>', unsafe_allow_html=True)

    with tab2:
        idx = st.session_state.grammar_idx
        if idx >= len(GRAMMAR_QA):
            celebrate("সব ব্যাকরণ প্রশ্ন শেষ! তুমি দারুণ! 🏆")
            if st.button("🔄 আবার করো"):
                st.session_state.grammar_idx = 0
                st.session_state.grammar_revealed = False
                st.rerun()
        else:
            item = GRAMMAR_QA[idx]
            st.progress(idx / len(GRAMMAR_QA))
            st.markdown(f'<div class="quiz-question">প্রশ্ন {idx+1}/{len(GRAMMAR_QA)}: {item["q"]}</div>', unsafe_allow_html=True)
            st.caption(f"💡 ইঙ্গিত: {item['hint']}")

            if not st.session_state.grammar_revealed:
                if st.button("উত্তর দেখো 👁"):
                    st.session_state.grammar_revealed = True
                    st.rerun()
            else:
                st.markdown(f'<div class="correct-answer">✅ {item["a"]}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ জানতাম!", key="gram_ok"):
                        award()
                        st.session_state.grammar_idx += 1
                        st.session_state.grammar_revealed = False
                        st.rerun()
                with c2:
                    if st.button("❌ জানতাম না", key="gram_no"):
                        wrong()
                        st.session_state.grammar_idx += 1
                        st.session_state.grammar_revealed = False
                        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# অনুচ্ছেদ
# ════════════════════════════════════════════════════════════════════════════
elif page == "✍️ অনুচ্ছেদ":
    st.markdown("## ✍️ অনুচ্ছেদ পড়ো ও প্রশ্নের উত্তর দাও")

    topic = st.selectbox(
        "অনুচ্ছেদ বেছে নাও:",
        list(ESSAYS.keys()),
        format_func=lambda x: f"{ESSAYS[x]['emoji']} {x}",
    )
    if topic != st.session_state.essay_topic:
        st.session_state.essay_topic = topic
        st.session_state.essay_q_idx = 0
        st.session_state.essay_revealed = False

    essay = ESSAYS[topic]
    tab1, tab2 = st.tabs(["📖 অনুচ্ছেদ পড়ো", "❓ প্রশ্নোত্তর"])

    with tab1:
        st.markdown(f'<div class="essay-text">{essay["text"]}</div>', unsafe_allow_html=True)

    with tab2:
        q_idx = st.session_state.essay_q_idx
        qa = essay["qa"]
        if q_idx >= len(qa):
            celebrate(f"{topic} অনুচ্ছেদ সম্পন্ন! অসাধারণ! 🌟")
            if st.button("🔄 আবার করো"):
                st.session_state.essay_q_idx = 0
                st.session_state.essay_revealed = False
                st.rerun()
        else:
            item = qa[q_idx]
            st.progress(q_idx / len(qa))
            st.markdown(f'<div class="quiz-question">প্রশ্ন {q_idx+1}/{len(qa)}: {item["q"]}</div>', unsafe_allow_html=True)

            if not st.session_state.essay_revealed:
                if st.button("উত্তর দেখো 👁"):
                    st.session_state.essay_revealed = True
                    st.rerun()
            else:
                st.markdown(f'<div class="correct-answer">✅ {item["a"]}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ জানতাম!", key="essay_ok"):
                        award()
                        st.session_state.essay_q_idx += 1
                        st.session_state.essay_revealed = False
                        st.rerun()
                with c2:
                    if st.button("❌ জানতাম না", key="essay_no"):
                        wrong()
                        st.session_state.essay_q_idx += 1
                        st.session_state.essay_revealed = False
                        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# কবিতা
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎵 কবিতা":
    st.markdown("## 🎵 কবিতা পড়ো ও শেখো")

    poem_title = st.selectbox(
        "কবিতা বেছে নাও:",
        list(POEMS.keys()),
        format_func=lambda x: f"{POEMS[x]['emoji']} {x}",
    )
    if poem_title != st.session_state.poem_title:
        st.session_state.poem_title = poem_title
        st.session_state.poem_q_idx = 0
        st.session_state.poem_revealed = False

    poem = POEMS[poem_title]
    tab1, tab2 = st.tabs(["📖 কবিতা পড়ো", "❓ প্রশ্নোত্তর"])

    with tab1:
        st.markdown('<div class="essay-text">', unsafe_allow_html=True)
        for line in poem["lines"]:
            if line:
                st.markdown(f'<div class="poem-line">{line}</div>', unsafe_allow_html=True)
            else:
                st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meaning-box"><strong>🌿 কবিতার মূলভাব:</strong><br>{poem["meaning"]}</div>', unsafe_allow_html=True)

    with tab2:
        q_idx = st.session_state.poem_q_idx
        qa = poem["qa"]
        if q_idx >= len(qa):
            celebrate(f"কবিতার সব প্রশ্ন শেষ! বাহবা! 🎉")
            if st.button("🔄 আবার করো"):
                st.session_state.poem_q_idx = 0
                st.session_state.poem_revealed = False
                st.rerun()
        else:
            item = qa[q_idx]
            st.progress(q_idx / len(qa))
            st.markdown(f'<div class="quiz-question">প্রশ্ন {q_idx+1}/{len(qa)}: {item["q"]}</div>', unsafe_allow_html=True)

            if not st.session_state.poem_revealed:
                if st.button("উত্তর দেখো 👁"):
                    st.session_state.poem_revealed = True
                    st.rerun()
            else:
                st.markdown(f'<div class="correct-answer">✅ {item["a"]}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ জানতাম!", key="poem_ok"):
                        award()
                        st.session_state.poem_q_idx += 1
                        st.session_state.poem_revealed = False
                        st.rerun()
                with c2:
                    if st.button("❌ জানতাম না", key="poem_no"):
                        wrong()
                        st.session_state.poem_q_idx += 1
                        st.session_state.poem_revealed = False
                        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ফলাফল
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏆 ফলাফল":
    st.markdown("## 🏆 আজকের ফলাফল")
    stars = st.session_state.stars

    if stars == 0:
        msg, badge = "এখনো শুরু করোনি। চলো শুরু করি! 💪", "🌱"
    elif stars < 5:
        msg, badge = "ভালো শুরু! আরো চেষ্টা করো। 😊", "🌟"
    elif stars < 15:
        msg, badge = "দারুণ করছ অধিরাজ! 🎉", "⭐⭐⭐"
    elif stars < 30:
        msg, badge = "অসাধারণ! তুমি একটি চ্যাম্পিয়ন! 🏆", "🥇"
    else:
        msg, badge = "তুমি সুপারস্টার অধিরাজ! 🚀", "🌠🌠🌠"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="topic-card" style="text-align:center; border-left-color:#FFD700;">
          <div style="font-size:5rem;">{badge}</div>
          <h2 style="color:#FF6B35;">⭐ {stars} তারা</h2>
          <p style="font-size:1.1rem;">{msg}</p>
          <p style="color:#888;">🔥 সর্বোচ্চ ধারা: {st.session_state.streak}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 নতুন করে শুরু করো"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
