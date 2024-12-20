import tkinter as tk

#function to open profit overview window
def open_expenses_window():
    profit_window = tk.Toplevel()
    profit_window.title("Expense Overview")
    profit_window.geometry("400x300")

    tk.Label(profit_window, text="Profit Overview", font=("Arial", 20)).pack(pady=20)
    
    #add your profit overview logic here

# Test function to directly run the profit window
if __name__ == '__main__':
    root = tk.Tk()
    open_expenses_window()
    root.mainloop()
