import streamlit as st
import json
import os

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

FILE_NAME = "library.json"


# -------------------- JSON FILE HANDLING --------------------
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            st.error("Could not read library.json. Please check that it contains valid JSON.")
            data = {}
    else:
        data = {}

    data.setdefault("books", [])
    data.setdefault("issued_books", [])
    data.setdefault("authors", [])

    if not isinstance(data["authors"], list):
        data["authors"] = []

    # Add authors from books already saved in older versions of library.json.
    for book in data["books"]:
        author = str(book.get("author", "")).strip()
        if author and author not in data["authors"]:
            data["authors"].append(author)

    return data


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


data = load_data()


# -------------------- SESSION STATE --------------------
# Any old saved value (e.g. "Warm Beige") falls back to Light.
if st.session_state.get("theme") not in ("Light", "Dark"):
    st.session_state.theme = "Light"

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


# -------------------- FONTS + BUTTON SHAPE (both themes) --------------------
# Font order:
#   Headings, metric numbers, buttons -> Poppins
#   Body text, labels, inputs, tables -> Inter
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* Body text */
    .stApp, .stApp p, .stApp li, .stApp label, .stApp input,
    .stApp textarea, .stApp select,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stDataFrame"],
    .stApp [data-testid="stAlert"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }

    /* Headings: title > header > subheader */
    .stApp h1 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 2.2rem; }
    .stApp h2 { font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.6rem; }
    .stApp h3 { font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.25rem; }
    .stApp h4 { font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 1.05rem; }

    /* Metric numbers */
    .stApp [data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* Caption under the title */
    .stApp [data-testid="stCaptionContainer"] { font-size: 0.9rem; opacity: 0.8; }

    /* Short, compact buttons instead of long rectangles */
    div.stButton > button,
    div.stFormSubmitButton > button {
        width: auto;
        min-height: 0;
        padding: 0.35rem 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------- THEME BUTTONS --------------------
st.sidebar.title("🎨 Appearance")
theme_col1, theme_col2 = st.sidebar.columns(2)

with theme_col1:
    if st.button("☀️ Light"):
        st.session_state.theme = "Light"
        st.rerun()

with theme_col2:
    if st.button("🌙 Dark"):
        st.session_state.theme = "Dark"
        st.rerun()


# -------------------- APPLY THEME --------------------
# Light theme: black text, black buttons.
# Dark theme:  white text, white buttons.
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #1A1D24; }
        [data-testid="stMetric"] {
            background-color: #1F2430; border: 1px solid #2E3440;
            padding: 18px; border-radius: 12px;
        }

        /* White text */
        h1, h2, h3, h4, p, li, label, [data-testid="stCaptionContainer"],
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        div[data-baseweb="input"] input, div[data-baseweb="select"] > div,
        textarea { background-color: #1F2430; color: #FFFFFF; }

        /* White buttons with black text */
        div.stButton > button, div.stFormSubmitButton > button {
            background-color: #FFFFFF; color: #000000; border: 1px solid #FFFFFF;
        }
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            background-color: #D1D5DB; color: #000000; border-color: #D1D5DB;
        }
        div.stButton > button p, div.stFormSubmitButton > button p {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; }
        [data-testid="stSidebar"] { background-color: #F3F4F6; }
        [data-testid="stMetric"] {
            background-color: #F9FAFB; border: 1px solid #E5E7EB;
            padding: 18px; border-radius: 12px;
        }

        /* Black text */
        h1, h2, h3, h4, p, li, label, [data-testid="stCaptionContainer"],
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        div[data-baseweb="input"] input, div[data-baseweb="select"] > div,
        textarea { color: #000000; }

        /* Black buttons with white text */
        div.stButton > button, div.stFormSubmitButton > button {
            background-color: #000000; color: #FFFFFF; border: 1px solid #000000;
        }
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            background-color: #333333; color: #FFFFFF; border-color: #333333;
        }
        div.stButton > button p, div.stFormSubmitButton > button p {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# -------------------- APPLICATION TITLE --------------------
st.title("📚 Library Management System")
st.caption("A smarter and simpler way to manage your library")


# -------------------- NAVIGATION BUTTONS --------------------
st.sidebar.title("📚 Navigation")

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
        type="primary" if st.session_state.menu == option else "secondary"
    ):
        st.session_state.menu = option
        st.rerun()

menu = st.session_state.menu


# -------------------- DASHBOARD --------------------
if menu == "Dashboard":
    st.header("🏠 Library Dashboard")

    # ---------- QUICK ACTIONS (at the top) ----------
    st.subheader("🚀 Quick Actions")
    quick_actions = [
        ("➕ Add Book", "Add Books"),
        ("📖 View Books", "View Books"),
        ("🔍 Search", "Search Books"),
        ("📤 Issue", "Issue Books"),
        ("↩️ Return", "Return Books"),
    ]
    action_cols = st.columns(len(quick_actions))
    for col, (label, target) in zip(action_cols, quick_actions):
        with col:
            if st.button(label, key=f"quick_{target}"):
                st.session_state.menu = target
                st.rerun()

    st.divider()
    st.write("Welcome to your Library Management System!")
    st.write("Manage books and borrowing activities easily through one platform.")

    total_books = sum(int(book.get("quantity", 0)) for book in data["books"])
    available_count = sum(int(book.get("available", 0)) for book in data["books"])
    issued_count = sum(
        int(book.get("quantity", 0)) - int(book.get("available", 0))
        for book in data["books"]
    )
    total_titles = len(data["books"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Copies", total_books)
    col2.metric("✅ Available Copies", available_count)
    col3.metric("📖 Issued Copies", issued_count)
    col4.metric("📑 Total Titles", total_titles)

    st.divider()
    st.subheader("📊 Library Overview")
    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.info(f"📚 Your library contains {total_titles} different book titles.")
        st.success(f"✅ Currently, {available_count} book copies are available.")

    with info_col2:
        st.warning(f"📖 Currently, {issued_count} book copies are issued.")
        st.info(f"✍️ {len(data['authors'])} authors are saved in your library.")


# -------------------- ADD BOOKS --------------------
elif menu == "Add Books":
    st.header("➕ Add New Book")

    categories = [
        "Fiction", "Non-Fiction", "Science", "Technology", "History",
        "Biography", "Mathematics", "Literature", "Computer Science",
        "Education", "Reference", "Other"
    ]

    st.write("Enter the book details below.")

    # Previously saved author names appear in this dropdown.
    author_options = sorted(set(data["authors"]))
    add_author_option = "➕ Add a new author"
    author_options.append(add_author_option)

    author_choice = st.selectbox(
        "Select Author",
        author_options,
        key="author_choice"
    )

    if author_choice == add_author_option:
        author_name = st.text_input("Enter New Author Name", key="new_author_name")
    else:
        author_name = author_choice

    with st.form("add_book_form"):
        book_id = st.number_input("Book ID", min_value=1, step=1)
        title = st.text_input("Book Title")
        category = st.selectbox("Select Book Category", categories)
        quantity = st.number_input("Quantity", min_value=1, step=1)

        submit = st.form_submit_button("➕ Add Book")

        if submit:
            author_name = author_name.strip()

            if not title.strip() or not author_name:
                st.error("Please enter the book title and author name.")
            elif any(int(book["id"]) == int(book_id) for book in data["books"]):
                st.error("Book ID already exists. Please use a different ID.")
            else:
                new_book = {
                    "id": int(book_id),
                    "title": title.strip(),
                    "author": author_name,
                    "category": category,
                    "quantity": int(quantity),
                    "available": int(quantity)
                }

                data["books"].append(new_book)

                # Save each author once in library.json.
                if author_name not in data["authors"]:
                    data["authors"].append(author_name)

                save_data(data)
                st.success("Book added successfully!")
                st.rerun()


# -------------------- VIEW BOOKS --------------------
elif menu == "View Books":
    st.header("📚 All Library Books")

    if data["books"]:
        st.dataframe(data["books"], use_container_width=True, hide_index=True)
    else:
        st.warning("No books available. Add a book to get started.")


# -------------------- SEARCH BOOKS --------------------
elif menu == "Search Books":
    st.header("🔍 Search Books")
    search_text = st.text_input("Enter Book Title, Author or ID")

    if search_text:
        results = []
        for book in data["books"]:
            if (
                search_text.lower() in book["title"].lower()
                or search_text.lower() in book["author"].lower()
                or search_text == str(book["id"])
            ):
                results.append(book)

        if results:
            st.success(f"{len(results)} matching book(s) found.")
            st.dataframe(results, use_container_width=True, hide_index=True)
        else:
            st.warning("No matching books found.")


# -------------------- ISSUE BOOKS --------------------
elif menu == "Issue Books":
    st.header("📖 Issue Books")

    available_books = [
        book for book in data["books"]
        if int(book.get("available", 0)) > 0
    ]

    if available_books:
        book_options = {
            f'{book["id"]} - {book["title"]}': book["id"]
            for book in available_books
        }

        with st.form("issue_form"):
            student_name = st.text_input("Student Name")
            student_id = st.text_input("Student ID")
            selected_book = st.selectbox("Select Book", list(book_options.keys()))
            submit = st.form_submit_button("📖 Issue Book")

            if submit:
                if not student_name.strip() or not student_id.strip():
                    st.error("Please enter the student name and student ID.")
                else:
                    selected_id = book_options[selected_book]

                    for book in data["books"]:
                        if int(book["id"]) == int(selected_id):
                            book["available"] -= 1
                            data["issued_books"].append({
                                "student_name": student_name.strip(),
                                "student_id": student_id.strip(),
                                "book_id": int(selected_id),
                                "book_title": book["title"]
                            })
                            break

                    save_data(data)
                    st.success("Book issued successfully!")
                    st.rerun()
    else:
        st.warning("No books are currently available for issuing.")


# -------------------- RETURN BOOKS --------------------
elif menu == "Return Books":
    st.header("↩️ Return Books")

    if data["issued_books"]:
        selected_index = st.selectbox(
            "Select Issued Book",
            range(len(data["issued_books"])),
            format_func=lambda i: (
                f'{data["issued_books"][i]["student_name"]} - '
                f'{data["issued_books"][i]["book_title"]} '
                f'(Student ID: {data["issued_books"][i]["student_id"]})'
            )
        )

        if st.button("↩️ Return Book"):
            returned_book = data["issued_books"].pop(selected_index)

            for book in data["books"]:
                if int(book["id"]) == int(returned_book["book_id"]):
                    book["available"] += 1
                    break

            save_data(data)
            st.success("Book returned successfully!")
            st.rerun()
    else:
        st.warning("No issued books to return.")


# -------------------- DELETE BOOKS --------------------
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
            selected_id = book_options[selected_book]

            is_issued = any(
                int(item["book_id"]) == int(selected_id)
                for item in data["issued_books"]
            )

            if is_issued:
                st.error(
                    "This book cannot be deleted because a copy is currently issued."
                )
            else:
                data["books"] = [
                    book for book in data["books"]
                    if int(book["id"]) != int(selected_id)
                ]
                # Keep the author saved even if this book is deleted.
                save_data(data)
                st.success("Book deleted successfully!")
                st.rerun()
    else:
        st.warning("No books available to delete.")
