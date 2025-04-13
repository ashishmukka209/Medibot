# import streamlit as st
# import requests
# import time
# import random

# # Streamlit page config
# st.set_page_config(page_title="MediBot Dashboard", page_icon="🩺", layout="wide")

# # Hide Streamlit UI elements
# hide_streamlit_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display:none;}
#     </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# # Fade-in animation
# fade_in_animation = """
#     <style>
#     .fade-in {
#         animation: fadeInAnimation 1s ease-in forwards;
#     }
#     @keyframes fadeInAnimation {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
#     </style>
# """
# st.markdown(fade_in_animation, unsafe_allow_html=True)

# # Title
# st.title("🩺 MediBot Real-Time Dashboard")

# # Sidebar
# st.sidebar.header("Details")
# api_url = "http://127.0.0.1:8000/vitals"
# token = st.sidebar.text_input("Enter Your Access Token", type="password")

# # Dummy patient IDs
# patient_ids = ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]

# # Initialize session state
# if "started" not in st.session_state:
#     st.session_state["started"] = False

# # Buttons in Sidebar
# start_clicked = stop_clicked = False  # Track clicks separately

# if not st.session_state["started"]:
#     start_clicked = st.sidebar.button("▶️ Start Monitoring")
# else:
#     stop_clicked = st.sidebar.button("⏹️ Stop Monitoring")

# # Immediate action after clicking
# if start_clicked:
#     st.session_state["started"] = True
#     st.rerun()  # 🔥 Immediately rerun to reflect button change

# if stop_clicked:
#     st.session_state.clear()
#     st.success("✅ Logged out successfully!")
#     st.rerun()  # 🔥 Immediately rerun to reflect button change

# # Main Monitoring Area
# if st.session_state.get("started", False):

#     dummy_vitals = {
#         "patient_id": random.choice(patient_ids),
#         "heart_rate": random.randint(55, 140),
#         "oxygen": random.randint(85, 100),
#         "temperature": round(random.uniform(95.0, 104.0), 1),
#         "bp_sys": random.randint(90, 180),
#         "bp_dia": random.randint(60, 120),
#         "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
#     }
    
#     headers = {"Authorization": f"Bearer {token}"}
#     try:
#         response = requests.post(api_url, json=dummy_vitals, headers=headers)

#         if response.status_code == 200:
#             data = response.json()

#             # Card color
#             if data['status'] == "Critical":
#                 card_color = "#5c1a1a"
#                 blink = True
#             elif data['status'] == "Abnormal":
#                 card_color = "#5c4b1a"
#                 blink = False
#             else:
#                 card_color = "#1a5c2b"
#                 blink = False

#             # Patient Card
#             st.markdown(
#                 f"""
#                 <div class="fade-in" style="background-color: {card_color}; padding: 20px; border-radius: 10px;">
#                     <h3 style="color: white;">🆔 Patient ID: {data['patient_id']}</h3>
#                     <div style="display: flex; justify-content: space-between; color: white;">
#                         <div>
#                             ❤️ <strong>Heart Rate (bpm):</strong> {dummy_vitals['heart_rate']}<br>
#                             🌡️ <strong>Temperature (°F):</strong> {dummy_vitals['temperature']}
#                         </div>
#                         <div>
#                             🫁 <strong>Oxygen (%):</strong> {dummy_vitals['oxygen']}<br>
#                             🩸 <strong>Blood Pressure (mmHg):</strong> {dummy_vitals['bp_sys']}/{dummy_vitals['bp_dia']}
#                         </div>
#                     </div>
#                     <hr style="border: 1px solid white;">
#                     <h4 style="color: white;">🚨 Status: {data['status']}</h4>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # Emergency blinking if Critical
#             if blink:
#                 st.markdown(
#                     """
#                     <style>
#                     @keyframes blink {
#                         0% {opacity: 1;}
#                         50% {opacity: 0;}
#                         100% {opacity: 1;}
#                     }
#                     .blink {
#                         animation: blink 1s infinite;
#                         color: red;
#                         font-size: 40px;
#                         text-align: center;
#                     }
#                     </style>
#                     <div class="blink">🚨 EMERGENCY 🚨</div>
#                     """,
#                     unsafe_allow_html=True
#                 )

