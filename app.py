
import base64
import json
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TypeBlitz | Arcade Edition",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

WORDS = """
the quick brown fox jumps over the lazy dog while students learn
coding skills every day practice makes progress and confidence
technology connects people across the world computers process
information quickly and software helps solve real problems
reading carefully improves focus accuracy patience and memory
python is a popular language for building useful applications
small steps repeated daily can produce excellent results
keyboard typing requires rhythm control attention and consistency
learning new concepts takes time but effort creates improvement
""".split()

HARD_WORDS = [
    "value", "result", "index", "count", "while", "return",
    "input", "output", "total", "score", "array", "string",
    "if", "else", "for", "print", "data", "user",
]

DURATIONS = {
    "30 Seconds": 30,
    "1 Minute": 60,
    "2 Minutes": 120,
    "5 Minutes": 300,
    "10 Minutes": 600,
    "20 Minutes": 1200,
    "30 Minutes": 1800,
}
from datetime import date

DAILY_CHALLENGE_KEY = "typeblitz_daily_challenge"
DAILY_CHALLENGE_DATE = date.today().isoformat()

def make_daily_passage():
    today = date.today().isoformat()
    seed = int(today.replace("-", ""))
    rng = random.Random(seed)

    count = 100
    words = [rng.choice(WORDS) for _ in range(count)]

    for i in range(0, count, 8):
        words[i] = words[i].capitalize()

    for i in range(11, count, 12):
        words[i] += rng.choice([".", ",", "!"])

    words[-1] += "."
    return " ".join(words)

def make_passage(level, duration):
    count = max(100, int(duration / 60 * 80))
    words = random.choices(WORDS, k=count)

    if level == "Easy":
        passage = " ".join(words)

    elif level == "Medium":
        result = []
        for i, word in enumerate(words):
            if i % 8 == 0:
                word = word.capitalize()
            if i > 0 and i % 12 == 0:
                result[-1] += random.choice([".", ",", "!"])
            result.append(word)
        result[-1] += "."
        passage = " ".join(result)

    else:
        symbols = [";", "()", "{}", "[]", "==", "!=", "+", "=", ":", "_"]
        result = []

        for i, word in enumerate(words):
            if i % 5 == 0:
                word = random.choice(HARD_WORDS)
            if i % 4 == 0:
                word += random.choice(symbols)
            if i % 7 == 0:
                word += str(random.randint(1, 99))
            result.append(word)

        passage = " ".join(result)

    # Verify actual word count
    assert len(passage.split()) == count
    return passage



if "game_id" not in st.session_state:
    st.session_state.game_id = 0

if "passage" not in st.session_state:
    st.session_state.passage = make_passage("Easy", 30)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b0a14;
    --panel: #151326;
    --purple: #a78bfa;
    --blue: #60a5fa;
    --orange: #fb923c;
    --muted: #a5a1bb;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 0%, #282050 0%, transparent 38%),
        radial-gradient(ellipse at 0% 45%, #1a1631 0%, transparent 38%),
        var(--bg);
    color: #f8f7ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1600px;
    padding: 1.4rem 2.2rem 2rem;
}

[data-testid="stSidebar"] {
    background: #100e1d;
    border-right: 1px solid #302744;
}

[data-testid="stSidebar"] * {
    color: #f1edff;
}

.brand {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 8px 0 20px;
    border-bottom: 1px solid #302744;
    margin-bottom: 22px;
}

.brand-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    font-size: 27px;
    background: linear-gradient(135deg, #8b5cf6, #4f46e5);
    box-shadow: 0 0 28px #8b5cf633;
}

.brand-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: 1px;
}

.brand-name span {
    color: #a78bfa;
}

.brand-sub {
    color: #a5a1bb;
    font-size: 10px;
    letter-spacing: 3px;
    margin-top: 6px;
    font-weight: 700;
}

.eyebrow {
    color: #c4b5fd;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 800;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(42px, 5vw, 70px);
    font-weight: 900;
    line-height: .98;
    letter-spacing: 1px;
    margin: 10px 0;
}

