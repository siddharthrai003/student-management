import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

# Page title
st.title("🎓 Student Record Management System")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add Student")

    id = st.number_input("Student ID", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, step=1)
    course = st.text_input("Course")

    if st.button("Add Student"):
        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (id, name, age, course)
            )
            conn.commit()
            st.success("Student Added Successfully!")
        except sqlite3.IntegrityError:
            st.error("Student ID already exists!")


# READ
elif menu == "View Students":
    st.header("Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)

    st.dataframe(df, use_container_width=True)


# UPDATE
elif menu == "Update Student":
    st.header("Update Student")

    id = st.number_input("Enter Student ID", min_value=1, step=1)
    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=1, step=1)
    course = st.text_input("New Course")

    if st.button("Update Student"):
        cursor.execute(
            "UPDATE students SET name=?, age=?, course=? WHERE id=?",
            (name, age, course, id)
        )
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student Updated Successfully!")
        else:
            st.error("Student Not Found!")


# DELETE
elif menu == "Delete Student":
    st.header("Delete Student")

    id = st.number_input("Enter Student ID", min_value=1, step=1)

    if st.button("Delete Student"):
        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student Deleted Successfully!")
        else:
            st.error("Student Not Found!")

conn.close()