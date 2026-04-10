import streamlit as st
import numpy as np
import pandas as pd
import time
import random

st.set_page_config(layout="wide")
st.title("QAirBrain Dashboard")

# -----------------------
# SIMULATED SENSOR DATA
# -----------------------
co2 = np.random.randint(400, 2000)
hrv = np.random.randint(30, 80)
gsr = np.random.uniform(1, 6)

# -----------------------
# COGNITION STORAGE
# -----------------------
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None

if "baseline_rt" not in st.session_state:
    st.session_state.baseline_rt = None

if "stroop_score" not in st.session_state:
    st.session_state.stroop_score = 0.5

if "memory_score" not in st.session_state:
    st.session_state.memory_score = 0.5

# -----------------------
# RISK MODEL
# -----------------------
cog_norm = 0.7  # default

if st.session_state.reaction_time:
    rt_ms = st.session_state.reaction_time * 1000
    if st.session_state.baseline_rt:
        cog_norm = min(1, st.session_state.baseline_rt / rt_ms)

co2_norm = co2 / 2000
hrv_norm = hrv / 80
gsr_norm = gsr / 6

risk = int((0.3*co2_norm + 
            0.25*(1-hrv_norm) + 
            0.2*gsr_norm + 
            0.25*(1-cog_norm)) * 100)

# -----------------------
# TOP METRICS
# -----------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("CO2 (ppm)", co2)
col2.metric("HRV (ms)", hrv)
col3.metric("GSR (µS)", round(gsr,2))
col4.metric("Risk Score", risk)

# Risk level
if risk < 40:
    st.success("Low Risk")
elif risk < 70:
    st.warning("Moderate Risk")
else:
    st.error("High Risk")

# Alerts
if co2 > 1200:
    st.warning("Poor ventilation detected!")

if risk > 70:
    st.error("High cognitive risk! Take cognition test.")

st.divider()

# -----------------------
# GRAPHS
# -----------------------
data = pd.DataFrame({
    "CO2": np.random.randint(400, 2000, 20),
    "HRV": np.random.randint(30, 80, 20),
    "GSR": np.random.uniform(1, 6, 20)
})

col1, col2 = st.columns(2)
col1.line_chart(data["CO2"])
col2.line_chart(data["HRV"])
st.line_chart(data["GSR"])

st.divider()

import streamlit as st
import numpy as np
import pandas as pd
import time
import random

st.set_page_config(layout="wide")
st.title("QAirBrain Dashboard")

# -----------------------
# SENSOR DATA
# -----------------------
co2 = np.random.randint(400, 2000)
hrv = np.random.randint(30, 80)
gsr = np.random.uniform(1, 6)

col1, col2, col3, col4 = st.columns(4)
col1.metric("CO2 (ppm)", co2)
col2.metric("HRV (ms)", hrv)
col3.metric("GSR (µS)", round(gsr,2))
import streamlit as st
import numpy as np
import pandas as pd
import time
import random

st.set_page_config(layout="wide")
st.title("QAirBrain Dashboard")

# -----------------------
# USER INPUT
# -----------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

name = st.text_input("Enter your name:", st.session_state.user_name)
if name:
    st.session_state.user_name = name

# -----------------------
# SENSOR DATA (SIMULATED)
# -----------------------
co2 = np.random.randint(400, 2000)
hrv = np.random.randint(30, 80)
gsr = np.random.uniform(1, 6)

# store CO2 history
if "co2_history" not in st.session_state:
    st.session_state.co2_history = []

st.session_state.co2_history.append(co2)

# -----------------------
# METRICS
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("CO2 (ppm)", co2)
col2.metric("HRV (ms)", hrv)
col3.metric("GSR (µS)", round(gsr,2))

st.divider()

