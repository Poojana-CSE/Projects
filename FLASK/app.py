from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

def load_requests():
    try:
        with open("requests.txt", "r") as file:
            requests = file.read().split("\n\n")
        return requests[:-1]  # Exclude the last empty string caused by the split
    except FileNotFoundError:
        return []

def update_requests(requests):
    with open("requests.txt", "w") as file:
        file.write("\n\n".join(requests))

@app.route('/')
def manager_view():
    requests = load_requests()
    return render_template('index.html', requests=requests)

@app.route('/submit', methods=['POST'])
def submit():
    requests = load_requests()
    updated_requests = []
    for idx, request in enumerate(requests):
        status = "Approved" if request.form[f'status_{idx}'] == '1' else "Not Approved"
        updated_requests.append(request.replace("Status: Pending", f"Status: {status}"))

    update_requests(updated_requests)
    flash("Requests updated successfully.")
    return redirect(url_for('manager_view'))

@app.route('/worker')
def worker_view():
    return render_template('worker.html')

@app.route('/worker_submit', methods=['POST'])
def worker_submit():
    name = request.form['name']
    id_number = request.form['id_number']
    subject = request.form['subject']
    explanation = request.form['explanation']

    try:
        with open("requests.txt", "r") as file:
            last_request_number = sum(1 for _ in file) // 6
    except FileNotFoundError:
        last_request_number = 0

    request_number = last_request_number + 1

    with open("requests.txt", "a") as file:
        file.write(f"Request {request_number}:\nName: {name}\nID Number: {id_number}\nSubject: {subject}\nExplanation: {explanation}\nStatus: Pending\n\n")

    flash(f"Data has been saved as Request {request_number}.")
    return redirect(url_for('worker_view'))

@app.route('/check_status', methods=['POST'])
def check_status():
    request_number = request.form['request_number']
    try:
        with open("requests.txt", "r") as file:
            lines = file.readlines()
        found = False
        for line in lines:
            if f"Request {request_number}:" in line:
                found = True
            elif found and "Status:" in line:
                status = line.split(":")[1].strip()
                flash(f"Request {request_number} status: {status}")
                return redirect(url_for('worker_view'))
        flash(f"Request {request_number} not found.")
    except FileNotFoundError:
        flash("No requests found.")
    return redirect(url_for('worker_view'))

if __name__ == '__main__':
    app.run(debug=True)
