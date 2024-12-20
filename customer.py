import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Function to open customer management window
def open_customer_window(main_frame):
    clear_frame(main_frame)

    # Title Label
    customer_label = tk.Label(main_frame, text="Customer Management", font=("Arial", 24))
    customer_label.pack(pady=10)

    # Search bar label and entry
    tk.Label(main_frame, text="Search:", font=("Arial", 14)).pack(pady=5)
    search_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
    search_entry.pack(pady=5)

    # Treeview style and font size
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    # Treeview to display customer data
    customer_tree = ttk.Treeview(main_frame, columns=("Internal ID", "Customer ID", "Name", "City", "Shop"), show='headings', height=8)
    customer_tree.heading("Internal ID", text="Internal ID", anchor=tk.W)
    customer_tree.heading("Customer ID", text="Customer ID", anchor=tk.W)
    customer_tree.heading("Name", text="Customer Name", anchor=tk.W)
    customer_tree.heading("City", text="City", anchor=tk.W)
    customer_tree.heading("Shop", text="Shop", anchor=tk.W)

    # Set increased column widths
    customer_tree.column("Internal ID", width=150)  # Increased width
    customer_tree.column("Customer ID", width=200)  # Increased width
    customer_tree.column("Name", width=250)         # Increased width
    customer_tree.column("City", width=200)         # Increased width
    customer_tree.column("Shop", width=200)         # Increased width

    customer_tree.pack(pady=20)

    # Function to refresh the table based on the search query
    def refresh_customer_table(search_query=None):
        # Clear the Treeview
        for row in customer_tree.get_children():
            customer_tree.delete(row)

        # Fetch customers from the database, filter if search_query is provided
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()

        if search_query:
            # Search query: filter by customer_id, name, city, or shop
            query = f"%{search_query}%"
            c.execute("SELECT internal_id, customer_id, name, city, shop FROM customers WHERE customer_id LIKE ? OR name LIKE ? OR city LIKE ? OR shop LIKE ?",
                      (query, query, query, query))
        else:
            c.execute("SELECT internal_id, customer_id, name, city, shop FROM customers")

        rows = c.fetchall()

        # Insert data into the Treeview
        for row in rows:
            customer_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))

        conn.close()

    # Function to show popup for action buttons
    def show_popup(event):
        # Get selected item
        selected_item = customer_tree.selection()

        if selected_item:
            selected = customer_tree.item(selected_item)
            internal_id = selected['values'][0]

            # Create a popup menu
            popup = tk.Menu(main_frame, tearoff=0)
            popup.add_command(label="Edit", command=lambda: update_customer(internal_id))
            popup.add_command(label="Delete", command=lambda: delete_customer(internal_id))
            popup.post(event.x_root, event.y_root)

    # Function to handle updating a customer
    def update_customer(internal_id):
        clear_frame(main_frame)

        # Fetch existing customer data
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT customer_id, name, city, shop FROM customers WHERE internal_id=?", (internal_id,))
        customer_data = c.fetchone()
        conn.close()

        # Show form pre-filled with existing customer data
        tk.Label(main_frame, text="Update Customer", font=("Arial", 24)).pack(pady=10)

        tk.Label(main_frame, text="Customer ID", font=("Arial", 16)).pack(pady=5)
        customer_id_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_id_entry.pack(pady=5)
        customer_id_entry.insert(0, customer_data[0])

        tk.Label(main_frame, text="Customer Name", font=("Arial", 16)).pack(pady=5)
        customer_name_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_name_entry.pack(pady=5)
        customer_name_entry.insert(0, customer_data[1])

        tk.Label(main_frame, text="City", font=("Arial", 16)).pack(pady=5)
        customer_city_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_city_entry.pack(pady=5)
        customer_city_entry.insert(0, customer_data[2])

        tk.Label(main_frame, text="Shop", font=("Arial", 16)).pack(pady=5)
        customer_shop_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_shop_entry.pack(pady=5)
        customer_shop_entry.insert(0, customer_data[3])

        def save_updated_customer():
            customer_id = customer_id_entry.get()
            customer_name = customer_name_entry.get()
            city = customer_city_entry.get()
            shop = customer_shop_entry.get()

            if customer_id and customer_name and city and shop:
                conn = sqlite3.connect('db/factory.db')
                c = conn.cursor()
                c.execute("UPDATE customers SET customer_id=?, name=?, city=?, shop=? WHERE internal_id=?",
                          (customer_id, customer_name, city, shop, internal_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Customer updated successfully!")
                open_customer_window(main_frame)  # Go back to customer list page and refresh table
            else:
                messagebox.showwarning("Input Error", "Please fill out all fields.")

        submit_button = tk.Button(main_frame, text="Update Customer", font=("Arial", 14), command=save_updated_customer)
        submit_button.pack(pady=10)

    # Function to delete a customer
    def delete_customer(internal_id):
        result = messagebox.askyesno("Delete Customer", "Are you sure you want to delete this customer?")
        if result:
            conn = sqlite3.connect('db/factory.db')
            c = conn.cursor()
            c.execute("DELETE FROM customers WHERE internal_id=?", (internal_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer deleted successfully!")
            refresh_customer_table()

    # Bind right-click to show the popup for Edit and Delete actions
    customer_tree.bind("<Button-3>", show_popup)

    # Function to handle search input changes
    def on_search_key_release(event):
        search_query = search_entry.get()
        refresh_customer_table(search_query)

    # Bind search entry to key release event
    search_entry.bind('<KeyRelease>', on_search_key_release)

    # Initially refresh the table to show all customers
    refresh_customer_table()

    # Function to open the add customer form
    def open_add_customer_form():
        clear_frame(main_frame)

        # Customer form labels and entries
        tk.Label(main_frame, text="Customer ID", font=("Arial", 16)).pack(pady=5)
        customer_id_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_id_entry.pack(pady=5)

        tk.Label(main_frame, text="Customer Name", font=("Arial", 16)).pack(pady=5)
        customer_name_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_name_entry.pack(pady=5)

        tk.Label(main_frame, text="City", font=("Arial", 16)).pack(pady=5)
        customer_city_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_city_entry.pack(pady=5)

        tk.Label(main_frame, text="Shop", font=("Arial", 16)).pack(pady=5)
        customer_shop_entry = tk.Entry(main_frame, font=("Arial", 14), width=30)
        customer_shop_entry.pack(pady=5)

        # Add customer button (inside form)
        submit_button = tk.Button(main_frame, text="Submit Customer", font=("Arial", 14), command=lambda: add_customer(customer_id_entry, customer_name_entry, customer_city_entry, customer_shop_entry))
        submit_button.pack(pady=10)

    # Function to add a customer to the database
    def add_customer(customer_id_entry, customer_name_entry, customer_city_entry, customer_shop_entry):
        customer_id = customer_id_entry.get()
        customer_name = customer_name_entry.get()
        city = customer_city_entry.get()
        shop = customer_shop_entry.get()

        if customer_id and customer_name and city and shop:
            try:
                conn = sqlite3.connect('db/factory.db')
                c = conn.cursor()
                c.execute("INSERT INTO customers (customer_id, name, city, shop) VALUES (?, ?, ?, ?)",
                          (customer_id, customer_name, city, shop))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Customer added successfully!")
                open_customer_window(main_frame)  # Go back to customer list page and refresh table
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Customer ID already exists! Please enter a unique Customer ID.")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    # Add customer button to open the add customer form
    add_customer_button = tk.Button(main_frame, text="Add Customer", font=("Arial", 14), command=open_add_customer_form)
    add_customer_button.pack(pady=10)

# Function to clear the current frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
