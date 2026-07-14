import streamlit as st
from database import register_user, login_user

def auth_page():
    choice = st.sidebar.selectbox(
        "Account",
        ["Login", "Sign Up"]
    )

    if choice == "Login":

        st.subheader("🔐 Login")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.success("Login Successful!")
                st.rerun()

            else:
                st.error("Invalid Email or Password")

    else:

        st.subheader("📝 Sign Up")

        username = st.text_input("Username")
        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if password != confirm_password:
                st.error("Passwords do not match")

            else:
                if register_user(username, email, password):
                    st.success("✅ Account Created Successfully!")
                else:
                    st.error("Email or Username already exists")