.hero-title span {
    background: linear-gradient(90deg, #c4b5fd, #60a5fa, #fb923c);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-sub {
    color: #b1adc6;
    font-size: 14px;
    line-height: 1.7;
    max-width: 600px;
    margin-bottom: 24px;
}

.game-badge {
    display: inline-block;
    padding: 7px 12px;
    border: 1px solid #54417e;
    border-radius: 7px;
    color: #ddd6fe;
    background: #251b3b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}

.section-label {
    color: #c4b5fd;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 800;
    text-transform: uppercase;
    margin: 12px 0;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #19162b, #11101e);
    border: 1px solid #342b4c;
    border-radius: 17px;
}

div[data-testid="stMetric"] {
    background: #171429;
    border: 1px solid #342b4c;
    border-radius: 14px;
    padding: 16px 18px;
}

div[data-testid="stMetricLabel"] {
    color: #b7b0d0;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

div[data-testid="stMetricValue"] {
    color: #f8f7ff;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px;
    font-weight: 800;
}

.stButton > button {
    border-radius: 10px;
    min-height: 46px;
    font-weight: 800;
    border: 1px solid #6550a0;
    transition: .2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #8b5cf6, #5b5de6);
    color: white;
    border: none;
    box-shadow: 0 5px 22px #7c3aed30;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    transform: translateY(-1px);
}



/* Streamlit/BaseWeb selectboxes: dark field + visible selected value */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #171429 !important;
    background-color: #171429 !important;
    border: 1px solid #a78bfa !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div[class*="singleValue"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div[class*="singleValue"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div[class*="valueContainer"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
    fill: #c4b5fd !important;
    color: #c4b5fd !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background: #171429 !important;
    background-color: #171429 !important;
}

[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="option"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

[role="option"]:hover {
    background: #342653 !important;
}

/* FORCE readable text in Streamlit dropdowns */
div[data-baseweb="select"] > div {
    background-color: #171429 !important;
    border: 1px solid #a78bfa !important;
}

/* Selected option text */
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #c4b5fd !important;
    color: #c4b5fd !important;
}

/* Dropdown menu and its options */
ul[role="listbox"],
li[role="option"],
div[data-baseweb="popover"] {
    background-color: #171429 !important;
    color: #ffffff !important;
}

li[role="option"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

li[role="option"]:hover {
    background-color: #342653 !important;
}



hr {
    border-color: #302744;
}

.footer {
    color: #77718f;
    text-align: center;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 18px 0;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem .8rem;
    }
    .hero-title {
        font-size: 44px;
    }
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">🎮</div>
      <div>
        <div class="brand-name">TYPE<span>BLITZ</span></div>
        <div class="brand-sub">ARCADE EDITION</div>
      </div>
    </div>
    <div class="section-label">⚙ GAME SETUP</div>
    """, unsafe_allow_html=True)

    duration_label = st.selectbox(
        "MATCH LENGTH",
        list(DURATIONS.keys()),
        key="duration_choice",
    )

    st.markdown("### 📅 DAILY CHALLENGE")
    st.caption(f"Today's challenge · {DAILY_CHALLENGE_DATE}")

    if st.button("🎯 Play Daily Challenge", use_container_width=True):
        st.session_state.daily_challenge_active = True
        st.session_state.daily_challenge_passage = make_daily_passage()

    sound_enabled = st.toggle("🔊 Sound Effects", value=True, key="sound_enabled")

    uploaded_wrong_sound = st.file_uploader(
        "🎵 Custom wrong-key sound (MP3/WAV)",
        type=["mp3", "wav"],
        help="This sound plays when you type an incorrect character. Leave empty to use the built-in error beep.",
        key="wrong_sound_upload",
    )

    custom_wrong_sound_data = None
    if uploaded_wrong_sound is not None:
        sound_bytes = uploaded_wrong_sound.getvalue()
        sound_mime = "audio/mpeg" if uploaded_wrong_sound.name.lower().endswith(".mp3") else "audio/wav"
        encoded_sound = base64.b64encode(sound_bytes).decode("ascii")
        custom_wrong_sound_data = f"data:{sound_mime};base64,{encoded_sound}"

    level = st.selectbox(
        "DIFFICULTY",
        ["Easy", "Medium", "Hard"],
        key="level_choice",
    )

    duration = DURATIONS[duration_label]
    sound_enabled_json = json.dumps(sound_enabled)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🎲  NEW CHALLENGE", type="primary", use_container_width=True):
        st.session_state.daily_challenge_active = False
        st.session_state.passage = make_passage(level, duration)
        st.session_state.game_id += 1
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div class="section-label">🏁 YOUR MISSION</div>',
        unsafe_allow_html=True,
    )

    descriptions = {
        "Easy": "Warm up with simple words. Focus on flow and accuracy.",
        "Medium": "Capital letters and punctuation raise the challenge.",
        "Hard": "Symbols and coding-style words test your control.",
    }

    st.markdown(
        f'<div style="color:#b5afca;line-height:1.8;font-size:13px">'
        f'{descriptions[level]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("TYPE FAST. STAY SHARP. BEAT YOUR SCORE.")


daily_active = st.session_state.get("daily_challenge_active", False)

if daily_active:
    passage = st.session_state.get(
        "daily_challenge_passage",
        make_daily_passage(),
    )
    duration = 60
    duration_label = "Daily Challenge · 60 Seconds"
else:
    passage = st.session_state.passage
    duration_label = st.session_state.get(
        "duration_choice",
        list(DURATIONS.keys())[0],
    )
    duration = DURATIONS[duration_label]

st.markdown("""
<div class="eyebrow">THE KEYBOARD ARENA • SEASON 01</div>
<div class="hero-title">READY. SET.<br><span>TYPE!</span></div>
<div class="hero-sub">
Enter the arena, find your rhythm, and chase your personal best.
Every word counts. Every second matters.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">
  <span class="game-badge">⚡ SPEED CHALLENGE</span>
  <span class="game-badge">🎯 ACCURACY COUNTS</span>
  <span class="game-badge">🏆 BEAT YOUR RECORD</span>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("MATCH LENGTH", duration_label)
with m2:
    st.metric("DIFFICULTY", st.session_state.get("level_choice", "Easy"))
with m3:
    st.metric("WORDS IN ARENA", len(passage.split()))
with m4:
    st.metric("ROUND", st.session_state.game_id + 1)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">⌨ THE TYPING ARENA</div>',
            unsafe_allow_html=True)

passage_json = json.dumps(passage)
duration_json = json.dumps(duration)

sound_enabled_json = json.dumps(sound_enabled)
custom_wrong_sound_json = json.dumps(custom_wrong_sound_data)
daily_mode_json = json.dumps(daily_active)
daily_date_json = json.dumps(DAILY_CHALLENGE_DATE)

components.html(
    """
    <div id="arcade" style="
      background:linear-gradient(145deg,#19162b,#100f1d);
      color:#f8f7ff;
      padding:clamp(14px,2vw,28px);
      font-family:Inter,Arial,sans-serif;
      border:1px solid #44345f;
      border-radius:18px;
      box-shadow:0 15px 50px #00000030;
      box-sizing:border-box;
      width:100%;
    ">
      <style>
        #arcade * { box-sizing:border-box; }
        .topline {
          display:flex;justify-content:space-between;align-items:center;
          gap:12px;flex-wrap:wrap;margin-bottom:20px;
        }
        .arena-title {
          font-size:11px;font-weight:800;letter-spacing:2px;
          color:#c4b5fd;
        }
        .live-badge {
          color:#86efac;background:#123326;border:1px solid #225b42;
          border-radius:20px;padding:6px 10px;font-size:10px;
          font-weight:800;letter-spacing:1px;
        }
        .stats {
          display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
          gap:10px;margin-bottom:20px;
        }
        .stat {
          padding:14px 12px;background:#100f20;
          border:1px solid #342b4c;border-radius:12px;min-width:0;
        }
        .stat-label {
          font-size:10px;color:#aaa3c2;letter-spacing:1px;
          font-weight:700;margin-bottom:8px;
        }
        .stat-value {
          font-size:clamp(20px,3vw,30px);font-weight:800;
          color:#f8f7ff;line-height:1.1;overflow-wrap:anywhere;
        }
        #timer { color:#fb923c; }
        .passage {
          background:#100f20;border:1px solid #342b4c;
          border-radius:14px;padding:clamp(16px,2vw,25px);
          min-height:160px;max-height:280px;overflow:auto;
          font-size:clamp(16px,1.7vw,20px);line-height:2;
          overflow-wrap:anywhere;white-space:pre-wrap;
          color:#a9a4be;margin-bottom:14px;
        }
        .passage .done { color:#a78bfa; }
        .passage .current {
          color:#fff;background:#5b3ba5;
          border-radius:3px;box-shadow:0 0 0 2px #5b3ba5;
        }
        .passage .wrong {
          color:#fecaca;background:#7f1d1d;
          border-radius:3px;
        }
        #typing {
          width:100%;height:120px;resize:vertical;
          background:#171429;color:#f8f7ff;
          border:1px solid #50406f;border-radius:12px;
          padding:16px;font:16px/1.7 Inter,Arial,sans-serif;
          outline:none;transition:border-color .2s,box-shadow .2s;
        }
        #typing:focus {
          border-color:#a78bfa;
          box-shadow:0 0 0 3px #a78bfa20;
        }
        #typing:disabled { opacity:.75; }
        .actions {
          display:flex;align-items:center;gap:12px;
          justify-content:space-between;flex-wrap:wrap;margin-top:14px;
        }
        #start {
          background:linear-gradient(100deg,#8b5cf6,#5557e8);
          color:white;border:0;border-radius:10px;
          padding:13px 24px;font-size:14px;font-weight:800;
          cursor:pointer;min-height:46px;
        }
        #start:hover { filter:brightness(1.13); }
        #status {
          color:#aaa3c2;font-size:12px;line-height:1.6;
          flex:1;text-align:right;min-width:150px;
        }
        #result {
          display:none;margin-top:16px;padding:20px;
          background:linear-gradient(110deg,#30204f,#17284b);
          border:1px solid #7960c3;border-radius:14px;
        }
        #result h2 { margin:0 0 8px;font-size:24px;color:#fff; }
        #result p { margin:0;color:#d3c9f3;line-height:1.7; }
        .rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 76px;
  height: 76px;
  margin: 12px 0;
  border-radius: 18px;
  font-size: 38px;
  font-weight: 900;
  color: #fff;
  background: linear-gradient(135deg, #8b5cf6, #fb923c);
  box-shadow: 0 0 28px #8b5cf655;
  animation: rankPop .45s ease-out;
}

.record-message {
  color: #86efac;
  font-weight: 800;
  margin: 8px 0;
  animation: rankPop .45s ease-out;
}

@keyframes rankPop {
  0% { transform: scale(.65); opacity: .3; }
  70% { transform: scale(1.08); opacity: 1; }
  100% { transform: scale(1); }
}
        @media(max-width:560px) {
          .stats { grid-template-columns:repeat(2,minmax(0,1fr)); }
          .actions { align-items:stretch; }
          #start { width:100%; }
          #status { text-align:left; }
        }
      </style>

      <div class="topline">
        <div class="arena-title">ROUND IN PROGRESS / TYPE WITH PRECISION</div>
        <div class="live-badge" id="stateBadge">● READY TO PLAY</div>
      </div>

      <div class="stats">
        <div class="stat">
          <div class="stat-label">⚡ SPEED</div>
          <div class="stat-value" id="wpm">0</div>
          <div style="color:#89829f;font-size:10px;margin-top:5px">WORDS / MIN</div>
        </div>
        <div class="stat">
          <div class="stat-label">🎯 ACCURACY</div>
          <div class="stat-value" id="accuracy">100%</div>
          <div style="color:#89829f;font-size:10px;margin-top:5px">CORRECT INPUT</div>
        </div>
        <div class="stat">
          <div class="stat-label">⏱ TIME LEFT</div>
          <div class="stat-value" id="timer">READY</div>
          <div style="color:#89829f;font-size:10px;margin-top:5px">SECONDS</div>
        </div>
        <div class="stat">
          <div class="stat-label">⌨ CHARACTERS</div>
          <div class="stat-value" id="chars">0</div>
          <div style="color:#89829f;font-size:10px;margin-top:5px">TYPED</div>
        </div>
      </div>

      <div class="arena-title" style="margin:0 0 10px">YOUR PASSAGE</div>
      <div id="passage" class="passage"></div>

      <div class="arena-title" style="margin:0 0 10px">YOUR INPUT</div>
      <textarea id="typing" disabled
        placeholder="Press START MATCH, then type the passage here..."
        spellcheck="false" autocomplete="off" autocapitalize="off"></textarea>

      <div class="actions">
        <button id="start">▶ START MATCH</button>
        <div id="status">Your countdown begins with your first character.</div>
      </div>

      <div id="result">
  <h2 id="resultTitle">🏆 MATCH COMPLETE</h2>
  <div id="rankBadge" class="rank-badge">C</div>
  <div id="recordMessage" class="record-message"></div>
  <p id="resultText"></p>
  <div id="historyBox"></div>
  <div id="badgesBox"></div>
</div>
    </div>

    <script>
    (() => {
      const passage = PASSAGE_PLACEHOLDER;
      const duration = DURATION_PLACEHOLDER;
      const soundEnabled = SOUND_PLACEHOLDER === true;
      const customWrongSound = CUSTOM_WRONG_AUDIO_PLACEHOLDER;
      const dailyChallengeMode = DAILY_MODE_PLACEHOLDER === true;
      const dailyChallengeDate = DAILY_DATE_PLACEHOLDER;
      let audioContext = null;

function playSound(type) {
  if (!soundEnabled) return;

  // If a custom file was uploaded, use it for incorrect characters.
  if (type === "wrong" && customWrongSound) {
    try {
      const audio = new Audio(customWrongSound);
      audio.volume = 0.85;
      audio.play().catch(() => {});
      return;
    } catch (error) {
      // Fall back to the built-in error beep.
    }
  }

  try {
    audioContext = audioContext || new (
      window.AudioContext || window.webkitAudioContext
    )();

    if (audioContext.state === "suspended") {
      audioContext.resume();
    }

    const sounds = {
      key:     { frequency: 720, duration: 0.07, volume: 0.12 },
      wrong:   { frequency: 180, duration: 0.12,  volume: 0.07 },
      start:   { frequency: 660, duration: 0.12,  volume: 0.07 },
      finish:  { frequency: 880, duration: 0.22,  volume: 0.08 },
      record:  { frequency: 1040, duration: 0.30, volume: 0.08 }
    };

    const sound = sounds[type];
    if (!sound) return;

    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();

    oscillator.type = type === "wrong" ? "square" : "sine";
    oscillator.frequency.value = sound.frequency;

    gain.gain.setValueAtTime(sound.volume, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(
      0.001,
      audioContext.currentTime + sound.duration
    );

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    oscillator.start();
    oscillator.stop(audioContext.currentTime + sound.duration);
  } catch (error) {
    // Sound is optional; the typing game continues to work.
  }
}

      const $ = id => document.getElementById(id);
      const timer = $("timer");
      const passageBox = $("passage");
      const typing = $("typing");
      const startButton = $("start");
      const wpmBox = $("wpm");
      const accuracyBox = $("accuracy");
      const charsBox = $("chars");
      const status = $("status");
      const result = $("result");
      const resultTitle = $("resultTitle");
      const resultText = $("resultText");
      const rankBadge = $("rankBadge");
      const recordMessage = $("recordMessage");
      const BEST_KEY = "typeblitz_best_wpm";
      const BADGES_KEY = "typeblitz_unlocked_badges";

const BADGES = [
  {
    id: "first_match",
    name: "First Match",
    icon: "🎮",
    description: "Complete your first typing match"
  },
  {
    id: "speedster",
    name: "Speedster",
    icon: "⚡",
    description: "Reach 30 WPM or higher"
  },
  {
    id: "sharpshooter",
    name: "Sharpshooter",
    icon: "🎯",
    description: "Reach 95% accuracy or higher"
  },
  {
    id: "record_breaker",
    name: "Record Breaker",
    icon: "🏆",
    description: "Set a new personal best WPM"
  }
];

function getUnlockedBadges() {
  try {
    return JSON.parse(localStorage.getItem(BADGES_KEY) || "[]");
  } catch (e) {
    return [];
  }
}

function saveUnlockedBadges(badges) {
  try {
    localStorage.setItem(BADGES_KEY, JSON.stringify(badges));
  } catch (e) {
    // The game still works if browser storage is unavailable.
  }
}
      const HISTORY_KEY = "typeblitz_match_history";
      const DAILY_KEY = "typeblitz_daily_progress";

function getDailyProgress() {
  try {
    return JSON.parse(localStorage.getItem(DAILY_KEY) || "{}");
  } catch (e) {
    return {};
  }
}

function saveDailyProgress(progress) {
  try {
    localStorage.setItem(DAILY_KEY, JSON.stringify(progress));
  } catch (e) {
    // Daily progress is optional if storage is unavailable.
  }
}

function getHistory() {
  try {
    const saved = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    return Array.isArray(saved) ? saved : [];
  } catch (e) {
    return [];
  }
}

function saveHistory(history) {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 10)));
  } catch (e) {
    // Match history is optional if storage is unavailable.
  }
}
const SCORE_KEY = "typeblitz_best_score";

function getSavedNumber(key) {
  try {
    return Number(localStorage.getItem(key)) || 0;
  } catch (e) {
    return 0;
  }
}

function saveBest(key, value) {
  try {
    localStorage.setItem(key, String(value));
  } catch (e) {
    // App still works if browser storage is unavailable.
  }
}
      const stateBadge = $("stateBadge");

      let startedAt = null;
      let interval = null;
      let finished = false;
      let previousTypedValue = "";

      function renderPassage() {
        const text = typing.value;
        let html = "";

        for (let i = 0; i < passage.length; i++) {
          const ch = passage[i];
          const safe = ch === "&" ? "&amp;" :
                       ch === "<" ? "&lt;" :
                       ch === ">" ? "&gt;" : ch;

          let cls = "";
          if (i < text.length) {
            cls = text[i] === ch ? "done" : "wrong";
          } else if (i === text.length && !finished) {
            cls = "current";
          }

          html += cls
            ? '<span class="' + cls + '">' + safe + '</span>'
            : safe;
        }

        passageBox.innerHTML = html;
        const current = passageBox.querySelector(".current");
        if (current) {
          const box = passageBox.getBoundingClientRect();
          const target = current.getBoundingClientRect();
          if (target.bottom > box.bottom - 12 || target.top < box.top + 12) {
            current.scrollIntoView({block:"nearest"});
          }
        }
      }

      function updateStats() {
        const text = typing.value;
        let correct = 0;

        for (let i = 0; i < text.length && i < passage.length; i++) {
          if (text[i] === passage[i]) correct++;
        }

        const elapsed = startedAt === null
          ? 0
          : Math.max((Date.now() - startedAt) / 1000, 1);

        const wpm = elapsed > 0 ? correct / 5 / (elapsed / 60) : 0;
        const accuracy = text.length ? correct / text.length * 100 : 100;

        wpmBox.textContent = wpm.toFixed(1);
        accuracyBox.textContent = accuracy.toFixed(1) + "%";
        charsBox.textContent = text.length;

        return {correct, wpm, accuracy};
      }

      function finishTest() {
        if (finished) return;
        finished = true;
        
        playSound("finish");
        
        clearInterval(interval);
        typing.disabled = true;
        timer.textContent = "0";
        stateBadge.textContent = "● MATCH COMPLETE";
        stateBadge.style.color = "#c4b5fd";

        const stats = updateStats();

        
if (dailyChallengeMode) {
  const progress = getDailyProgress();

  if (progress.lastCompletedDate !== dailyChallengeDate) {
    const yesterday = new Date(dailyChallengeDate + "T12:00:00");
    yesterday.setDate(yesterday.getDate() - 1);

    const yesterdayDate = [
      yesterday.getFullYear(),
      String(yesterday.getMonth() + 1).padStart(2, "0"),
      String(yesterday.getDate()).padStart(2, "0")
    ].join("-");

    progress.streak =
      progress.lastCompletedDate === yesterdayDate
        ? (progress.streak || 0) + 1
        : 1;

    progress.lastCompletedDate = dailyChallengeDate;
    progress.lastWpm = Number(stats.wpm.toFixed(1));
    progress.lastAccuracy = Number(stats.accuracy.toFixed(1));

    saveDailyProgress(progress);
  }
}

const score = Math.round(
  stats.correct * 10 + stats.accuracy * 10
);

const previousBestWpm = getSavedNumber(BEST_KEY);
const previousBestScore = getSavedNumber(SCORE_KEY);

const newBestWpm = Math.max(previousBestWpm, stats.wpm);
const newBestScore = Math.max(previousBestScore, score);

saveBest(BEST_KEY, newBestWpm);
saveBest(SCORE_KEY, newBestScore);

const newWpmRecord = stats.wpm > previousBestWpm;
if (newWpmRecord) {
  playSound("record");
}
const newScoreRecord = score > previousBestScore;

const rank = stats.wpm >= 70 && stats.accuracy >= 95 ? "S" :
             stats.wpm >= 50 && stats.accuracy >= 90 ? "A" :
             stats.wpm >= 30 && stats.accuracy >= 85 ? "B" : "C";

        result.style.display = "block";
        resultTitle.textContent = "🏆 MATCH COMPLETE — RANK " + rank;
        rankBadge.textContent = rank;

const rankColors = {
  S: "linear-gradient(135deg, #facc15, #f97316)",
  A: "linear-gradient(135deg, #a78bfa, #6366f1)",
  B: "linear-gradient(135deg, #60a5fa, #2563eb)",
  C: "linear-gradient(135deg, #64748b, #334155)"
};

rankBadge.style.background = rankColors[rank];

recordMessage.textContent =
  newWpmRecord || newScoreRecord
    ? "🏆 NEW RECORD! You beat your previous best!"
    : "Keep practising to beat your personal best!";
    const history = getHistory();

history.unshift({
  date: new Date().toLocaleString(),
  wpm: Number(stats.wpm.toFixed(1)),
  accuracy: Number(stats.accuracy.toFixed(1)),
  score: score,
  rank: rank,
  characters: typing.value.length
});

saveHistory(history);
const unlockedBadges = getUnlockedBadges();
const newBadges = [];

function unlockBadge(id) {
  if (!unlockedBadges.includes(id)) {
    unlockedBadges.push(id);
    const badge = BADGES.find(item => item.id === id);
    if (badge) newBadges.push(badge);
  }
}

unlockBadge("first_match");

if (stats.wpm >= 30) {
  unlockBadge("speedster");
}

if (stats.accuracy >= 95) {
  unlockBadge("sharpshooter");
}

if (newWpmRecord) {
  unlockBadge("record_breaker");
}

saveUnlockedBadges(unlockedBadges);
const badgesBox = $("badgesBox");

if (badgesBox) {
  const savedBadges = getUnlockedBadges();

  badgesBox.innerHTML = `
    <h3 style="margin:20px 0 10px;color:#c4b5fd">
      🏅 ACHIEVEMENTS
    </h3>
    <div style="
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(145px,1fr));
      gap:10px;
    ">
      ${BADGES.map(badge => {
        const unlocked = savedBadges.includes(badge.id);

        return `
          <div style="
            padding:14px;
            border-radius:12px;
            background:${unlocked ? "#211b36" : "#100f20"};
            border:1px solid ${unlocked ? "#a78bfa" : "#342b4c"};
            opacity:${unlocked ? "1" : "0.5"};
            text-align:center;
          ">
            <div style="font-size:28px">
              ${unlocked ? badge.icon : "🔒"}
            </div>
            <strong style="color:#f8f7ff">
              ${badge.name}
            </strong>
            <div style="font-size:11px;color:#c4b5fd;margin-top:5px">
              ${badge.description}
            </div>
            <div style="font-size:10px;margin-top:7px;color:${unlocked ? "#86efac" : "#94a3b8"}">
              ${unlocked ? "UNLOCKED" : "LOCKED"}
            </div>
          </div>
        `;
      }).join("")}
    </div>
  `;
}
const historyBox = $("historyBox");

if (historyBox) {
  const savedHistory = getHistory();

  historyBox.innerHTML = `
    <h3 style="margin:20px 0 10px;color:#c4b5fd">
      📊 LAST 10 MATCHES
    </h3>
    ${savedHistory.map((game, index) => `
      <div style="
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:8px;
        padding:10px;
        margin:6px 0;
        background:#100f20;
        border:1px solid #342b4c;
        border-radius:8px;
        color:#f8f7ff;
        font-size:12px;
      ">
        <span>#${index + 1} · Rank ${game.rank}</span>
        <span>${game.wpm} WPM · ${game.accuracy}%</span>
        <span>${game.score.toLocaleString()} pts</span>
      </div>
    `).join("")}
  `;
}
        resultText.textContent =

  "Final speed: " + stats.wpm.toFixed(1) + " WPM · " +
  "Accuracy: " + stats.accuracy.toFixed(1) + "% · " +
  "Score: " + score.toLocaleString() + " points · " +
  "Personal best: " + newBestWpm.toFixed(1) + " WPM · " +
  "Best score: " + newBestScore.toLocaleString() + " points · " +
  "Characters typed: " + typing.value.length + ". " +
  (newWpmRecord ? "🏆 NEW WPM RECORD! " : "") +
  (newScoreRecord ? "⭐ NEW HIGH SCORE! " : "") +
  "Ready for another round?";

        status.textContent = "Round finished. Start a new match to play again.";
        startButton.textContent = "↻ PLAY AGAIN";
        renderPassage();
      }

      function tick() {
        if (finished || startedAt === null) return;

        const elapsed = (Date.now() - startedAt) / 1000;
        const remaining = Math.max(0, Math.ceil(duration - elapsed));
        timer.textContent = remaining;

        updateStats();
        if (elapsed >= duration) finishTest();
      }

      typing.addEventListener("input", () => {
        if (finished) return;

        if (startedAt === null && typing.value.length > 0) {
          startedAt = Date.now();
          interval = setInterval(tick, 200);
          stateBadge.textContent = "● MATCH LIVE";
          stateBadge.style.color = "#86efac";
          status.textContent = "Keep going! Your match is live.";
        }

        const currentValue = typing.value;

        // Play the normal key sound for correct new characters and the
        // custom/error sound for incorrect new characters. Backspace is silent.
        if (currentValue.length > previousTypedValue.length) {
          for (let i = previousTypedValue.length; i < currentValue.length; i++) {
            if (i >= passage.length) {
              playSound("wrong");
            } else if (currentValue[i] === passage[i]) {
              playSound("key");
            } else {
              playSound("wrong");
            }
          }
        }
        previousTypedValue = currentValue;

        updateStats();
        renderPassage();
      });

      startButton.addEventListener("click", () => {
        clearInterval(interval);
        startedAt = null;
        interval = null;
        finished = false;
        typing.value = "";
        previousTypedValue = "";
        typing.disabled = false;
        timer.textContent = duration;
        wpmBox.textContent = "0.0";
        accuracyBox.textContent = "100%";
        charsBox.textContent = "0";
        result.style.display = "none";
        stateBadge.textContent = "● READY TO PLAY";
        stateBadge.style.color = "#86efac";
        status.textContent = "Countdown starts when you type your first character.";
        startButton.textContent = "↻ RESTART MATCH";
        renderPassage();
        typing.focus();
      });

      renderPassage();
      timer.textContent = duration;
      status.textContent = "Press START MATCH to enter the arena.";
    })();
    </script>
    """.replace("PASSAGE_PLACEHOLDER", passage_json)
   .replace("DURATION_PLACEHOLDER", duration_json)
   .replace("SOUND_PLACEHOLDER", sound_enabled_json)
   .replace("CUSTOM_WRONG_AUDIO_PLACEHOLDER", custom_wrong_sound_json)
   .replace("DAILY_MODE_PLACEHOLDER", daily_mode_json)
   .replace("DAILY_DATE_PLACEHOLDER", daily_date_json),
    height=1100,
    scrolling=True,
)

st.markdown("""
<div class="footer">
TYPEBLITZ ARCADE EDITION &nbsp; • &nbsp; PRACTICE MAKES PROGRESS &nbsp; • &nbsp; PLAY YOUR WAY
</div>
""", unsafe_allow_html=True)
