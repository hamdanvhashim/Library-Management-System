
# IMPORTING LIBRARIES

import streamlit as st
import json
import os


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# THEME MANAGEMENT

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


# THEME BUTTONS

st.sidebar.title("🎨 Appearance")

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("☀️ Light", use_container_width=True):
        st.session_state.theme = "Light"

with col2:
    if st.button("🌙 Dark", use_container_width=True):
        st.session_state.theme = "Dark"


# APPLYING THEME

if st.session_state.theme == "Dark":

    st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
    }

    [data-testid="stMetric"] {
        background-color: #252525;
        padding: 20px;
        border-radius: 12px;
    }

    h1, h2, h3, p, label {
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7fb;
        color: #1e293b;
    }

    [data-testid="stSidebar"] {
        background-color: #e8eef7;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dbe3ef;
    }

    h1, h2, h3, p {
        color: #1e293b;
    }

    </style>
    """, unsafe_allow_html=True)


# JSON FILE HANDLING

FILE_NAME = "library.json"


def load_data():

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:
            return json.load(file)

    else:

        return {
            "books": [],
            "issued_books": []
        }


def save_data(data):

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


data = load_data()


# APPLICATION TITLE

st.title("📚 Library Management System")

st.caption("A smarter and simpler way to manage your library")

st.sidebar.title("📚 Navigation")


# NAVIGATION BUTTONS

menu_options = [
    "Dashboard",
    "Add Books",
    "View Books",
    "Search Books",
    "Issue Books",
    "Return Books",
    "Delete Books"
]

for option in menu_options:

    if st.sidebar.button(
        option,
        use_container_width=True,
        type="primary" if st.session_state.menu == option else "secondary"
    ):

        st.session_state.menu = option
        st.rerun()


menu = st.session_state.menu


# DASHBOARD

if menu == "Dashboard":

    st.header("🏠 Library Dashboard")

    st.write("Welcome to your Library Management System!")

    st.write(
        "Manage books, students and borrowing activities "
        "easily through one platform."
    )

    st.divider()

    total_books = sum(
        book["quantity"] for book in data["books"]
    )

    available_books = sum(
        book["available"] for book in data["books"]
    )

    issued_books = sum(
        book["quantity"] - book["available"]
        for book in data["books"]
    )

    total_titles = len(data["books"])

    # METRIC CARDS

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📚 Total Copies",
        total_books
    )

    col2.metric(
        "✅ Available Copies",
        available_books
    )

    col3.metric(
        "📖 Issued Copies",
        issued_books
    )

    col4.metric(
        "📑 Total Titles",
        total_titles
    )

    st.divider()

    # DASHBOARD INFORMATION

    st.subheader("📊 Library Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"📚 Your library contains {total_titles} different book titles."
        )

        st.success(
            f"✅ Currently, {available_books} book copies are available."
        )

    with col2:

        st.warning(
            f"📖 Currently, {issued_books} book copies are issued."
        )

        st.info(
            "💡 Use the navigation buttons to manage your library."
        )

    st.divider()

    st.subheader("🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("➕ Add New Book", use_container_width=True):

            st.session_state.menu = "Add Books"
            st.rerun()

    with col2:

        if st.button("📖 View All Books", use_container_width=True):

            st.session_state.menu = "View Books"
            st.rerun()

    with col3:

        if st.button("🔍 Search Books", use_container_width=True):

            st.session_state.menu = "Search Books"
            st.rerun()


# ADD BOOKS

elif menu == "Add Books":

    st.header("➕ Add New Book")

    categories = [
        "Fiction",
        "Non-Fiction",
        "Science",
        "Technology",
        "History",
        "Biography",
        "Mathematics",
        "Literature",
        "Computer Science",
        "Education",
        "Reference",
        "Other"
    ]

    with st.form("add_book_form"):

        book_id = st.number_input(
            "Book ID",
            min_value=1,
            step=1
        )

        title = st.text_input("Book Title")

        author = st.text_input("Author Name")

        category = st.selectbox(
            "Select Book Category",
            categories
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        submit = st.form_submit_button(
            "➕ Add Book",
            use_container_width=True
        )

        if submit:

            if not title or not author:

                st.error("Please fill all the fields.")

            elif any(
                book["id"] == book_id
                for book in data["books"]
            ):

                st.error("Book ID already exists.")

            else:

                new_book = {
                    "id": int(book_id),
                    "title": title,
                    "author": author,
                    "category": category,
                    "quantity": int(quantity),
                    "available": int(quantity)
                }

                data["books"].append(new_book)

                save_data(data)

                st.success("Book added successfully!")


# VIEW BOOKS

elif menu == "View Books":

    st.header("📚 All Library Books")

    if data["books"]:

        st.dataframe(
            data["books"],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("No books available.")


# SEARCH BOOKS

elif menu == "Search Books":

    st.header("🔍 Search Books")

    search = st.text_input(
        "Enter Book Title, Author or ID"
    )

    if search:

        results = []

        for book in data["books"]:

            if (
                search.lower() in book["title"].lower()
                or search.lower() in book["author"].lower()
                or search == str(book["id"])
            ):

                results.append(book)

        if results:

            st.success(f"{len(results)} matching book(s) found.")

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No matching books found.")


# ISSUE BOOKS

elif menu == "Issue Books":

    st.header("📖 Issue Books")

    available_books = [
        book for book in data["books"]
        if book["available"] > 0
    ]

    if available_books:

        with st.form("issue_form"):

            student_name = st.text_input("Student Name")

            student_id = st.text_input("Student ID")

            book_options = {
                f'{book["id"]} - {book["title"]}': book["id"]
                for book in available_books
            }

            selected_book = st.selectbox(
                "Select Book",
                list(book_options.keys())
            )

            submit = st.form_submit_button("📖 Issue Book")

            if submit:

                if not student_name or not student_id:

                    st.error("Please enter student details.")

                else:

                    book_id = book_options[selected_book]

                    for book in data["books"]:

                        if book["id"] == book_id:

                            book["available"] -= 1

                            data["issued_books"].append({

                                "student_name": student_name,

                                "student_id": student_id,

                                "book_id": book_id,

                                "book_title": book["title"]

                            })

                            save_data(data)

                            st.success("Book issued successfully!")

                            break

    else:

        st.warning("No books available for issuing.")


# RETURN BOOKS

elif menu == "Return Books":

    st.header("↩️ Return Books")

    if data["issued_books"]:

        selected = st.selectbox(
            "Select Issued Book",

            range(len(data["issued_books"])),

            format_func=lambda i:
            f'{data["issued_books"][i]["student_name"]} - '
            f'{data["issued_books"][i]["book_title"]}'
        )

        if st.button("↩️ Return Book"):

            returned_book = data["issued_books"].pop(selected)

            for book in data["books"]:

                if book["id"] == returned_book["book_id"]:

                    book["available"] += 1

                    break

            save_data(data)

            st.success("Book returned successfully!")

            st.rerun()

    else:

        st.warning("No issued books to return.")


# DELETE BOOKS

elif menu == "Delete Books":

    st.header("🗑️ Delete Books")

    if data["books"]:

        book_options = {
            f'{book["id"]} - {book["title"]}': book["id"]
            for book in data["books"]
        }

        selected_book = st.selectbox(
            "Select Book to Delete",
            list(book_options.keys())
        )

        if st.button("🗑️ Delete Book"):

            book_id = book_options[selected_book]

            issued = any(
                item["book_id"] == book_id
                for item in data["issued_books"]
            )

            if issued:

                st.error(
                    "Cannot delete this book because copies are currently issued."
                )

            else:

                data["books"] = [
                    book for book in data["books"]
                    if book["id"] != book_id
                ]

                save_data(data)

                st.success("Book deleted successfully!")

                st.rerun()

    else:

        st.warning("No books available to delete.")

