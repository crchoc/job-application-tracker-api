import os

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide"
)


st.title("💼 Job Application Tracker")
st.write("A simple dashboard for managing job applications.")


if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None


def get_auth_headers():
    if not st.session_state.access_token:
        return {}

    return {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }


def register_user(email, full_name, password):
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={
            "email": email,
            "full_name": full_name or None,
            "password": password
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def login_user(email, password):
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        data={
            "username": email,
            "password": password
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_current_user():
    response = requests.get(
        f"{API_BASE_URL}/auth/me",
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_summary():
    response = requests.get(
        f"{API_BASE_URL}/applications/summary",
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_applications(status=None, search=None):
    params = {
        "sort_by": "id",
        "sort_order": "desc",
        "limit": 100
    }

    if status and status != "all":
        params["status"] = status

    if search:
        params["search"] = search

    response = requests.get(
        f"{API_BASE_URL}/applications",
        params=params,
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def create_application(payload):
    response = requests.post(
        f"{API_BASE_URL}/applications",
        json=payload,
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def update_application(application_id, payload):
    response = requests.patch(
        f"{API_BASE_URL}/applications/{application_id}",
        json=payload,
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def delete_application(application_id):
    response = requests.delete(
        f"{API_BASE_URL}/applications/{application_id}",
        headers=get_auth_headers(),
        timeout=10
    )
    response.raise_for_status()
    return response.json()


with st.sidebar:
    st.header("Account")

    if st.session_state.access_token:
        st.success(f"Logged in as {st.session_state.user_email}")

        if st.button("Logout"):
            st.session_state.access_token = None
            st.session_state.user_email = None
            st.rerun()

    else:
        auth_tab, register_tab = st.tabs(["Login", "Register"])

        with auth_tab:
            with st.form("login_form"):
                login_email = st.text_input("Email", key="login_email")
                login_password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )

                login_submitted = st.form_submit_button("Login")

                if login_submitted:
                    if not login_email or not login_password:
                        st.warning("Email and password are required.")
                    else:
                        try:
                            token_data = login_user(
                                email=login_email,
                                password=login_password
                            )

                            st.session_state.access_token = token_data[
                                "access_token"
                            ]

                            user = get_current_user()
                            st.session_state.user_email = user["email"]

                            st.success("Login successful.")
                            st.rerun()

                        except requests.exceptions.RequestException as error:
                            st.error(f"Login failed: {error}")

        with register_tab:
            with st.form("register_form"):
                register_email = st.text_input(
                    "Email",
                    key="register_email"
                )
                register_full_name = st.text_input(
                    "Full name",
                    key="register_full_name"
                )
                register_password = st.text_input(
                    "Password",
                    type="password",
                    key="register_password"
                )

                register_submitted = st.form_submit_button("Create Account")

                if register_submitted:
                    if not register_email or not register_password:
                        st.warning("Email and password are required.")
                    elif len(register_password) < 8:
                        st.warning("Password must be at least 8 characters.")
                    else:
                        try:
                            register_user(
                                email=register_email,
                                full_name=register_full_name,
                                password=register_password
                            )

                            st.success(
                                "Account created successfully. "
                                "Please log in."
                            )

                        except requests.exceptions.RequestException as error:
                            st.error(f"Registration failed: {error}")


if not st.session_state.access_token:
    st.info("Please log in or create an account to manage job applications.")
    st.stop()


try:
    summary = get_summary()

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Total", summary["total"])
    col2.metric("Saved", summary["saved"])
    col3.metric("Applied", summary["applied"])
    col4.metric("Interview", summary["interview"])
    col5.metric("Rejected", summary["rejected"])
    col6.metric("Offer", summary["offer"])

except requests.exceptions.RequestException:
    st.error(
        "Cannot connect to the FastAPI backend. "
        "Make sure the API is running."
    )
    st.stop()


st.divider()


st.header("Add New Application")

with st.form("create_application_form"):
    company = st.text_input("Company")
    position = st.text_input("Position")
    status = st.selectbox(
        "Status",
        ["saved", "applied", "interview", "rejected", "offer"]
    )
    job_url = st.text_input("Job URL")
    location = st.text_input("Location")
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add Application")

    if submitted:
        if not company or not position:
            st.warning("Company and position are required.")
        else:
            payload = {
                "company": company,
                "position": position,
                "status": status,
                "job_url": job_url or None,
                "location": location or None,
                "notes": notes or None
            }

            try:
                create_application(payload)
                st.success("Application added successfully.")
                st.rerun()
            except requests.exceptions.RequestException as error:
                st.error(f"Failed to add application: {error}")


st.divider()


st.header("Applications")

filter_col1, filter_col2 = st.columns([1, 2])

with filter_col1:
    selected_status = st.selectbox(
        "Filter by status",
        ["all", "saved", "applied", "interview", "rejected", "offer"]
    )

with filter_col2:
    search_keyword = st.text_input("Search keyword")


try:
    applications = get_applications(
        status=selected_status,
        search=search_keyword
    )

    if applications:
        df = pd.DataFrame(applications)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No applications found.")

except requests.exceptions.RequestException as error:
    st.error(f"Failed to load applications: {error}")


st.divider()


st.header("Update Application Status")

with st.form("update_application_form"):
    update_id = st.number_input(
        "Application ID",
        min_value=1,
        step=1
    )
    new_status = st.selectbox(
        "New status",
        ["saved", "applied", "interview", "rejected", "offer"],
        key="update_status"
    )
    update_notes = st.text_area("Update notes")

    update_submitted = st.form_submit_button("Update Application")

    if update_submitted:
        payload = {
            "status": new_status
        }

        if update_notes:
            payload["notes"] = update_notes

        try:
            update_application(int(update_id), payload)
            st.success("Application updated successfully.")
            st.rerun()
        except requests.exceptions.RequestException as error:
            st.error(f"Failed to update application: {error}")


st.divider()


st.header("Delete Application")

with st.form("delete_application_form"):
    delete_id = st.number_input(
        "Application ID to delete",
        min_value=1,
        step=1
    )

    delete_submitted = st.form_submit_button("Delete Application")

    if delete_submitted:
        try:
            delete_application(int(delete_id))
            st.success("Application deleted successfully.")
            st.rerun()
        except requests.exceptions.RequestException as error:
            st.error(f"Failed to delete application: {error}")