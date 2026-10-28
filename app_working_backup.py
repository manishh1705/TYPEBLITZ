
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TypeBlitz",
    page_icon="⌨️",
    layout="centered",
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


def make_passage(level, duration):
    count = min(5000, max(50, int(duration / 60 * 45)))
    words = random.choices(WORDS, k=count)

    if level == "Easy":
        return " ".join(words)

    if level == "Medium":
        result = []
        for i, word in enumerate(words):
            if i % 8 == 0:
                word = word.capitalize()
            if i > 0 and i % 12 == 0:
                result[-1] += random.choice([".", ",", "!"])
            result.append(word)
        result[-1] += "."
        return " ".join(result)

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

    return " ".join(result)


durations = {
    "30 Seconds": 30,
    "1 Minute": 60,
    "2 Minutes": 120,
    "5 Minutes": 300,
    "10 Minutes": 600,
    "20 Minutes": 1200,
    "30 Minutes": 1800,
}

st.title("⌨️ TypeBlitz")
st.caption("Test your typing speed. Build accuracy. Beat your best.")

col1, col2 = st.columns(2)

with col1:
    duration_label = st.selectbox(
        "Test duration", list(durations.keys())
    )

with col2:
    level = st.selectbox(
        "Difficulty", ["Easy", "Medium", "Hard"]
    )

duration = durations[duration_label]

if "passage" not in st.session_state:
    st.session_state.passage = make_passage(level, duration)

if "best_wpm" not in st.session_state:
    st.session_state.best_wpm = 0.0

if st.button("▶ New Test / Restart", type="primary"):
    st.session_state.passage = make_passage(level, duration)

passage = st.session_state.passage

# The timer and typing logic run inside the browser.
# No Streamlit reruns are required while the user types.
passage_json = __import__("json").dumps(passage)
duration_json = __import__("json").dumps(duration)

components.html(
    """
    <div id="typeblitz" style="
        background:#10131c;color:#f1f5f9;padding:12px;
        font-family:Arial,sans-serif;border-radius:12px;
    ">
      <div id="timer" style="
          text-align:center;font-size:32px;font-weight:bold;
          color:#60a5fa;margin:8px;
      ">READY</div>

      <div id="passage" style="
          background:#1b2030;border:1px solid #343b50;
          padding:18px;border-radius:10px;font-size:18px;
          line-height:1.9;overflow-wrap:anywhere;margin-bottom:14px;
      "></div>

      <textarea id="typing" disabled placeholder="Press Start, then type here..."
        style="
          width:100%;height:140px;box-sizing:border-box;
          background:#1b2030;color:#fff;border:1px solid #475569;
          border-radius:8px;padding:12px;font-size:16px;
        "></textarea>

      <button id="start" style="
          width:100%;padding:12px;margin-top:12px;
          background:#2563eb;color:white;border:0;
          border-radius:8px;font-size:16px;cursor:pointer;
      ">Start Test</button>

      <div style="
          display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
          gap:8px;margin-top:16px;text-align:center;
      ">
        <div>WPM<strong id="wpm" style="display:block;font-size:24px">0</strong></div>
        <div>Accuracy<strong id="accuracy" style="display:block;font-size:24px">0%</strong></div>
        <div>Characters<strong id="chars" style="display:block;font-size:24px">0</strong></div>
      </div>
      <div id="status" style="margin-top:14px;text-align:center"></div>
    </div>

    <script>
    (() => {
      const passage = PASSAGE_PLACEHOLDER;
      const duration = DURATION_PLACEHOLDER;

      const timer = document.getElementById("timer");
      const passageBox = document.getElementById("passage");
      const typing = document.getElementById("typing");
      const startButton = document.getElementById("start");
      const wpmBox = document.getElementById("wpm");
      const accuracyBox = document.getElementById("accuracy");
      const charsBox = document.getElementById("chars");
      const status = document.getElementById("status");

      passageBox.textContent = passage;

      let startedAt = null;
      let interval = null;
      let finished = false;

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
        const accuracy = text.length ? correct / text.length * 100 : 0;

        wpmBox.textContent = wpm.toFixed(1);
        accuracyBox.textContent = accuracy.toFixed(1) + "%";
        charsBox.textContent = text.length;

        return {correct, wpm, accuracy};
      }

      function finishTest() {
        if (finished) return;
        finished = true;
        clearInterval(interval);
        typing.disabled = true;
        timer.textContent = "0s";

        const stats = updateStats();
        status.textContent =
          "Test completed! Final WPM: " + stats.wpm.toFixed(1) +
          " · Accuracy: " + stats.accuracy.toFixed(1) + "%";
        startButton.textContent = "Restart Test";
      }

      function tick() {
        if (finished || startedAt === null) return;

        const elapsed = (Date.now() - startedAt) / 1000;
        const remaining = Math.max(0, Math.ceil(duration - elapsed));

        timer.textContent = remaining + "s";
        updateStats();

        if (elapsed >= duration) finishTest();
      }

      typing.addEventListener("input", () => {
        if (finished) return;

        if (startedAt === null && typing.value.length > 0) {
          startedAt = Date.now();
          interval = setInterval(tick, 200);
        }

        updateStats();

        if (typing.value.length >= passage.length) finishTest();
      });

      startButton.addEventListener("click", () => {
        clearInterval(interval);
        startedAt = null;
        finished = false;
        typing.value = "";
        typing.disabled = false;
        timer.textContent = duration + "s";
        wpmBox.textContent = "0.0";
        accuracyBox.textContent = "0.0%";
        charsBox.textContent = "0";
        status.textContent = "Timer starts when you begin typing.";
        startButton.textContent = "Restart Test";
        typing.focus();
      });

      timer.textContent = duration + "s";
      status.textContent = "Press Start Test to begin.";
    })();
    </script>
    """.replace("PASSAGE_PLACEHOLDER", passage_json)
       .replace("DURATION_PLACEHOLDER", duration_json),
    height=590,
    scrolling=False,
)

st.caption(
    "Choose your duration and difficulty above. "
    "New Test / Restart generates a fresh passage."
)
