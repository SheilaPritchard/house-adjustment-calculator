from fpdf import FPDF
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import Image, filedialog
from PIL import Image, ImageTk

# Create the main Tkinter window
root = tk.Tk()
root.geometry("1100x500")

#Changes tkinter window icon
try:  
    photo = ImageTk.PhotoImage(file="C:\\Users\\sepri\\OneDrive\Pictures\Saved Pictures\download_icon1.png")
    root.iconphoto(False, photo) 

except FileNotFoundError:
    print("Icon file not found, using default icon")

# Create a frame with a green border
border_frame = tk.Frame(root, bg="Teal", bd=10, relief="solid")
border_frame.grid(row=0, column=0, sticky="nsew")

# Allow window expansion
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Center the border_frame in the window
border_frame.grid_columnconfigure(0, weight=1)

# This avoids the error of an undefined variable if the user closes the window without opening a CSV file.
results_text = ""
df = None

# Placed above other code in hopes it will make label_result defined in code.
label_results = tk.Label(border_frame, text="", bg="AliceBlue", justify="left", anchor="center")
label_results.grid(row=2, column=0, padx=10, pady=10)

def display_results():
    global df, results_text

    if df is None:
        return

    # Filters only closed sales
    sales = df[df["Status"] == "Closed"].copy()

    # Convert ClosePrice, SqFtTotal, and other relevant columns to numeric
    numeric_cols = ["ClosePrice", "SqFtTotal", "BathsFull", "GarageCapacity", "BedsTotal"]

    for col in numeric_cols:
        sales[col] = pd.to_numeric(sales[col], errors="coerce")

    # Drop rows missing required values
    sales = sales.dropna(subset=numeric_cols)

    if len(sales) == 0:
        results_text = "No closed sales found."
        label_results.config(text=results_text)
        return

    median_price = sales["ClosePrice"].median()
    median_sqft = sales["SqFtTotal"].median()
    median_bath = sales["BathsFull"].median()
    median_garage = sales["GarageCapacity"].median()
    median_beds = sales["BedsTotal"].median()

    # Linear regression (polynomial of degree 1 for a straight line)
    # m variables are reference to slopes 
    m1 = np.polyfit(sales["SqFtTotal"], sales["ClosePrice"], 1)[0]
    m2 = np.polyfit(sales["BathsFull"], sales["ClosePrice"], 1)[0]
    m3 = np.polyfit(sales["GarageCapacity"], sales["ClosePrice"], 1)[0]
    m4 = np.polyfit(sales["BedsTotal"], sales["ClosePrice"], 1)[0]

    # Display results in Tkinter
    results_text = (
        f"Median Close Price: {median_price:,.0f}\n"
        f"Median SqFtTotal: {median_sqft:,.0f}\n"
        f"Median BathsFull: {median_bath}\n"
        f"Median GarageCapacity: {median_garage}\n"
        f"Median BedsTotal: {median_beds}\n"
        f"Closed Price Adjustment: {m1:,.2f}\n"
        f"Full Baths Adjustment: {m2:,.0f}\n"
        f"Garage Capacity Adjustment: {m3:,.0f}\n"
        f"Beds Total Adjustment: {m4:,.0f}"
    )

    label_results.config(text=results_text)

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

    # Displays results in the window
    display_results()

# Generate a PDF
def create_pdf():
    global results_text
    if not results_text:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in results_text.split("\n"):
        pdf.cell(0, 10, txt=line, ln=True)

    pdf.output("results.pdf")

    print("PDF created: results.pdf")

def exit_no():
    # Exits if user clicks no
    root.destroy()

# Button to open CSV file
open_button = tk.Button(border_frame, text="Open CSV File", bg="AliceBlue", command=open_file)
open_button.grid(row=0, column=0, padx=10, pady=10)

# Label to show which CSV file was opened
label_opened = tk.Label(border_frame, text="CSV File Opened: None", bg="AliceBlue")
label_opened.grid(row=1, column=0, padx=10, pady=10)

pdf_question = tk.Label(border_frame, text="Would you like to create a PDF of the results?")
pdf_question.grid(row=3, column=0, padx=10, pady=10)

yes_button = tk.Button(border_frame, text="Yes", command=create_pdf)
yes_button.grid(row=4, column=0, padx=10, pady=10)

no_button = tk.Button(border_frame, text="No", command=exit_no)
no_button.grid(row=5, column=0, padx=10, pady=10)

# Exit button
button_exit = tk.Button(border_frame, text="Exit", command=root.destroy)
button_exit.grid(row=6, column=0, padx=10, pady=10)

root.mainloop()