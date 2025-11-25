import streamlit as st
import time

st.set_page_config(page_title="Complex UI Demo", layout="wide")

# ----------------------------------
# 1️⃣  Initialize session state values
# ----------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "step" not in st.session_state:
    st.session_state.step = 1

if "preferences" not in st.session_state:
    st.session_state.preferences = {}

if "results" not in st.session_state:
    st.session_state.results = None


# ----------------------------------
# 2️⃣  Callback functions
# ----------------------------------

def save_user_info():
    """Triggered when user submits profile form"""
    st.session_state.user = {
        "name": st.session_state.name_input,
        "age": st.session_state.age_input,
    }
    st.session_state.step = 2  # move to next step

def update_preferences():
    """Triggered when preference tab is used"""
    st.session_state.preferences["mode"] = st.session_state.mode_select
    st.session_state.preferences["threshold"] = st.session_state.threshold_slider


@st.cache_resource
def expensive_computation(user, preferences):
    """Expensive heavy computation (cached)"""
    time.sleep(2)  # simulate heavy work
    return {
        "score": preferences["threshold"] * 10 + len(user["name"]),
        "status": "Completed"
    }


def run_analysis():
    """Final analysis step"""

    # ---- FIX: ensure required keys exist ----
    if "mode" not in st.session_state.preferences:
        st.session_state.preferences["mode"] = "Basic"

    if "threshold" not in st.session_state.preferences:
        st.session_state.preferences["threshold"] = 50

    if not st.session_state.user:
        st.error("User info is missing. Please go back and enter details.")
        return
    # -----------------------------------------

    with st.spinner("Running analysis..."):
        st.session_state.results = expensive_computation(
            st.session_state.user,
            st.session_state.preferences
        )
    st.session_state.step = 3


# ----------------------------------
# 3️⃣ SIDE BAR Navigation (State-driven)
# ----------------------------------

st.sidebar.title("Navigation")
st.sidebar.write("Current Step:", st.session_state.step)
st.sidebar.write("User:", st.session_state.user)


# ----------------------------------
# 4️⃣ MAIN UI FLOW
# ----------------------------------

st.title("Complex Streamlit App with Session State Flow")


# -----------------------------
# STEP 1: USER PROFILE FORM
# -----------------------------
if st.session_state.step == 1:
    st.subheader("Step 1: Enter Your Profile")

    with st.form("profile_form"):
        st.text_input("Enter Name:", key="name_input")
        st.number_input("Enter Age:", key="age_input")
        submitted = st.form_submit_button("Save", on_click=save_user_info)

    st.info("Fill the form and click Save.")


# -----------------------------
# STEP 2: USER PREFERENCES
# -----------------------------
elif st.session_state.step == 2:
    st.subheader("Step 2: Select Your Preferences")

    tab1, tab2 = st.tabs(["Mode", "Threshold Settings"])

    with tab1:
        st.selectbox(
            "Choose Mode:",
            ["Basic", "Advanced", "Expert"],
            key="mode_select",
            on_change=update_preferences
        )

    with tab2:
        st.slider(
            "Choose threshold:",
            1, 100, 50,
            key="threshold_slider",
            on_change=update_preferences
        )

    st.write("Current Preferences:", st.session_state.preferences)

    st.button("Run Analysis", on_click=run_analysis)

    st.info("Adjust settings and run analysis.")


# -----------------------------
# STEP 3: RESULTS DISPLAY
# -----------------------------
elif st.session_state.step == 3:
    st.subheader("Step 3: Results")

    st.success("Analysis Complete!")

    st.json(st.session_state.results)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Modify Preferences"):
            st.session_state.step = 2

    with col2:
        if st.button("Start Over"):
            st.session_state.clear()
            st.experimental_rerun()
