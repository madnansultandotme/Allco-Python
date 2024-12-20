import tkinter as tk
from customer import open_customer_window
from item import open_items_window
from profit import open_profit_window
from expenses import open_expenses_window
from sale import open_sale_window
from dashboard import open_dashboard_window  # Import the dashboard function

# function to display the dashboard page
def show_dashboard():
    clear_frame()
    open_dashboard_window(main_frame)  # Call the dashboard function

# function to clear the current frame for new content
def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# function to show a specific screen and hide the others
def show_screen(screen_func):
    clear_frame()
    screen_func()  # display the selected screen

# setup main application window
root = tk.Tk()
root.title("Factory Dashboard")
root.geometry("1000x800")

# menu bar using frame with buttons
menu_frame = tk.Frame(root, bg="lightgrey")
menu_frame.pack(side=tk.TOP, fill=tk.X)

button_font = ("Arial", 14)  # font size for menu buttons

# menu buttons
dashboard_button = tk.Button(menu_frame, text="Dashboard", font=button_font, width=12, command=show_dashboard)
dashboard_button.pack(side=tk.LEFT, padx=5, pady=5)

customer_button = tk.Button(menu_frame, text="Customer", font=button_font, width=12, command=lambda: show_screen(lambda: open_customer_window(main_frame)))
customer_button.pack(side=tk.LEFT, padx=5, pady=5)

items_button = tk.Button(menu_frame, text="Items", font=button_font, width=12, command=lambda: show_screen(lambda: open_items_window(main_frame)))
items_button.pack(side=tk.LEFT, padx=5, pady=5)

profit_button = tk.Button(menu_frame, text="Profit", font=button_font, width=12, command=lambda: show_screen(lambda: open_profit_window(main_frame)))
profit_button.pack(side=tk.LEFT, padx=5, pady=5)

expenses_button = tk.Button(menu_frame, text="Expenses", font=button_font, width=12, command=lambda: show_screen(lambda: open_expenses_window(main_frame)))
expenses_button.pack(side=tk.LEFT, padx=5, pady=5)

sales_button = tk.Button(menu_frame, text="Sales", font=button_font, width=12, command=lambda: show_screen(lambda: open_sale_window(main_frame)))
sales_button.pack(side=tk.LEFT, padx=5, pady=5)

# main content area
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# display default dashboard page
show_dashboard()

# run the tkinter main loop
root.mainloop()
