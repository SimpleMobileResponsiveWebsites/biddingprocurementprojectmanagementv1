import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = []


def add_project():
    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Add Project"):
        project = {
            "name": project_name,
            "description": project_description,
            "start_date": start_date,
            "end_date": end_date,
            "bids": [],
            "procurement_items": []
        }
        st.session_state.projects.append(project)
        st.success("Project added successfully!")


def add_bid():
    if not st.session_state.projects:
        st.warning("No projects available. Please add a project first.")
        return

    project_names = [p["name"] for p in st.session_state.projects]
    selected_project = st.selectbox("Select Project", project_names)

    bidder_name = st.text_input("Bidder Name")
    bid_amount = st.number_input("Bid Amount", min_value=0.0, step=0.01)
    bid_date = st.date_input("Bid Date")

    if st.button("Add Bid"):
        for project in st.session_state.projects:
            if project["name"] == selected_project:
                project["bids"].append({
                    "bidder": bidder_name,
                    "amount": bid_amount,
                    "date": bid_date
                })
                st.success("Bid added successfully!")
                break


def manage_procurement():
    if not st.session_state.projects:
        st.warning("No projects available. Please add a project first.")
        return

    project_names = [p["name"] for p in st.session_state.projects]
    selected_project = st.selectbox("Select Project", project_names)

    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01)

    if st.button("Add Procurement Item"):
        for project in st.session_state.projects:
            if project["name"] == selected_project:
                project["procurement_items"].append({
                    "item": item_name,
                    "quantity": quantity,
                    "unit_price": unit_price
                })
                st.success("Procurement item added successfully!")
                break


def view_projects():
    if not st.session_state.projects:
        st.warning("No projects available.")
        return

    for project in st.session_state.projects:
        st.subheader(project["name"])
        st.write(f"Description: {project['description']}")
        st.write(f"Start Date: {project['start_date']}")
        st.write(f"End Date: {project['end_date']}")

        st.write("Bids:")
        for bid in project["bids"]:
            st.write(f"- {bid['bidder']}: ${bid['amount']} on {bid['date']}")

        st.write("Procurement Items:")
        for item in project["procurement_items"]:
            st.write(f"- {item['item']}: {item['quantity']} units at ${item['unit_price']} each")

        st.write("---")


def download_csv():
    if not st.session_state.projects:
        st.warning("No projects available to download.")
        return

    data = []
    for project in st.session_state.projects:
        project_data = {
            "Project Name": project["name"],
            "Description": project["description"],
            "Start Date": project["start_date"],
            "End Date": project["end_date"],
            "Number of Bids": len(project["bids"]),
            "Number of Procurement Items": len(project["procurement_items"])
        }
        data.append(project_data)

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Project Data as CSV",
        data=csv,
        file_name="project_data.csv",
        mime="text/csv"
    )


# Main app
st.title("Project Management and Bidding System")

menu = ["Add Project", "Add Bid", "Manage Procurement", "View Projects", "Download Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Project":
    add_project()
elif choice == "Add Bid":
    add_bid()
elif choice == "Manage Procurement":
    manage_procurement()
elif choice == "View Projects":
    view_projects()
elif choice == "Download Data":
    download_csv()
