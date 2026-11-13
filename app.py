
import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")
st.write("Manage Student Records Easily")

# CSV file
FILE = "students.csv"

# Load existing data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "Roll No", "Name", "Age", "Course", "Marks"
    ])

# Sidebar menu
st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Search Student",
     "Update Student", "Delete Student"]
)

# ADD STUDENT
if menu == "Add Student":

    st.subheader("Add New Student")

    with st.form("add_student_form"):

        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

        submit = st.form_submit_button("Add Student")

        if submit:

            if name.strip() == "" or course.strip() == "":
                st.error("Please enter all student details.")

            elif roll in df["Roll No"].values:
                st.error("Roll Number already exists!")

            else:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                df = pd.concat([df, new_student], ignore_index=True)
                df.to_csv(FILE, index=False)

                st.success("Student added successfully!")

# VIEW STUDENTS
elif menu == "View Students":

    st.subheader("All Student Records")

    if df.empty:
        st.warning("No student records found.")

    else:
        st.dataframe(df, use_container_width=True)

        st.write("Total Students:", len(df))
        st.write("Average Marks:", round(df["Marks"].mean(), 2))

# SEARCH STUDENT
elif menu == "Search Student":

    st.subheader("Search Student")

    roll = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Search"):

        result = df[df["Roll No"] == roll]

        if not result.empty:
            st.success("Student Found!")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("Student Not Found!")

# UPDATE STUDENT
elif menu == "Update Student":

    st.subheader("Update Student Details")

    roll = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Find Student"):

        result = df[df["Roll No"] == roll]

        if not result.empty:

            st.session_state["edit_student"] = result.iloc[0].to_dict()
        else:
            st.error("Student Not Found!")

    if "edit_student" in st.session_state:

        student = st.session_state["edit_student"]

        with st.form("update_form"):

            name = st.text_input("Name", value=str(student["Name"]))
            age = st.number_input("Age", min_value=1, max_value=100,
                                  value=int(student["Age"]))
            course = st.text_input("Course", value=str(student["Course"]))
            marks = st.number_input("Marks", min_value=0.0,
                                    max_value=100.0,
                                    value=float(student["Marks"]))

            update = st.form_submit_button("Update Student")

            if update:

                df.loc[df["Roll No"] == roll, "Name"] = name
                df.loc[df["Roll No"] == roll, "Age"] = age
                df.loc[df["Roll No"] == roll, "Course"] = course
                df.loc[df["Roll No"] == roll, "Marks"] = marks

                df.to_csv(FILE, index=False)

                del st.session_state["edit_student"]

                st.success("Student Updated Successfully!")
                st.rerun()

# DELETE STUDENT
elif menu == "Delete Student":

    st.subheader("Delete Student Record")

    roll = st.number_input("Enter Roll Number", min_value=1, step=1)

    if st.button("Delete Student"):

        if roll in df["Roll No"].values:

            df = df[df["Roll No"] != roll]

            df.to_csv(FILE, index=False)

            st.success("Student Deleted Successfully!")

        else:
            st.error("Student Not Found!")
