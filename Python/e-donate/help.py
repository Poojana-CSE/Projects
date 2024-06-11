import tkinter as tk
from tkinter import messagebox

def submit_help():
    org_name = org_name_entry.get()
    amount_needed = amount_needed_entry.get()
    selected_types = [types[i] for i in range(len(types)) if type_vars[i].get() == 1]

    if not org_name or not amount_needed or not selected_types:
        messagebox.showerror("Error", "Please fill in all fields and select at least one type.")
        return

    with open("help.txt", "a") as help_file:
        help_file.write(f"Organization Name: {org_name}, Amount Needed: {amount_needed}, Type: {', '.join(selected_types)}, Status: Pending\n")

    messagebox.showinfo("Success", "Information submitted successfully!")

root = tk.Tk()
root.title("Help Request Form")

tk.Label(root, text="Organization Name:").grid(row=0, column=0, padx=5, pady=5)
org_name_entry = tk.Entry(root)
org_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Amount Needed:").grid(row=1, column=0, padx=5, pady=5)
amount_needed_entry = tk.Entry(root)
amount_needed_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Type:").grid(row=2, column=0, padx=5, pady=5)

types = ["Cancer Patients", "Childs", "Age Old Peoples", "Physically Challenged", "All of the above"]
type_vars = [tk.IntVar() for _ in range(len(types))]
for i, type_name in enumerate(types):
    tk.Checkbutton(root, text=type_name, variable=type_vars[i]).grid(row=2, column=i+1, padx=5, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_help)
submit_button.grid(row=3, column=0, columnspan=len(types)+1, pady=10)

root.mainloop()