#             # Medical Report
#             st.subheader("📃 Medical Report")
#             st.text_area("Report", data['report'], height=300, key=random.randint(0, 1000000))

#             # Wait 10 seconds for next patient
#             time.sleep(2)
#             st.rerun()

#         else:
#             st.error(f"❌ API Error: {response.status_code} - {response.text}")

#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")
import streamlit as st
import requests
import time
import random

# 🚑 Streamlit page config
st.set_page_config(page_title="MediBot Dashboard", page_icon="🩺", layout="wide")

# 🚫 Hide Streamlit UI elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 🎨 Fade-in animation
fade_in_animation = """
    <style>
    .fade-in {
        animation: fadeInAnimation 1s ease-in forwards;
    }
    @keyframes fadeInAnimation {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
"""
st.markdown(fade_in_animation, unsafe_allow_html=True)

# 🩺 Title
st.title("🩺 MediBot Real-Time Dashboard")

# 🛠️ Sidebar
st.sidebar.header("Details")
api_url = "http://127.0.0.1:8000/vitals"
token = st.sidebar.text_input("Enter Your Access Token", type="password")

# Dummy patient IDs
patient_ids = ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]

# Initialize session state
if "started" not in st.session_state:
    st.session_state["started"] = False

# Buttons in Sidebar
start_clicked = stop_clicked = False

if not st.session_state["started"]:
    start_clicked = st.sidebar.button("▶️ Start Monitoring")
else:
    stop_clicked = st.sidebar.button("⏹️ Stop Monitoring")

# Immediate action after clicking
if start_clicked:
    st.session_state["started"] = True
    st.rerun()

if stop_clicked:
    st.session_state.clear()
    st.success("✅ Logged out successfully!")
    st.rerun()

# Main Monitoring Area
if st.session_state.get("started", False):

    dummy_vitals = {
        "patient_id": random.choice(patient_ids),
        "heart_rate": random.randint(55, 140),
        "oxygen": random.randint(85, 100),
        "temperature": round(random.uniform(95.0, 104.0), 1),
        "bp_sys": random.randint(90, 180),
        "bp_dia": random.randint(60, 120),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(api_url, json=dummy_vitals, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Card color
            if data['status'] == "Critical":
                card_color = "#5c1a1a"
                blink = True
            elif data['status'] == "Abnormal":
                card_color = "#5c4b1a"
                blink = False
            else:
                card_color = "#1a5c2b"
                blink = False

            # 🩺 Patient Card
            st.markdown(
                f"""
                <div class="fade-in" style="background-color: {card_color}; padding: 20px; border-radius: 10px;">
                    <h3 style="color: white;">🆔 Patient ID: {data['patient_id']}</h3>
                    <div style="display: flex; justify-content: space-between; color: white;">
                        <div>
                            ❤️ <strong>Heart Rate (bpm):</strong> {dummy_vitals['heart_rate']}<br>
                            🌡️ <strong>Temperature (°F):</strong> {dummy_vitals['temperature']}
                        </div>
                        <div>
                            🫁 <strong>Oxygen (%):</strong> {dummy_vitals['oxygen']}<br>
                            🩸 <strong>Blood Pressure (mmHg):</strong> {dummy_vitals['bp_sys']}/{dummy_vitals['bp_dia']}
                        </div>
                    </div>
                    <hr style="border: 1px solid white;">
                    <h4 style="color: white;">🚨 Status: {data['status']}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 🚨 Emergency blinking if Critical
            if blink:
                st.markdown(
                    """
                    <style>
                    @keyframes blink {
                        0% {opacity: 1;}
                        50% {opacity: 0;}
                        100% {opacity: 1;}
                    }
                    .blink {
                        animation: blink 1s infinite;
                        color: red;
                        font-size: 40px;
                        text-align: center;
                    }
                    </style>
                    <div class="blink">🚨 EMERGENCY 🚨</div>
                    """,
                    unsafe_allow_html=True
                )

            # 📃 Medical Report
            st.subheader("📃 Medical Report")
            st.markdown(data['report'], unsafe_allow_html=True)  # << 🔥 CHANGE: show HTML report properly

            # Wait 2 seconds for next patient
            time.sleep(2)
            st.rerun()

        else:
            st.error(f"❌ API Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
