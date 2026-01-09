import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Jacket Load Distribution",
    layout="centered"
)

# ----------------------------
# DATA
# ----------------------------
REGISTER_FILE = "pressure_register.csv"

JACKETS = {
    "G05": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "H05": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "J05": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.9,"D":16.9}},
    "J04": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "K04": {"EAC":{"A":11.6,"B":11.5,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "L04": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "M04": {"EAC":{"A":11.6,"B":11.2,"C":22.9,"D":12.6}, "OBS":{"A":17.4,"B":19.6,"C":22.9,"D":17.4}},
    "L05": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "M05": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.4,"B":19.6,"C":22.8,"D":17.4}},
    "L06": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "M06": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.4,"B":19.6,"C":22.8,"D":17.4}},
    "L07": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "M07": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.4,"B":19.6,"C":22.8,"D":17.4}},
    "F05": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.4}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "D05": {"EAC":{"A":11.9,"B":11.4,"C":22.3,"D":12.3}, "OBS":{"A":17.8,"B":20.1,"C":22.3,"D":17.0}},
    "E05": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.4}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "E04": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.4}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "G04": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.4}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "K07": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "J07": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "H07": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "G07": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "F07": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "E07": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "D07 (Radar)": {"EAC":{"A":11.8,"B":11.6,"C":22.6,"D":12.1}, "OBS":{"A":17.6,"B":20.4,"C":22.6,"D":16.6}},
    "D06": {"EAC":{"A":12.0,"B":11.4,"C":22.2,"D":12.3}, "OBS":{"A":17.9,"B":20.1,"C":22.2,"D":16.9}},
    "E06": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "F06": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "G06": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "H06": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "J06": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "K06": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "K05": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "L03": {"EAC":{"A":11.6,"B":11.2,"C":22.9,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.9,"D":17.4}},
    "M03": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.4,"B":19.6,"C":22.8,"D":17.4}},
    "L02": {"EAC":{"A":11.6,"B":11.2,"C":22.9,"D":12.7}, "OBS":{"A":17.2,"B":19.6,"C":22.9,"D":17.5}},
    "M01": {"EAC":{"A":11.6,"B":11.2,"C":23.0,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":23.0,"D":17.4}},
    "M02": {"EAC":{"A":11.6,"B":11.1,"C":22.9,"D":12.7}, "OBS":{"A":17.3,"B":19.6,"C":22.9,"D":17.5}},
    "K01": {"EAC":{"A":12.0,"B":11.4,"C":22.2,"D":12.3}, "OBS":{"A":17.9,"B":20.1,"C":22.2,"D":16.9}},
    "L01": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "J01": {"EAC":{"A":11.6,"B":10.8,"C":22.9,"D":13.1}, "OBS":{"A":17.3,"B":19.0,"C":22.9,"D":18.0}},
    "A02": {"EAC":{"A":11.6,"B":11.1,"C":22.9,"D":12.7}, "OBS":{"A":17.3,"B":19.6,"C":22.9,"D":17.5}},
    "A03": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "A04": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "H04": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "H01": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "H02": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "G02": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "D04": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "E03": {"EAC":{"A":11.6,"B":11.2,"C":22.8,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.8,"D":17.4}},
    "C04": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "B04": {"EAC":{"A":11.6,"B":11.4,"C":22.8,"D":12.3}, "OBS":{"A":17.4,"B":20.1,"C":22.8,"D":16.9}},
    "B02": {"EAC":{"A":11.6,"B":11.2,"C":23.0,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":23.0,"D":17.4}},
    "B03": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "C02": {"EAC":{"A":11.6,"B":11.2,"C":23.0,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":23.0,"D":17.4}},
    "C03": {"EAC":{"A":11.6,"B":11.2,"C":22.9,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":22.9,"D":17.4}},
    "E02": {"EAC":{"A":11.6,"B":11.2,"C":23.0,"D":12.6}, "OBS":{"A":17.3,"B":19.6,"C":23.0,"D":17.4}},
    "D03": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "F02": {"EAC":{"A":11.9,"B":11.4,"C":22.4,"D":12.3}, "OBS":{"A":17.8,"B":20.1,"C":22.4,"D":16.9}},
    "E01": {"EAC":{"A":11.9,"B":11.4,"C":22.4,"D":12.3}, "OBS":{"A":17.8,"B":20.1,"C":22.4,"D":16.9}},
    "F01": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
    "G01": {"EAC":{"A":11.6,"B":11.4,"C":22.9,"D":12.3}, "OBS":{"A":17.3,"B":20.1,"C":22.9,"D":17.0}},
}

LEG_LABELS = {
    "A": "BP (A)",
    "B": "BQ (B)",
    "C": "AQ (C)",
    "D": "AP (D)"
}

# ----------------------------
# FUNCTIONS
# ----------------------------
from datetime import datetime, timedelta

def save_pressures(jacket_id, case, pressures):
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    new_row = {
        "Jacket ID": jacket_id,
        "Case": case,
        "Date Time (UTC)": now,   # ✅ ONLY change
        "BP (A)": pressures["A"],
        "BQ (B)": pressures["B"],
        "AQ (C)": pressures["C"],
        "AP (D)": pressures["D"],
        "Comment": ""
    }

    if os.path.exists(REGISTER_FILE):
        df = pd.read_csv(REGISTER_FILE)

        # 🔑 FIX: rename old column if it exists
        if "DateTime" in df.columns:
            df = df.rename(columns={"DateTime": "Date Time (UTC)"})

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(REGISTER_FILE, index=False)
    return len(df) - 1

def load_register():
    if os.path.exists(REGISTER_FILE):
        return pd.read_csv(REGISTER_FILE)
    return pd.DataFrame()

def leg_box(label, value, minimum):
    color = "#2ecc71" if value >= minimum else "#e74c3c"
    return f"""
    <div style="
        background-color:{color};
        color:white;
        padding:12px;
        border-radius:12px;
        text-align:center;
        font-size:14px;
        min-height:90px;">
        <strong>{label}</strong><br>
        {value:.1f}%<br>
        <span style="font-size:12px;">Min: {minimum:.1f}%</span>
    </div>
    """

# ----------------------------
# HEADER
# ----------------------------
st.title("⚖️ Jacket Load Distribution")
st.caption("Le Treport OWF - DEME OFFSHORE")

# ----------------------------
# SELECTION
# ----------------------------
st.subheader("Jacket & Case")
jacket_id = st.selectbox("Jacket ID", list(JACKETS.keys()))
case = st.radio("Case", ["EAC", "OBS"], horizontal=True)
min_targets = JACKETS[jacket_id][case]

# ----------------------------
# PRESSURE INPUTS
# ----------------------------
st.subheader("Pressure Input (bar)")
col1, col2 = st.columns(2)
with col1:
    pA = st.number_input("BP (A)", min_value=0.0, step=0.1)
    pC = st.number_input("AQ (C)", min_value=0.0, step=0.1)
with col2:
    pB = st.number_input("BQ (B)", min_value=0.0, step=0.1)
    pD = st.number_input("AP (D)", min_value=0.0, step=0.1)

pressures = {"A": pA, "B": pB, "C": pC, "D": pD}

# ----------------------------
# DATA LOGGING (IMMEDIATELY BELOW INPUT)
# ----------------------------
st.subheader("Data Logging")
col_save, col_view = st.columns(2)

# Track last saved record in session state
if "last_saved_index" not in st.session_state:
    st.session_state["last_saved_index"] = None

# --- SAVE PRESSURES BUTTON ---
with col_save:
    if st.button("💾 Save Pressures", use_container_width=True):
        # Save pressures first
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
            "Jacket ID": jacket_id,
            "Case": case,
            "DateTime": now,
            "BP (A)": pressures["A"],
            "BQ (B)": pressures["B"],
            "AQ (C)": pressures["C"],
            "AP (D)": pressures["D"],
            "Comment": ""  # initially empty
        }

        if os.path.exists(REGISTER_FILE):
            df = pd.read_csv(REGISTER_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])

        df.to_csv(REGISTER_FILE, index=False)
        st.session_state["last_saved_index"] = len(df) - 1  # store index for comment
        st.success("Pressures saved successfully!")

# --- COMMENT INPUT FOR LAST SAVED RECORD ---
if st.session_state.get("last_saved_index") is not None:
    df = pd.read_csv(REGISTER_FILE)
    idx = st.session_state["last_saved_index"]
    comment = st.text_input(
        "Add a comment for last record:",
        value=df.at[idx, "Comment"]
    )
    if st.button("💬 Save Comment"):
        df.at[idx, "Comment"] = comment
        df.to_csv(REGISTER_FILE, index=False)
        st.success("Comment saved!")

# --- VIEW REGISTER BUTTON (TOGGLE) ---
with col_view:
    if st.button("📋 Register", use_container_width=True):
        # Toggle the boolean
        st.session_state["show_register"] = not st.session_state.get("show_register", False)

# --- DISPLAY REGISTER ---
if st.session_state.get("show_register", False):
    st.subheader("Pressure Register")
    df = pd.read_csv(REGISTER_FILE)
    if df.empty:
        st.info("No records available.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

# ----------------------------
# CALCULATIONS
# ----------------------------
total_pressure = sum(pressures.values())
if total_pressure > 0:
    percentages = {k: (v / total_pressure) * 100 for k, v in pressures.items()}
else:
    percentages = {k: 0 for k in pressures}

# ----------------------------
# RESULTS
# ----------------------------
st.subheader("Results")
st.metric("Total Pressure (bar)", f"{total_pressure:.2f}")

# ----------------------------
# VISUALIZATION
# ----------------------------
st.subheader("Jacket Visualization")
html_layout = f"""
<div style="max-width:360px;margin:auto;font-family:Arial;">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">

    <div style="display:flex;align-items:center;gap:8px;">
        <div style="
            background-color:#7f8c8d;
            color:white;
            padding:4px;
            border-radius:6px;
            font-size:11px;
            width:34px;
            height:34px;
            display:flex;
            align-items:center;
            justify-content:center;">
            BL
        </div>
        {leg_box("BP (A)", percentages["A"], min_targets["A"])}
    </div>

    {leg_box("BQ (B)", percentages["B"], min_targets["B"])}
    {leg_box("AQ (C)", percentages["C"], min_targets["C"])}
    {leg_box("AP (D)", percentages["D"], min_targets["D"])}

</div>
<div style="
    margin-top:14px;
    background-color:#34495e;
    color:white;
    padding:12px;
    border-radius:12px;
    text-align:center;">
    <strong>{jacket_id}</strong>
</div>
</div>
"""
components.html(html_layout, height=420)

# ----------------------------
# WARNINGS
# ----------------------------
failed = [
    LEG_LABELS[k] for k in percentages
    if percentages[k] < min_targets[k]
]

if failed:
    st.warning(
        f"⚠️ Minimum load distribution NOT achieved on: {', '.join(failed)}\n\n"
        "Suggested action:\n"
        "Re-level the jacket. Remember to watch the level indicator while levelling."
    )
else:
    st.success("✅ All legs meet minimum load distribution requirements.")
