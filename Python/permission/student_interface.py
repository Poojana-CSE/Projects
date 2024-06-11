import tkinter as tk
from tkinter import messagebox

def on_submit():
    # Get the values from the input fields
    name = name_entry.get().strip()
    id_number = id_entry.get().strip()
    subject = subject_var.get().strip()  # Get selected subject from the variable
    explanation = explanation_entry.get("1.0", tk.END).strip()

    # Check if any field is empty
    if not (name and id_number and subject and explanation):
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    # Read the last request number from the file or start from 1 if the file is empty
    try:
        with open("requests.txt", "r") as file:
            last_request_number = sum(1 for line in file if line.startswith("Request"))
    except FileNotFoundError:
        last_request_number = 0

    # Increment the request number
    request_number = last_request_number + 1

    # Save data to a text file with a one-line space between each request
    with open("requests.txt", "a") as file:
        if last_request_number != 0:  # Add space if there's already an existing request
            file.write("\n")
        file.write(f"\nRequest {request_number}:\nName: {name}\nID Number: {id_number}\nSubject: {subject}\nExplanation: {explanation}\nStatus: Pending\n")

    messagebox.showinfo("Submission Details", f"Data has been saved to requests.txt as Request {request_number}. Make a note of the request number to check status in the future.")

    # Clear input fields after submission
    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    explanation_entry.delete("1.0", tk.END)
    subject_var.set(subject_options[0])  # Reset the dropdown to the default option

# Create the main application window
root = tk.Tk()
root.title("Student Interface")
root.configure(bg="#ADD8E6")  # Light blue background

# Create a frame
frame = tk.Frame(root, bg="#ADD8E6")  # Light blue background
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
