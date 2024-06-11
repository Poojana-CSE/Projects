import tkinter as tk
from tkinter import messagebox

def load_requests():
    try:
        with open("requests.txt", "r") as file:
            requests = file.read().split("\n\nRequest ")
        requests = [request.strip() for request in requests if request.strip()]
        return requests
    except FileNotFoundError:
        messagebox.showerror("Error", "No requests found.")
        return []

def update_requests(requests):
    try:
        with open("requests.txt", "w") as file:
            file.write("\n\nRequest ".join(requests))
        messagebox.showinfo("Success", "Requests updated successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No requests found.")

def teacher_view():
    def submit():
        for idx, var in enumerate(status_vars):
            if var.get() == 1:
                request_lines = requests[idx].split('\n')
                for i, line in enumerate(request_lines):
                    if line.startswith("Status:"):
                        request_lines[i] = "Status: Approved"
                        break
                requests[idx] = '\n'.join(request_lines)
            elif var.get() == 2:
                request_lines = requests[idx].split('\n')
                for i, line in enumerate(request_lines):
                    if line.startswith("Status:"):
                        request_lines[i] = "Status: Not Approved"
                        break
                requests[idx] = '\n'.join(request_lines)
        update_requests(requests)

    teacher_window = tk.Tk()
    teacher_window.title("Teacher View")
    teacher_window.geometry("800x600")

    requests = load_requests()
    status_vars = []

    for idx, request_text in enumerate(requests):
        col = idx // 3
        row = (idx % 3) * 3

        request_frame = tk.Frame(teacher_window, borderwidth=1, relief="solid", padx=10, pady=10, bg="light blue")
        request_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        request_label = tk.Label(request_frame, text=request_text, justify="left", bg="light blue", fg="black")
        request_label.grid(row=0, column=0, columnspan=2, sticky="w")

        status_var = tk.IntVar(value=0)
        status_vars.append(status_var)

        approve_checkbox = tk.Checkbutton(request_frame, text="Approve", variable=status_var, onvalue=1, offvalue=0, bg="light blue", fg="black")
        approve_checkbox.grid(row=1, column=0, padx=(0, 5), sticky="e")

        not_approve_checkbox = tk.Checkbutton(request_frame, text="Not Approve", variable=status_var, onvalue=2, offvalue=0, bg="light blue", fg="black")
        not_approve_checkbox.grid(row=1, column=1, padx=(5, 0), sticky="w")

    # Calculate the row for the submit button to place it at the bottom right
    total_rows = (len(requests) + 2) // 3 * 3
    submit_button = tk.Button(teacher_window, text="Submit", command=submit, bg="light blue", fg="black")
    submit_button.grid(row=total_rows + 1, column=col, pady=10, padx=10, sticky="se")

    teacher_window.mainloop()

teacher_view()
