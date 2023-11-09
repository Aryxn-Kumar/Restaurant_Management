from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kashif7kato'
app.config['MYSQL_DB'] = 'restaurant_management'

# Initialize MySQL
db = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with your authentication logic
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT username, password FROM login WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and password == user[1]:  # Use integer index to access 'password' column
            # Successful login
            return redirect('/homepage')
        else:
            # Failed login
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists. Please choose another username."
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
            db.connection.commit()
            cursor.close()
            return "Registration successful. You can now log in."

    return render_template('register.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Handle POST requests for the homepage if needed
        pass
    return render_template('homepage.html')

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    if request.method == 'POST':
        # Handle staff-related operations here, e.g., adding new staff
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']
        
        # Insert the new staff into the database
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO staff (staff_name, staff_number, staff_designation, staff_salary) VALUES (%s, %s, %s, %s)",
                       (staff_name, staff_number, staff_designation, staff_salary))
        db.connection.commit()
        cursor.close()
    
    # Fetch the list of staff from the database to display in the template
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM staff")
    staff_data = cursor.fetchall()
    cursor.close()

    return render_template('staff.html', staff=staff_data)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    if request.method == 'POST':
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO staff (staff_name, staff_number, staff_designation, staff_salary) VALUES (%s, %s, %s, %s)",
                       (staff_name, staff_number, staff_designation, staff_salary))
        db.connection.commit()
        cursor.close()

    return redirect('/staff')

@app.route('/update_staff', methods=['POST'])
def update_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']

        cursor = db.connection.cursor()
        cursor.execute("UPDATE staff SET staff_name = %s, staff_number = %s, staff_designation = %s, staff_salary = %s WHERE staff_id = %s",
                       (staff_name, staff_number, staff_designation, staff_salary, staff_id))
        db.connection.commit()
        cursor.close()

    return redirect('/staff')

if __name__ == "__main__":
    app.run(debug=True)
