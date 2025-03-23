import streamlit as st
from time_management_page import show_time_management_page
from learning_companion_page import show_learning_companion_page
from adhd_vertexai_chatbot import virtual_consultation

# Apply Enhanced Custom CSS for Styling & Animation
st.markdown(
    """
    <style>
    /* Soft Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    }

    /* Subtle Fade-in animation for title */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-10px); }
        100% { opacity: 1; transform: translateY(0px); }
    }
    .float-text {
        animation: fadeIn 2s ease-in-out;
        text-align: center;
        font-size: 44px;
        font-weight: bold;
        color: #2c3e50;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        padding-top: 25px;
    }

    /* Subtle Fade-in animation for subtitle */
    @keyframes fadeInSlow {
        0% { opacity: 0; transform: translateY(5px); }
        100% { opacity: 1; transform: translateY(0px); }
    }
    .wave-text {
        animation: fadeInSlow 2.5s ease-in-out;
        text-align: center;
        font-size: 28px;
        color: #34495e;
        font-weight: 500;
        margin-top: 12px;
        margin-bottom: 50px;
    }

    /* Improved Button Styling */
    .stButton>button {
        width: 300px;
        padding: 16px;
        font-size: 20px;
        background: linear-gradient(to right, #6a89cc, #4a69bd);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        box-shadow: 3px 5px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 14px;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #4a69bd, #1e3799);
        transform: scale(1.05);
        box-shadow: 4px 6px 18px rgba(0, 0, 0, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Simulate page navigation using session_state
if 'page' not in st.session_state:
    st.session_state.page = "home"
 

# Home Page Content
if st.session_state.page == "home":
    # Title with Subtle Fade-in Effect
    st.markdown('<div class="float-text">Welcome to NeuroNavigation!</div>', unsafe_allow_html=True)

    # Subtitle with Subtle Fade-in Effect
    st.markdown('<div class="wave-text">How can we assist you today?</div>', unsafe_allow_html=True)

    # Centered Buttons Using Columns for Alignment
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        
        if st.button("⏳ Time Management"):
            st.session_state.page = "time_management"
            st.rerun()  # Rerun the app to update the page
        if st.button("📚 Learning Companion"):
            st.session_state.page = "learning_companion"
            st.rerun()  # Rerun the app to update the page
        if st.button("🔍 Virtual Consultation"):
            st.session_state.page = "virtual_consultation"
            st.rerun()  # Rerun the app to update the page

# Virtual Consultation Page
elif st.session_state.page == "virtual_consultation":
    virtual_consultation()

# Time Management Page
elif st.session_state.page == "time_management":
    show_time_management_page()  # Call the function from the external file

# Learning Companion Page
elif st.session_state.page == "learning_companion":
    show_learning_companion_page()

   