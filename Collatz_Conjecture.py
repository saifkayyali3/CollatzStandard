import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd 
import matplotlib.pyplot as mat

# Global variable to store the last computed sequence
last_sequence = []

# Parsing Function
def parse_collatz(val):
    val = val.replace(" ", "").lower()
    try:
        # Handle 2.7*10^64 style
        if "*10^" in val:
            base, exp = val.split("*10^")
            return int(float(base) * (10 ** int(exp)))
        # Handle exponentiation like 2**64 or 2.7*10**64
        elif "**" in val:
            base, exp = val.split("**")
            if "*10" in base:
                base_num = float(base.replace("*10", ""))
                return int(base_num * (10 ** int(exp)))
            else:
                return int(float(base) ** int(exp))
        # Handle simple exponentiation like 2^64
        elif "^" in val:
            base, exp = val.split("^")
            return int(float(base) ** int(exp))
        # Handle scientific notation like 2e64
        elif "e" in val:
            return int(float(val))
        # Plain numbers
        else:
            return int(float(val))
    except (ValueError, IndexError, OverflowError):
        return None
# Collatz Sequence Simulation
def collatz():
    global last_sequence 
    try:
        n = parse_collatz(inpt.get())
        if n is None or n <= 0:
            result.config(state=tk.NORMAL)
            result.delete(1.0, tk.END)
            result.insert(tk.END, "Error: Enter a positive integer and make it not larger than your RAM can handle")
            result.config(state=tk.DISABLED)
            btn_export.pack_forget()
            btn_visualize.pack_forget()
            return
        last_sequence = [n]
        while n != 1:
            if n % 2 == 0: n //= 2
            else: n = 3 * n + 1
            last_sequence.append(n)
        
        # Check the actual number of steps in the list
        if len(last_sequence) >= 200 or max(last_sequence) > 1e18: 
             result.config(state=tk.NORMAL)
             result.delete(1.0, tk.END)
             result.insert(tk.END, f"Steps: {len(last_sequence)} | Max Value: {max(last_sequence)} \nSequence too long to display (Export for details).")
             result.config(state=tk.DISABLED)
        else:
             sequence_str = ", ".join(map(str, last_sequence))
             result.config(state=tk.NORMAL)
             result.delete(1.0, tk.END)
             result.insert(tk.END, f"Steps: {len(last_sequence)} | Max Value: {max(last_sequence)} \nSequence: {sequence_str}")
             result.config(state=tk.DISABLED)
        btn_export.pack(pady=5)
        btn_visualize.pack(pady=5)
    except ValueError:
        pass

# Visualization function
def visualize_graph():
    mat.close('all')
    global last_sequence
    if not last_sequence:
        return
    starting_number = last_sequence[0]
    

    is_massive = max(last_sequence) > 1e18

    fig, ax = mat.subplots()
    manager = fig.canvas.manager
    try:
        manager.window.state('zoomed')          # Windows
    except AttributeError:
        try:
            manager.full_screen_toggle()        # macOS/Linux fallback
        except AttributeError:
            pass
    if is_massive:
       ax.plot(last_sequence, color='royalblue', linewidth=1)
       ax.set_yscale('log')
       ax.set_ylabel("Value (log₁₀ scale)")
       ax.set_title(f"Collatz Path for {starting_number}\n(Logarithmic Scale)\nNote: display starts from highest number in sequence for convenience", pad=20)
    else:
        ax.plot(last_sequence, marker='o', linestyle='-', color='royalblue')
        ax.set_ylabel("Value")
        ax.set_title(f"Collatz Sequence for {starting_number}", pad=20)

    mat.xlabel("Steps")
    mat.grid(True, linestyle='--', alpha=0.7)

    if not is_massive:
        import matplotlib.ticker as ticker
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True) 
        formatter.set_powerlimits((-3, 4)) 
        ax.yaxis.set_major_formatter(formatter)
    
    mat.show()
    btn_visualize.pack_forget()
    btn_export.pack_forget()
    result.config(state=tk.NORMAL)
    result.delete(1.0, tk.END)
    result.insert(tk.END, "Graph closed. Enter a new number to start again!")
    result.config(state=tk.DISABLED)
    last_sequence = [] 
    inpt.delete(0, tk.END)
# Export to CSV function
def export_csv():
    if not last_sequence:
        messagebox.showwarning("No Data", "Please click Submit first to generate a sequence!")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if filepath:
        df = pd.DataFrame({"Step": range(len(last_sequence)), "Value": last_sequence})
        df.to_csv(filepath, index=False)
        result.config(text="Data exported successfully!", bg="lime")

# UI Setup
root=tk.Tk()
root.geometry("600x500")
root.title("Collatz Conjecture Visualizer")
root.config(bg="turquoise")
lbl=tk.Label(root,text="Collatz Conjecture Visualizer", font=("Times", 16, "bold"), bg="turquoise", fg="black")
lbl.pack(pady=10)
lbl_1=tk.Label(root,text="Enter a number and click Submit\nStandard form and Exponential form are allowed", bg="turquoise", fg="black")
lbl_1.pack()
lbl_2=tk.Label(root,text="Examples of valid inputs:\n27, 2.7e10, 2.7*10^10, 2**64, 2^64", bg="turquoise", fg="black")
lbl_2.pack()
note=tk.Label(root,text="Note: Very large numbers may not be precise, check README.md for more details", bg="turquoise", fg="red", font=("bold", 10))
note.pack()
warning=tk.Label(root,text="WARNING: Don't enter numbers larger than your RAM can handle!", bg="turquoise", fg="red")
warning.pack()
inpt=tk.Entry(root)
inpt.pack()
btn=tk.Button(root,text="Submit",command=collatz, bg="royal blue",fg="black")
btn.pack()
result=scrolledtext.ScrolledText(root,height=10, width=80, state=tk.DISABLED, wrap=tk.WORD, font=("Times", 12))
result.pack()
btn_export = tk.Button(root, text="Export CSV", command=export_csv, bg="forest green", fg="white")
btn_visualize = tk.Button(root, text="Visualize Graph", command=visualize_graph, bg="dark orange", fg="white")
root.mainloop()