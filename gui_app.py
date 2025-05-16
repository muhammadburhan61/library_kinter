import tkinter as tk
from tkinter import messagebox, simpledialog
from library_tkinter.book_library import Book, EBook, Library, BookNotAvailableError

# Create an instance of Library
library = Library()

# Initialize the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")

# ====================== Event Handlers and Logic ======================

def toggle_ebook_fields():
    """
    Enable or disable download size entry based on checkbox.
    """
    if ebook_var.get():
        size_entry.config(state="normal")
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state="disabled")

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()
    is_ebook = ebook_var.get()
    size = size_entry.get().strip()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Download size required for eBooks.")
            return
        try:
            float(size)  # Validating size is numeric
        except ValueError:
            messagebox.showerror("Error", "Download size must be a number.")
            return
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added to the library.")
    update_book_list()
    clear_inputs()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed from library.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        listbox.delete(0, tk.END)
        if books:
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

def clear_inputs():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)
    ebook_var.set(False)
    toggle_ebook_fields()

# ====================== GUI Layout ======================

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Title:").grid(row=0, column=0, sticky="e")
title_entry = tk.Entry(frame, width=40)
title_entry.grid(row=0, column=1)

tk.Label(frame, text="Author:").grid(row=1, column=0, sticky="e")
author_entry = tk.Entry(frame, width=40)
author_entry.grid(row=1, column=1)

tk.Label(frame, text="ISBN:").grid(row=2, column=0, sticky="e")
isbn_entry = tk.Entry(frame, width=40)
isbn_entry.grid(row=2, column=1)

ebook_var = tk.BooleanVar()
ebook_checkbox = tk.Checkbutton(frame, text="eBook?", variable=ebook_var, command=toggle_ebook_fields)
ebook_checkbox.grid(row=3, column=1, sticky="w")

tk.Label(frame, text="Download Size (MB):").grid(row=4, column=0, sticky="e")
size_entry = tk.Entry(frame, width=20, state="disabled")
size_entry.grid(row=4, column=1, sticky="w")

button_frame = tk.Frame(root, pady=10)
button_frame.pack()

tk.Button(button_frame, text="Add Book", width=15, command=add_book).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Lend Book", width=15, command=lend_book).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Return Book", width=15, command=return_book).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Remove Book", width=15, command=remove_book).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="View by Author", width=15, command=view_books_by_author).grid(row=1, column=1, padx=5)

tk.Label(root, text="Library Inventory:", font=("Helvetica", 12, "bold")).pack(pady=5)
listbox = tk.Listbox(root, width=90, height=15)
listbox.pack(pady=10)

update_book_list()
root.mainloop()
