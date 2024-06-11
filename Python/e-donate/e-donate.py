import tkinter as tk
from tkinter import messagebox

def load_helps():
    try:
        with open("help.txt", "r") as file:
            helps = file.read().splitlines()
        return helps
    except FileNotFoundError:
        messagebox.showerror("Error", "No helps found.")
        return []

def update_helps(help_requests):
    try:
        with open("help.txt", "w") as file:
            file.write("\n".join(help_requests))
        messagebox.showinfo("Success", "Help requests updated successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No helps found.")

def load_amounts():
    try:
        with open("amount.txt", "r") as file:
            amounts = file.read().splitlines()
        return amounts
    except FileNotFoundError:
        messagebox.showerror("Error", "No amounts found.")
        return []

def update_amounts(new_amounts):
    try:
        with open("amount.txt", "w") as file:
            file.write("\n".join(new_amounts))
        messagebox.showinfo("Success", "Amounts updated successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No amounts found.")

def manager_view():
    manager_window = tk.Tk()
    manager_window.title("Manager View")

    def submit():
        updated_helps = []
        updated_amounts = load_amounts()

        for idx, help_request in enumerate(help_requests):
            if donate_vars[idx].get() == 1:
                help_parts = help_request.split(", ")
                org_name = help_parts[0].split(": ")[1]
                amount_needed = int(help_parts[1].split(": ")[1])
                help_type = help_parts[2].split(": ")[1]
                status = help_parts[3].split(": ")[1]

                if status == "Pending":
                    help_parts[3] = "Status: Donated"
                    updated_helps.append(", ".join(help_parts))

                    for i, line in enumerate(updated_amounts):
                        if help_type in line:
                            category, amount = line.split(":")
                            amount = int(amount)
                            if amount < amount_needed:
                                messagebox.showerror("Error", f"Insufficient funds for {help_type}.")
                                return
                            updated_amounts[i] = f"{category}:{amount - amount_needed}"
                            break
                    else:
                        messagebox.showerror("Error", "No matching category found in amounts.")
                else:
                    updated_helps.append(help_request)
            elif pending_vars[idx].get() == 1:
                updated_helps.append(help_request)

        update_helps(updated_helps)
        update_amounts(updated_amounts)

    help_requests = load_helps()
    selected_types = ["Cancer Patients", "Childs", "Age Old Peoples", "Physically Challenged", "All of the above"]
    donate_vars = []
    pending_vars = []

    for idx, help_request in enumerate(help_requests):
        help_label = tk.Label(manager_window, text=help_request)
        help_label.grid(row=idx*3, column=0, columnspan=4, sticky="w")

        donate_var = tk.IntVar()
        donate_vars.append(donate_var)
        donate_checkbox = tk.Checkbutton(manager_window, text="Donate", variable=donate_var)
        donate_checkbox.grid(row=idx*3+1, column=0)

        pending_var = tk.IntVar()
        pending_vars.append(pending_var)
        pending_checkbox = tk.Checkbutton(manager_window, text="Pending", variable=pending_var)
        pending_checkbox.grid(row=idx*3+1, column=1)

    submit_button = tk.Button(manager_window, text="Submit", command=submit)
    submit_button.grid(row=len(help_requests)*3+1, columnspan=4, pady=10)

    manager_window.mainloop()

manager_view()
