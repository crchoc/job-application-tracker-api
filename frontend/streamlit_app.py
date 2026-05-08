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


def get_summary():
    response = requests.get(f"{API_BASE_URL}/applications/summary", timeout=10)
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
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def create_application(payload):
    response = requests.post(
        f"{API_BASE_URL}/applications",
        json=payload,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def update_application(application_id, payload):
    response = requests.patch(
        f"{API_BASE_URL}/applications/{application_id}",
        json=payload,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def delete_application(application_id):
    response = requests.delete(
        f"{API_BASE_URL}/applications/{application_id}",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


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
        "Make sure the API is running at http://127.0.0.1:8000"
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