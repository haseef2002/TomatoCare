# src/utils/auth.py
import streamlit as st
import json
import os
import hashlib
from streamlit_google_auth import Authenticate

# Pathing setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
USERS_FILE = os.path.join(BASE_DIR, 'app', 'users.json')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    with open(USERS_FILE, 'r') as f:
        try: return json.load(f)
        except: return {}

def save_user(username, password, email=None):
    users = load_users()
    if username in users: return False
    users[username] = {
        "password": hash_password(password),
        "email": email if email else "Not Provided",
        "role": "User"
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    return True

def verify_login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return username
    return None

def check_auth():
    if 'connected' not in st.session_state:
        st.session_state['connected'] = False
        st.session_state['user_name'] = ""
        st.session_state['guest_mode'] = False

    if st.session_state['connected'] or st.session_state['guest_mode']:
        return

    st.title("🍅 TomatoCare AI Expert System")
    st.markdown("Select a pathway to access the diagnostic engine.")
    
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Register", "👤 Guest Mode"])
    
    with tab1:
        st.subheader("Login")
        u = st.text_input("Username", key="l_u")
        p = st.text_input("Password", type="password", key="l_p")
        if st.button("Access Dashboard"):
            user = verify_login(u, p)
            if user:
                st.session_state.connected, st.session_state.user_name = True, user
                st.rerun()
            else: st.error("Invalid credentials.")

    with tab2:
        st.subheader("Create Account")
        new_u = st.text_input("Choose Username")
        new_p = st.text_input("Choose Password", type="password")
        new_e = st.text_input("Gmail (Optional - for disease alerts)")
        if st.button("Register"):
            if len(new_u) < 3 or len(new_p) < 5:
                st.warning("Username/Password too short.")
            elif save_user(new_u, new_p, new_e):
                st.success("Registered! Please switch to the Login tab.")
            else: st.error("Username already taken.")


    with tab3:
        st.subheader("Guest Access")
        st.write("Browse the encyclopedia and use the scanner with limited history saving.")
        if st.button("Enter as Guest"):
            st.session_state.guest_mode = True
            st.session_state.user_name = "Guest User"
            st.rerun()
            
    st.stop()