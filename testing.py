import pandas as pd 
import numpy as np 
import tkinter as tk
from tkinter import filedialog

def open_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return
    
    df = pd.read_csv(file_path)
    label_opened.config(text=f"CSV File Opened: {file_path}")

#Create the main Tkinter window
root = tk.Tk()
root.geometry("900x300")

#Button to open CSV file
open_button = tk.Button(root, text="Open CSV File", command=open_file).grid(row=0, column=0, padx=10, pady=10)

#Label to show which CSV file was opened
label_opened = tk.Label(root, text="CSV File Opened: None").grid(row=1, column=0, padx=10, pady=10)

#Exit button
button_exit = tk.Button(root, text = "Exit", command = exit).grid(row=2, column=0, padx=10, pady=10)

root.mainloop()