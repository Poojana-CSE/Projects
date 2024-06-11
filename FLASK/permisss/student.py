import tkinter as tk
from tkinter import messagebox
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.Permission
requests_collection = db.request

def check_status():
    request_number = request_entry.get()

    try:
        request_data = requests_collection.find_one({"request_number": int(request_number)})
        
        if request_data:
            status = request_data.get("status")
            if status:
                if status == "Approved":
                    requests_collection.delete_one({"request_number": int(request_number)})
                    messagebox.showinfo("Request Status", f"Request {request_number} was approved and has been removed.")
                else:
                    messagebox.showinfo("Request Status", f"Request {request_number} status: {status}")
            else:
                messagebox.showerror("Error", f"Status for Request {request_number} not found.")
        else:
            messagebox.showerror("Error", f"Request {request_number} not found.")
    except ValueError:
        messagebox.showerror("Error", "Invalid request number.")

root = tk.Tk()
root.title("Check Status")
root.configure(bg="#ADD8E6")

frame = tk.Frame(root, bg="#ADD8E6")
frame.pack(padx=20, pady=20)

request_label = tk.Label(frame, text="Enter Request Number:", bg="#ADD8E6", fg="black")
request_label.grid(row=0, column=0, sticky="e")

request_entry = tk.Entry(frame)
request_entry.grid(row=0, column=1, padx=5, pady=5)

status_button = tk.Button(frame, text="Check Status", command=check_status, bg="white", fg="black")
status_button.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()
