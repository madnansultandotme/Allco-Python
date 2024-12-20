import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Function to open items management window
def open_items_window(main_frame):
    clear_frame(main_frame)

    # Title Label
    item_label = tk.Label(main_frame, text="Items Management", font=("Arial", 24))
    item_label.pack(pady=10)

    # Search bar label and entry
    tk.Label(main_frame, text="Search:", font=("Arial", 14)).pack(pady=5)
    search_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
    search_entry.pack(pady=5)

    # Treeview style and font size
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    # Treeview to display item data
    item_tree = ttk.Treeview(main_frame, columns=("Item ID", "Item Name", "Manufactured Price", "Sale Price", "Stock"), show='headings', height=8)
    item_tree.heading("Item ID", text="Item ID", anchor=tk.W)
    item_tree.heading("Item Name", text="Item Name", anchor=tk.W)
    item_tree.heading("Manufactured Price", text="Manufactured Price", anchor=tk.W)
    item_tree.heading("Sale Price", text="Sale Price", anchor=tk.W)
    item_tree.heading("Stock", text="Stock", anchor=tk.W)

    # Set increased column widths
    item_tree.column("Item ID", width=150)
    item_tree.column("Item Name", width=200)
    item_tree.column("Manufactured Price", width=200)
    item_tree.column("Sale Price", width=200)
    item_tree.column("Stock", width=150)

    item_tree.pack(pady=20)

    # Function to refresh the table based on the search query
    def refresh_item_table(search_query=None):
        # Clear the Treeview
        for row in item_tree.get_children():
            item_tree.delete(row)

        # Fetch items from the database, filter if search_query is provided
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()

        if search_query:
            # Search query: filter by item_id, name, or stock
            query = f"%{search_query}%"
            c.execute("SELECT item_id, item_name, manufactured_price, sale_price, stock FROM items WHERE item_id LIKE ? OR item_name LIKE ?",
                      (query, query))
        else:
            c.execute("SELECT item_id, item_name, manufactured_price, sale_price, stock FROM items")

        rows = c.fetchall()

        # Insert data into the Treeview
        for row in rows:
            item_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))

        conn.close()

    # Function to show popup for action buttons
    def show_popup(event):
        # Get selected item
        selected_item = item_tree.selection()

        if selected_item:
            selected = item_tree.item(selected_item)
            item_id = selected['values'][0]

            # Create a popup menu
            popup = tk.Menu(main_frame, tearoff=0)
            popup.add_command(label="Edit", command=lambda: update_item(item_id))
            popup.add_command(label="Delete", command=lambda: delete_item(item_id))
            popup.post(event.x_root, event.y_root)

    # Function to handle updating an item
    def update_item(item_id):
        clear_frame(main_frame)

        # Fetch existing item data
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT item_name, manufactured_price, sale_price, stock FROM items WHERE item_id=?", (item_id,))
        item_data = c.fetchone()
        conn.close()

        # Show form pre-filled with existing item data
        tk.Label(main_frame, text="Update Item", font=("Arial", 24)).pack(pady=10)

        tk.Label(main_frame, text="Item Name", font=("Arial", 16)).pack(pady=5)
        item_name_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        item_name_entry.pack(pady=5)
        item_name_entry.insert(0, item_data[0])

        tk.Label(main_frame, text="Manufactured Price", font=("Arial", 16)).pack(pady=5)
        manufactured_price_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        manufactured_price_entry.pack(pady=5)
        manufactured_price_entry.insert(0, item_data[1])

        tk.Label(main_frame, text="Sale Price", font=("Arial", 16)).pack(pady=5)
        sale_price_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        sale_price_entry.pack(pady=5)
        sale_price_entry.insert(0, item_data[2])

        tk.Label(main_frame, text="Stock", font=("Arial", 16)).pack(pady=5)
        stock_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        stock_entry.pack(pady=5)
        stock_entry.insert(0, item_data[3])

        def save_updated_item():
            item_name = item_name_entry.get()
            manufactured_price = manufactured_price_entry.get()
            sale_price = sale_price_entry.get()
            stock = stock_entry.get()

            if item_name and manufactured_price and sale_price and stock:
                conn = sqlite3.connect('db/factory.db')
                c = conn.cursor()
                c.execute("UPDATE items SET item_name=?, manufactured_price=?, sale_price=?, stock=? WHERE item_id=?",
                          (item_name, manufactured_price, sale_price, stock, item_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Item updated successfully!")
                open_items_window(main_frame)  # Go back to item list page and refresh table
            else:
                messagebox.showwarning("Input Error", "Please fill out all fields.")

        submit_button = tk.Button(main_frame, text="Update Item", font=("Arial", 14), command=save_updated_item)
        submit_button.pack(pady=10)

    # Function to delete an item
    def delete_item(item_id):
        result = messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?")
        if result:
            conn = sqlite3.connect('db/factory.db')
            c = conn.cursor()
            c.execute("DELETE FROM items WHERE item_id=?", (item_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Item deleted successfully!")
            refresh_item_table()

    # Bind right-click to show the popup for Edit and Delete actions
    item_tree.bind("<Button-3>", show_popup)

    # Function to handle search input changes
    def on_search_key_release(event):
        search_query = search_entry.get()
        refresh_item_table(search_query)

    # Bind search entry to key release event
    search_entry.bind('<KeyRelease>', on_search_key_release)

    # Initially refresh the table to show all items
    refresh_item_table()

    # Function to open the add item form
    def open_add_item_form():
        clear_frame(main_frame)

        # Item form labels and entries
        tk.Label(main_frame, text="Item ID", font=("Arial", 16)).pack(pady=5)
        item_id_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        item_id_entry.pack(pady=5)

        tk.Label(main_frame, text="Item Name", font=("Arial", 16)).pack(pady=5)
        item_name_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        item_name_entry.pack(pady=5)

        tk.Label(main_frame, text="Manufactured Price", font=("Arial", 16)).pack(pady=5)
        manufactured_price_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        manufactured_price_entry.pack(pady=5)

        tk.Label(main_frame, text="Sale Price", font=("Arial", 16)).pack(pady=5)
        sale_price_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        sale_price_entry.pack(pady=5)

        tk.Label(main_frame, text="Stock", font=("Arial", 16)).pack(pady=5)
        stock_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        stock_entry.pack(pady=5)

        # Add item button (inside form)
        submit_button = tk.Button(main_frame, text="Add Item", font=("Arial", 14), command=lambda: add_item(item_id_entry, item_name_entry, manufactured_price_entry, sale_price_entry, stock_entry))
        submit_button.pack(pady=10)

        # Back button
        back_button = tk.Button(main_frame, text="Back", font=("Arial", 14), command=lambda: open_items_window(main_frame))
        back_button.pack(pady=10)

    # Function to add an item to the database
    def add_item(item_id_entry, item_name_entry, manufactured_price_entry, sale_price_entry, stock_entry):
        item_id = item_id_entry.get()
        item_name = item_name_entry.get()
        manufactured_price = manufactured_price_entry.get()
        sale_price = sale_price_entry.get()
        stock = stock_entry.get()

        if item_id and item_name and manufactured_price and sale_price and stock:
            try:
                conn = sqlite3.connect('db/factory.db')
                c = conn.cursor()
                c.execute("INSERT INTO items (item_id, item_name, manufactured_price, sale_price, stock) VALUES (?, ?, ?, ?, ?)",
                          (item_id, item_name, manufactured_price, sale_price, stock))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Item added successfully!")
                open_items_window(main_frame)  # Go back to item list page and refresh table
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Item ID already exists! Please enter a unique Item ID.")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    # Add item button to open the add item form
    add_item_button = tk.Button(main_frame, text="Add Item", font=("Arial", 14), command=open_add_item_form)
    add_item_button.pack(pady=10)


# Function to clear the current frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
