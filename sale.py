import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to open the sales overview window
def open_sale_window(main_frame):
    clear_frame(main_frame)

    # Title Label
    sale_label = tk.Label(main_frame, text="Sales Overview", font=("Arial", 24))
    sale_label.pack(pady=10)

    # Treeview to display sales transactions
    sales_tree = ttk.Treeview(main_frame, columns=("Sale ID", "Item Name", "Quantity", "Price (Rs.)", "Total Price (Rs.)", "Date"), show='headings', height=8)
    sales_tree.heading("Sale ID", text="Sale ID", anchor=tk.W)
    sales_tree.heading("Item Name", text="Item Name", anchor=tk.W)
    sales_tree.heading("Quantity", text="Quantity", anchor=tk.W)
    sales_tree.heading("Price (Rs.)", text="Price (Rs.)", anchor=tk.W)
    sales_tree.heading("Total Price (Rs.)", text="Total Price (Rs.)", anchor=tk.W)
    sales_tree.heading("Date", text="Date", anchor=tk.W)

    sales_tree.column("Sale ID", width=50)
    sales_tree.column("Item Name", width=150)
    sales_tree.column("Quantity", width=100)
    sales_tree.column("Price (Rs.)", width=100)
    sales_tree.column("Total Price (Rs.)", width=150)
    sales_tree.column("Date", width=150)

    sales_tree.pack(pady=20, fill=tk.BOTH, expand=True)  # Fill the space

    # Function to fetch and display daily transactions in the Treeview
    def refresh_sales_table():
        # Clear the Treeview
        for row in sales_tree.get_children():
            sales_tree.delete(row)

        # Fetch sales transactions from the database
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT sale_id, item_name, quantity, price, total_price, sale_date FROM sales WHERE date(sale_date) = date('now')")
        rows = c.fetchall()
        conn.close()

        # Insert data into the Treeview
        for row in rows:
            sales_tree.insert("", tk.END, values=(row[0], row[1], row[2], f"Rs. {row[3]:.2f}", f"Rs. {row[4]:.2f}", row[5]))

    # Function to plot sales graph based on days
    def plot_sales_graph():
        # Fetch sales data from the database
        conn = sqlite3.connect('db/factory.db')
        c = conn.cursor()
        c.execute("SELECT date(sale_date), SUM(total_price) FROM sales GROUP BY date(sale_date)")
        sales_data = c.fetchall()
        conn.close()

        # Prepare data for plotting
        dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in sales_data]
        total_sales = [row[1] for row in sales_data]

        # Plotting the vertical bar graph
        fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the size to fit the full screen width
        ax.bar(dates, total_sales, color='skyblue')  # Vertical bar graph
        ax.set_title("Daily Sales Overview")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Sales (Rs.)")

        # Format the date labels
        fig.autofmt_xdate()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

    # Display today's transactions
    refresh_sales_table()

    # Automatically plot the sales graph when the window opens
    plot_sales_graph()

# Function to clear the current frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Test function to directly run the sales window
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x800")  # Set the size to cover most of the screen
    open_sale_window(root)
    root.mainloop()
