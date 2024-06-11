import tkinter as tk
from tkinter import messagebox, simpledialog

def donate():
    name = name_entry.get()
    amount = amount_entry.get()
    categories = [c.get() for c in category_vars]
    selected_types = ["Cancer Patients", "Childs", "Age Old Peoples", "Physically Challenged", "All of the above"]
    selected_categories = [selected_types[i] for i in range(len(categories)) if categories[i] == 1]

    if not name or not amount or not selected_categories:
        messagebox.showerror("Error", "Please fill in all fields and select at least one category.")
        return

    # Payment Confirmation
    confirm_payment = messagebox.askyesno("Payment Confirmation", f"Please pay Rs. {amount} to Google Pay number 9042421622. After payment, click 'Yes'.")
    if not confirm_payment:
        return

    transaction_id = simpledialog.askstring("Transaction ID", "Enter Transaction ID:")
    if not transaction_id:
        messagebox.showerror("Error", "Transaction ID is required.")
        return

    # Donation Submission
    try:
        with open("history.txt", "r") as history_file:
            donation_no = sum(1 for line in history_file) + 1
    except FileNotFoundError:
        with open("history.txt", "w") as history_file:
            donation_no = 1

    with open("history.txt", "a") as history_file:
        donation_info = f"Donation no: {donation_no}, {name}, {amount}, {', '.join(selected_categories)}, Transaction ID: {transaction_id}\n"
        history_file.write(donation_info)

    try:
        with open("amount.txt", "r") as amount_file:
            amounts = amount_file.read().splitlines()
    except FileNotFoundError:
        with open("amount.txt", "w") as amount_file:
            amounts = [f"{category}:0" for category in selected_types]

    new_amounts = []
    for category, selected in zip(selected_types, categories):
        if selected:
            new_amounts.append(f"{category}:{amount}")
        else:
            for line in amounts:
                if category in line:
                    new_amounts.append(line)
                    break
            else:
                new_amounts.append(f"{category}:0")

    with open("amount.txt", "w") as amount_file:
        amount_file.write("\n".join(new_amounts))

    messagebox.showinfo("Success", "Payment successful! Thank you for donating.")

root = tk.Tk()
root.title("Donation Form")

tk.Label(root, text="Donater Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Amount (Rupees):").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Category:").grid(row=2, column=0, padx=5, pady=5)
category_vars = [tk.IntVar() for _ in range(5)]
categories = ["Cancer Patients", "Childs", "Age Old Peoples", "Physically Challenged", "All of the above"]
for i in range(5):
    tk.Checkbutton(root, text=categories[i], variable=category_vars[i]).grid(row=2, column=i+1, padx=5, pady=5)

donate_button = tk.Button(root, text="Donate", command=donate)
donate_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
