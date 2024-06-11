import tkinter as tk
from tkinter import messagebox

def check_status():
    request_number = request_entry.get()

    try:
        with open("requests.txt", "r") as file:
            lines = file.readlines()

        request_found = False
        status = None
        start_index = -1
        end_index = -1

        for i, line in enumerate(lines):
            if f"Request {request_number}:" in line:
                request_found = True
                start_index = i
                for j in range(i+1, len(lines)):
                    if lines[j].strip() == "":
                        end_index = j + 1
                        break
                    if "Status:" in lines[j]:
                        status = lines[j].strip().split(": ")[1]
                break

        if request_found:
            if status:
                if status == "Approved":
                    del lines[start_index:end_index]
                    # Renumber the remaining requests
                    request_count = 1
                    for i, line in enumerate(lines):
                        if line.startswith("Request "):
                            lines[i] = f"Request {request_count}:\n"
                            request_count += 1
                    with open("requests.txt", "w") as file:
                        file.writelines(lines)
                    messagebox.showinfo("Request Status", f"Request {request_number} was approved and has been removed.")
                else:
                    messagebox.showinfo("Request Status", f"Request {request_number} status: {status}")
            else:
                messagebox.showerror("Error", f"Status for Request {request_number} not found.")
        else:
            messagebox.showerror("Error", f"Request {request_number} not found.")
    
    except FileNotFoundError:
        messagebox.showerror("Error", "No requests file found.")

# Create the main application window
root = tk.Tk()
root.title("Check Status")
root.configure(bg="#ADD8E6")  # Light blue background

# Create a frame
frame = tk.Frame(root, bg="#ADD8E6")  # Light blue background
frame.pack(padx=20, pady=20)

# Request Number
request_label = tk.Label(frame, text="Enter Request Number:", bg="#ADD8E6", fg="black")
request_label.grid(row=0, column=0, sticky="e")

request_entry = tk.Entry(frame)
request_entry.grid(row=0, column=1, padx=5, pady=5)

status_button = tk.Button(frame, text="Check Status", command=check_status, bg="white", fg="black")
status_button.grid(row=0, column=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
