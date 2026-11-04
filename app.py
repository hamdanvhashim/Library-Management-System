#Importing libraries


import streamlit as st
import json
import os




#Page configuration



st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


#json file handling


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




#application title and sidebar



st.title("📚 Library Management System")

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Select an Option",
    [
        "Dashboard",
        "Add Books",
        "View Books",
        "Search Books",
        "Issue Books",
        "Return Books",
        "Delete Books"
    ]
)



#Dashboard



if menu == "Dashboard":

    st.header("Library Dashboard")

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

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Books", total_books)

    col2.metric("Available Books", available_books)

    col3.metric("Issued Books", issued_books)

    st.subheader("Welcome to Library Management System")

    st.write(
        "Manage your library books, students and borrowing activities easily."
    )



#Adding books 


elif menu == "Add Books":

    st.header("Add New Book")

    with st.form("add_book_form"):

        book_id = st.number_input(
            "Book ID",
            min_value=1,
            step=1
        )

        title = st.text_input("Book Title")

        author = st.text_input("Author Name")

        category = st.text_input("Category")

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        submit = st.form_submit_button("Add Book")

        if submit:

            if not title or not author or not category:

                st.error("Please fill all the fields.")

            elif any(book["id"] == book_id for book in data["books"]):

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




#View books 



elif menu == "View Books":

    st.header("All Library Books")

    if data["books"]:

        st.dataframe(
            data["books"],
            use_container_width=True
        )

    else:

        st.warning("No books available.")



#Search books



elif menu == "Search Books":

    st.header("Search Books")

    search = st.text_input("Enter Book Title, Author or ID")

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

            st.dataframe(results, use_container_width=True)

        else:

            st.warning("No matching books found.")



#Issue books



elif menu == "Issue Books":

    st.header("Issue Books")

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

            submit = st.form_submit_button("Issue Book")

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





#Return books



elif menu == "Return Books":

    st.header("Return Books")

    if data["issued_books"]:

        for index, issued in enumerate(data["issued_books"]):

            st.write(
                f'{issued["student_name"]} - {issued["book_title"]}'
            )

        selected = st.selectbox(
            "Select Issued Book",
            range(len(data["issued_books"])),
            format_func=lambda i:
            f'{data["issued_books"][i]["student_name"]} - '
            f'{data["issued_books"][i]["book_title"]}'
        )

        if st.button("Return Book"):

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




#Delete books



elif menu == "Delete Books":

    st.header("Delete Books")

    if data["books"]:

        book_options = {
            f'{book["id"]} - {book["title"]}': book["id"]
            for book in data["books"]
        }

        selected_book = st.selectbox(
            "Select Book to Delete",
            list(book_options.keys())
        )

        if st.button("Delete Book"):

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