# -----------------------
# SESSION INIT
# -----------------------
for key in ["rt_score","stroop_score","memory_score"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "baseline_data" not in st.session_state:
    st.session_state.baseline_data = None

if "baseline_time" not in st.session_state:
    st.session_state.baseline_time = None

if "baseline_co2" not in st.session_state:
    st.session_state.baseline_co2 = None

# -----------------------
# REACTION TEST (STABLE)
# -----------------------
st.subheader("Reaction Test")

if "rt_active" not in st.session_state:
    st.session_state.rt_active = False
    st.session_state.rt_start = 0
    st.session_state.rt_results = []
    st.session_state.rt_trial = 0

if not st.session_state.rt_active:
    if st.button("Start Reaction Test"):
        st.session_state.rt_active = True
        st.session_state.rt_results = []
        st.session_state.rt_trial = 0

if st.session_state.rt_active:
    st.write(f"Trial {st.session_state.rt_trial+1}/3")

    if st.button("CLICK", key=f"rt_{st.session_state.rt_trial}"):

        now = time.time()

        if st.session_state.rt_start == 0:
            st.session_state.rt_start = now
            st.info("Click again FAST")
        else:
            rt = now - st.session_state.rt_start
            st.session_state.rt_results.append(rt)
            st.session_state.rt_start = 0
            st.session_state.rt_trial += 1

    if st.session_state.rt_trial >= 3:
        avg = np.mean(st.session_state.rt_results)
        score = max(0.2, min(1, 0.6/avg))
        st.session_state.rt_score = score
        st.write(f"Reaction Score: {round(score,2)}")
        st.session_state.rt_active = False

# -----------------------
# STROOP TEST (YOUR VERSION)
# -----------------------
st.subheader("Stroop Test")

colors = ["RED","GREEN","BLUE","YELLOW"]

if "stroop_trial" not in st.session_state:
    st.session_state.stroop_trial = 0
    st.session_state.stroop_results = []
    st.session_state.stroop_active = False
    st.session_state.stroop_start = 0

if not st.session_state.stroop_active:
    if st.button("Start Stroop"):
        st.session_state.stroop_trial = 0
        st.session_state.stroop_results = []
        st.session_state.stroop_active = True

if st.session_state.stroop_active:

    if st.session_state.stroop_trial < 10:

        word = random.choice(colors)
        ink = random.choice(colors)

        st.markdown(f"<h2 style='color:{ink.lower()}'>{word}</h2>", unsafe_allow_html=True)

        if st.session_state.stroop_start == 0:
            st.session_state.stroop_start = time.time()

        cols = st.columns(len(colors))

        for i, c in enumerate(colors):
            if cols[i].button(c, key=f"s_{st.session_state.stroop_trial}_{c}"):

                rt = time.time() - st.session_state.stroop_start
                correct = (c == ink)

                st.session_state.stroop_results.append({"correct": correct, "rt": rt})
                st.session_state.stroop_trial += 1
                st.session_state.stroop_start = 0
                st.rerun()

    else:
        acc = sum(r["correct"] for r in st.session_state.stroop_results)/10
        st.session_state.stroop_score = acc
        st.write("Stroop Score:", round(acc,2))
        st.session_state.stroop_active = False

# -----------------------
# MEMORY TEST
# -----------------------
st.subheader("Memory Test")

if "mem_level" not in st.session_state:
    st.session_state.mem_level = 1
    st.session_state.mem_score = 0
    st.session_state.mem_active = False
    st.session_state.mem_sequence = ""
    st.session_state.mem_show = False

if not st.session_state.mem_active:
    if st.button("Start Memory"):
        st.session_state.mem_level = 1
        st.session_state.mem_score = 0
        st.session_state.mem_active = True
        st.session_state.mem_show = True

if st.session_state.mem_active:

    if st.session_state.mem_show:
        seq = "".join([str(random.randint(0,9)) for _ in range(st.session_state.mem_level)])
        st.session_state.mem_sequence = seq

        st.markdown(f"## {seq}")
        time.sleep(1)
        st.session_state.mem_show = False
        st.rerun()

    else:
        user = st.text_input("Enter sequence:")

        if st.button("Submit Memory"):

            if user == st.session_state.mem_sequence:
                st.session_state.mem_score += 1
                st.session_state.mem_level += 1
                st.session_state.mem_show = True
                st.rerun()
            else:
                score = min(1, st.session_state.mem_score/5)
                st.session_state.memory_score = score
                st.write("Memory Score:", score)
                st.session_state.mem_active = False

# -----------------------
# SAVE BASELINE
# -----------------------
st.divider()
st.subheader("Save Baseline")

if st.button("Save Baseline"):

    if None in [st.session_state.rt_score,
                st.session_state.stroop_score,
                st.session_state.memory_score]:
        st.error("Complete all tests first")

    elif not st.session_state.user_name:
        st.error("Enter your name")

    else:
        st.session_state.baseline_data = {
            "rt": st.session_state.rt_score,
            "stroop": st.session_state.stroop_score,
            "memory": st.session_state.memory_score
        }

        st.session_state.baseline_time = time.time()
        st.session_state.baseline_co2 = co2

        st.success("Baseline Saved!")

# -----------------------
# SHOW BASELINE
# -----------------------
if st.session_state.baseline_data:

    st.subheader("Baseline Profile")
    st.write("User:", st.session_state.user_name)
    st.write(st.session_state.baseline_data)

# -----------------------
# RETEST CONDITION (ADVANCED)
# -----------------------
if st.session_state.baseline_data:

    st.subheader("Re-Test Condition")

    time_passed = time.time() - st.session_state.baseline_time
    co2_change = abs(co2 - st.session_state.baseline_co2)

    st.write(f"Time passed: {int(time_passed)} sec")
    st.write(f"CO2 change: {co2_change} ppm")

    if time_passed > 600 and co2_change > 200:
        st.success("Conditions satisfied. You can take test again")

        if st.button("Take Test Again"):
            st.session_state.rt_score = None
            st.session_state.stroop_score = None
            st.session_state.memory_score = None

    else:
        st.warning("Wait until CO2 changes and stabilizes (10 min)")

# -----------------------
# FINAL COGNITION
# -----------------------
if st.session_state.baseline_data and \
   st.session_state.rt_score and \
   st.session_state.stroop_score and \
   st.session_state.memory_score:

    base = st.session_state.baseline_data

    # RT (raw comparison)
    current_rt = np.mean(st.session_state.rt_results)
    rt = base["rt"] / current_rt

    # Stroop & Memory (already normalized)
    stroop = st.session_state.stroop_score / base["stroop"]
    memory = st.session_state.memory_score / base["memory"]

    cog = int((0.4*rt + 0.3*stroop + 0.3*memory)*100)

    st.subheader("Cognition Score (vs Baseline)")
    st.metric("Score", cog)