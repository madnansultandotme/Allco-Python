import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Function to open the dashboard and manage sales
def open_dashboard_window(main_frame):
    clear_frame(main_frame)

    # Create a frame for the "Sell Items" section
    sell_items_frame = tk.Frame(main_frame)
    sell_items_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    # Create a frame for the cart (on the left side)
    cart_frame = tk.Frame(main_frame)
    cart_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    # Title Label for "Sell Items"
    dashboard_label = tk.Label(sell_items_frame, text="Sell Items", font=("Arial", 24))
    dashboard_label.pack(pady=10)

    # List to hold the items in the cart
    cart = []

    # Function to refresh the cart
    def refresh_cart():
        # Clear the Treeview
        for row in cart_tree.get_children():
            cart_tree.delete(row)

        total_price = 0
        for idx, item in enumerate(cart):
            total_price += item['total_price']
            cart_tree.insert("", tk.END, values=(idx + 1, item['item_name'], item['quantity'], item['price'], item['total_price']))

        # Update total price label
        total_price_label.config(text=f"Total Price: Rs. {total_price:.2f}")

    # Fetch items from the database for the dropdown
    def get_items():
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT item_id, item_name FROM items")
        items = c.fetchall()
        conn.close()
        return items

    # Fetch customers from the database for the dropdown
    def get_customers():
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT customer_id, name FROM customers")
        customers = c.fetchall()
        conn.close()
        return customers

    # Function to add item to cart
    def add_to_cart():
        item_name = item_combobox.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if item_name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            quantity = int(quantity)
            price = float(price)
            total_price = quantity * price

            # Add to cart list
            cart.append({'item_name': item_name, 'quantity': quantity, 'price': price, 'total_price': total_price})
            refresh_cart()  # Refresh the cart display
        else:
            messagebox.showwarning("Input Error", "Please fill in valid quantity and price.")

    # Function to generate and store receipt
    def generate_receipt():
        if not cart:
            messagebox.showwarning("Cart Empty", "Please add items to the cart before generating a receipt.")
            return

        customer_name = customer_combobox.get()
        amount_paid = amount_paid_entry.get()

        if not customer_name:
            messagebox.showwarning("Customer Selection", "Please select a customer.")
            return

        if not amount_paid.replace('.', '', 1).isdigit():
            messagebox.showwarning("Invalid Amount", "Please enter a valid amount for payment.")
            return

        amount_paid = float(amount_paid)

        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()

        # Fetch customer details
        c.execute("SELECT customer_id FROM customers WHERE name=?", (customer_name,))
        customer_id = c.fetchone()[0]

        # Calculate total price
        total_price = sum(item['total_price'] for item in cart)
        balance = total_price - amount_paid

        # Store each item in the sales database
        for item in cart:
            c.execute("INSERT INTO sales (customer_id, item_name, quantity, price, total_price) VALUES (?, ?, ?, ?, ?)",
                      (customer_id, item['item_name'], item['quantity'], item['price'], item['total_price']))

        # Update customer's balance
        c.execute("UPDATE customers SET balance = balance + ? WHERE customer_id = ?", (balance, customer_id))

        conn.commit()
        conn.close()

        # Clear cart and display success message
        cart.clear()
        refresh_cart()
        messagebox.showinfo("Success", "Receipt generated and transaction recorded successfully!")

    # Item selection dropdown
    tk.Label(sell_items_frame, text="Select Item", font=("Arial", 16)).pack(pady=5)
    items = get_items()
    item_combobox = ttk.Combobox(sell_items_frame, font=("Arial", 14), values=[item[1] for item in items], state="readonly", width=30)
    item_combobox.pack(pady=5)

    # Quantity input
    tk.Label(sell_items_frame, text="Quantity", font=("Arial", 16)).pack(pady=5)
    quantity_entry = tk.Entry(sell_items_frame, font=("Arial", 14), width=30)
    quantity_entry.pack(pady=5)

    # Price input
    tk.Label(sell_items_frame, text="Price", font=("Arial", 16)).pack(pady=5)
    price_entry = tk.Entry(sell_items_frame, font=("Arial", 14), width=30)
    price_entry.pack(pady=5)

    # Add to cart button
    add_cart_button = tk.Button(sell_items_frame, text="Add to Cart", font=("Arial", 14), command=add_to_cart)
    add_cart_button.pack(pady=10)

    # Cart Treeview in the cart_frame
    cart_tree = ttk.Treeview(cart_frame, columns=("S.No", "Item Name", "Quantity", "Price", "Total Price"), show='headings', height=8)
    cart_tree.heading("S.No", text="S.No", anchor=tk.W)
    cart_tree.heading("Item Name", text="Item Name", anchor=tk.W)
    cart_tree.heading("Quantity", text="Quantity", anchor=tk.W)
    cart_tree.heading("Price", text="Price", anchor=tk.W)
    cart_tree.heading("Total Price", text="Total Price", anchor=tk.W)

    cart_tree.column("S.No", width=50)
    cart_tree.column("Item Name", width=200)
    cart_tree.column("Quantity", width=100)
    cart_tree.column("Price", width=100)
    cart_tree.column("Total Price", width=150)

    cart_tree.pack(pady=10)

    # Total price label in cart_frame
    total_price_label = tk.Label(cart_frame, text="Total Price: Rs. 0.00", font=("Arial", 16))
    total_price_label.pack(pady=10)

    # Customer selection dropdown in sell_items_frame
    tk.Label(sell_items_frame, text="Select Customer", font=("Arial", 16)).pack(pady=5)
    customers = get_customers()
    customer_combobox = ttk.Combobox(sell_items_frame, font=("Arial", 14), values=[customer[1] for customer in customers], state="readonly", width=30)
    customer_combobox.pack(pady=5)

    # Amount paid input in sell_items_frame
    tk.Label(sell_items_frame, text="Amount Paid", font=("Arial", 16)).pack(pady=5)
    amount_paid_entry = tk.Entry(sell_items_frame, font=("Arial", 14), width=30)
    amount_paid_entry.pack(pady=5)

    # Generate receipt button in sell_items_frame
    generate_receipt_button = tk.Button(sell_items_frame, text="Generate Receipt", font=("Arial", 14), command=generate_receipt)
    generate_receipt_button.pack(pady=10)

# Function to clear the current frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Database setup for sales and customers table (if needed)
def setup_database():
    conn = sqlite3.connect('db/factory.db')
    c = conn.cursor()
    
    # Create sales table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')

    conn.commit()
    conn.close()

# Call this function once when the application starts to ensure the tables exist
setup_database()
