import streamlit as st
from auth.auth import AuthManager


def render_login():


    st.write("Please login to continue.")

    employee_id = st.text_input("Employee ID")

    employee_name = st.text_input("Employee Name")

    if st.button("Login", use_container_width=True):

        auth = AuthManager()

        user = auth.login(employee_id, employee_name)

        if user:

            st.session_state.user = user
            st.session_state.authenticated = True

            st.session_state.messages = [

                {
                    "role":"assistant",
                    "content":
                    f"Welcome **{user['name']}** 👋\n\n"
                    f"You are logged in as "
                    f"**{user['department']}**."
                }

            ]

            st.rerun()

        else:

            st.error("Invalid Employee ID or Employee Name.")