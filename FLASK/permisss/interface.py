import tkinter as tk
from tkinter import messagebox
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.Permission  
requests_collection = db.request

def get_next_request_number():
    last_request = requests_collection.find_one(sort=[("request_number", pymongo.DESCENDING)])
    if last_request:
        return last_request["request_number"] + 1
    return 1

def on_submit():
    name = name_entry.get().strip()
    id_number = id_entry.get().strip()
    subject = subject_var.get().strip()  
    explanation = explanation_entry.get("1.0", tk.END).strip()

    if not (name and id_number and subject and explanation):
        messagebox.showerror("Error", "Please fill in all the fields.")
        return
    request_number = get_next_request_number()
    request_data = {
        "request_number": request_number,
        "name": name,
        "id_number": id_number,
        "subject": subject,
        "explanation": explanation,
        "status": "Pending"
    }
    formatted_request = f"Request {request_number}:\n" \
                        f"Name: {name}\n" \
                        f"ID Number: {id_number}\n" \
                        f"Subject: {subject}\n" \
                        f"Explanation: {explanation}\n" \
                        f"Status: Pending"

    requests_collection.insert_one(request_data)

    messagebox.showinfo("Submission Details", formatted_request)

    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    explanation_entry.delete("1.0", tk.END)
    subject_var.set(subject_options[0])  
root = tk.Tk()
root.title("Student Interface")
root.configure(bg="#ADD8E6") 

# Create a frame
frame = tk.Frame(root, bg="#ADD8E6")  
frame.pack(padx=20, pady=20)

# Name
name_label = tk.Label(frame, text="Name:", bg="#ADD8E6", fg="black")
name_label.grid(row=0, column=0, sticky="e")

name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# ID Number
id_label = tk.Label(frame, text="ID Number:", bg="#ADD8E6", fg="black")
id_label.grid(row=1, column=0, sticky="e")

id_entry = tk.Entry(frame)
id_entry.grid(row=1, column=1, padx=5, pady=5)

# Subject
subject_label = tk.Label(frame, text="Subject:", bg="#ADD8E6", fg="black")
subject_label.grid(row=2, column=0, sticky="e")

subject_options = ["Casual leave", "Medical leave", "Emergency leave", "Other"]
subject_var = tk.StringVar(root)
subject_var.set(subject_options[0])  # Default option
subject_dropdown = tk.OptionMenu(frame, subject_var, *subject_options)
subject_dropdown.grid(row=2, column=1, padx=5, pady=5)

# Explanation
explanation_label = tk.Label(frame, text="Explanation:", bg="#ADD8E6", fg="black")
explanation_label.grid(row=3, column=0, sticky="ne")

explanation_entry = tk.Text(frame, width=30, height=5)
explanation_entry.grid(row=3, column=1, padx=5, pady=5)

# Submit Button
submit_button = tk.Button(frame, text="Submit", command=on_submit, bg="white", fg="black")
submit_button.grid(row=4, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
