import tkinter as tk
from tkinter import messagebox
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.Permission
requests_collection = db.request

def load_requests():
    requests = requests_collection.find()
    return list(requests)

def update_request_status(request_id, status):
    requests_collection.update_one({"_id": request_id}, {"$set": {"status": status}})

def teacher_view():
    def submit():
        for idx, var in enumerate(status_vars):
            if var.get() == 1:
                update_request_status(requests[idx]["_id"], "Approved")
            elif var.get() == 2:
                update_request_status(requests[idx]["_id"], "Not Approved")
        messagebox.showinfo("Success", "Requests updated successfully.")
        teacher_window.destroy()
        teacher_view()

    teacher_window = tk.Tk()
    teacher_window.title("Teacher View")
    teacher_window.geometry("600x600")

    requests = load_requests()
    status_vars = []

    for idx, request_data in enumerate(requests):
        request_frame = tk.Frame(teacher_window, borderwidth=1, relief="solid", padx=10, pady=10, bg="light blue")
        request_frame.grid(row=idx*3, column=0, padx=10, pady=10, sticky="ew")

        request_text = f"Request {request_data['request_number']}:\n" \
                       f"Name: {request_data['name']}\n" \
                       f"ID Number: {request_data['id_number']}\n" \
                       f"Subject: {request_data['subject']}\n" \
                       f"Explanation: {request_data['explanation']}\n" \
                       f"Status: {request_data['status']}"

        request_label = tk.Label(request_frame, text=request_text, justify="left", bg="light blue", fg="black")
        request_label.grid(row=0, column=0, sticky="w")

        status_var = tk.IntVar(value=0)
        status_vars.append(status_var)

        approve_checkbox = tk.Checkbutton(request_frame, text="Approve", variable=status_var, onvalue=1, offvalue=0, bg="light blue", fg="black")
        approve_checkbox.grid(row=1, column=0, padx=(0, 5), sticky="e")

        not_approve_checkbox = tk.Checkbutton(request_frame, text="Not Approve", variable=status_var, onvalue=2, offvalue=0, bg="light blue", fg="black")
        not_approve_checkbox.grid(row=1, column=1, padx=(5, 0), sticky="w")

    submit_button = tk.Button(teacher_window, text="Submit", command=submit, bg="light blue", fg="black")
    submit_button.grid(row=len(requests)*3, column=0, pady=10)

    teacher_window.mainloop()

teacher_view()
