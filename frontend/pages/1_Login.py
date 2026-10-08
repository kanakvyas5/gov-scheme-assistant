import streamlit as st

import api_client

st.set_page_config(page_title="Login", page_icon="🔑")
st.title("🔑 Login")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None

if st.session_state.token:
    st.success(f"You're already logged in as {st.session_state.user['name']}.")
    if st.button("Log out"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()
else:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

    if submitted:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            data, error = api_client.login(email, password)
            if error:
                st.error(error)
            else:
                st.session_state.token = data["token"]
                st.session_state.user = data["user"]
                st.success("Logged in successfully!")
                st.rerun()