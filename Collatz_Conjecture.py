import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd 
import matplotlib.pyplot as mat

last_sequence = []

def collatz():
    global last_sequence 
    try:
        n = int(inpt.get())
        if n <= 0:
            result.config(text="Error: Enter a positive integer (> 0).", bg="black", fg="red")
            btn_export.pack_forget()
            btn_visualize.pack_forget()
            return
        last_sequence = [n]
        while n != 1:
            if n % 2 == 0: n //= 2
            else: n = 3 * n + 1
            last_sequence.append(n)
        sequence_str = ", ".join(map(str, last_sequence))
        
        # Display summary to user
        result.config(text=f"Steps: {len(last_sequence)} | Max Value: {max(last_sequence)} \n Collatz Sequence: {sequence_str}", bg="tomato", fg="black")
        btn_export.pack(pady=5)
        btn_visualize.pack(pady=5)
    except ValueError:
        result.config(text="Please enter a valid integer.", bg="black", fg="red")
        btn_export.pack_forget()
        btn_visualize.pack_forget()


def visualize_graph():
    global last_sequence
    if not last_sequence:
        return
    
    
    mat.figure(figsize=(8, 5))
    mat.plot(last_sequence, marker='o', linestyle='-', color='royalblue')
    mat.title(f"Collatz Sequence for {last_sequence[0]}")
    mat.xlabel("Steps")
    mat.ylabel("Value")
    mat.grid(True, linestyle='--', alpha=0.7)

    import matplotlib.ticker as ticker
    ax = mat.gca() # Get the current axes to apply formatting
    formatter = ticker.ScalarFormatter(useMathText=True) # Enable scientific notation
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-3, 4)) # Triggers sci-notation for numbers > 10,000
    ax.yaxis.set_major_formatter(formatter)
    
    mat.show()
    btn_visualize.pack_forget()
    btn_export.pack_forget()
    result.config(text="Graph closed. Enter a new number to start again!", bg="turquoise")
    last_sequence = [] # Clear the data so it's ready for a fresh start
    inpt.delete(0, tk.END)
def export_csv():
    if not last_sequence:
        messagebox.showwarning("No Data", "Please click Submit first to generate a sequence!")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if filepath:
        df = pd.DataFrame({"Step": range(len(last_sequence)), "Value": last_sequence})
        df.to_csv(filepath, index=False)
        result.config(text="Data exported successfully!", bg="lime")


root=tk.Tk()
root.geometry("600x500")
root.title("Collatz Conjecture Visualizer")
root.config(bg="turquoise")
lbl=tk.Label(root,text="Enter a number and click Submit", bg="turquoise", fg="black")
lbl.pack()
inpt=tk.Entry(root)
inpt.pack()
btn=tk.Button(root,text="Submit",command=collatz, bg="royal blue",fg="black")
btn.pack()
result=tk.Label(root,text="",bg="turquoise", wraplength=580)
result.pack()
btn_export = tk.Button(root, text="Export CSV", command=export_csv, bg="forest green", fg="white")
btn_visualize = tk.Button(root, text="Visualize Graph", command=visualize_graph, bg="dark orange", fg="white")
root.mainloop()