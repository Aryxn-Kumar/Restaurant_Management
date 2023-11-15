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

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        if 'add_customer' in request.form:
            # Handle adding a new customer
            customer_name = request.form['customer_name']
            customer_number = request.form['customer_number']
            customer_email = request.form['customer_email']
            customer_address = request.form['customer_address']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO customer (customer_name, customer_number, customer_email, customer_address) VALUES (%s, %s, %s, %s)",
                           (customer_name, customer_number, customer_email, customer_address))
            db.connection.commit()
            cursor.close()

        elif 'delete_customer' in request.form:
            # Handle deleting a customer
            customer_id = request.form['customer_id']

            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
            db.connection.commit()
            cursor.close()

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM customer")
    customer_data = cursor.fetchall()
    cursor.close()

    return render_template('customers.html', customers=customer_data)

# ... (previous code)

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    if request.method == 'POST':
        if 'reserve_table' in request.form:
            # Handle table reservation
            party_size = request.form['party_size']
            reservation_date = request.form['reservation_date']

            # Assign the first available table
            cursor = db.connection.cursor()
            cursor.execute("SELECT table_id FROM table_ WHERE assignment_id IS NULL LIMIT 1")
            available_table = cursor.fetchone()

            if available_table:
                table_id = available_table[0]
                cursor.execute("INSERT INTO reservation (party_size, reservation_date, table_id) VALUES (%s, %s, %s)",
                               (party_size, reservation_date, table_id))
                db.connection.commit()
            else:
                return "No available tables for reservation."
                
            cursor.close()

        elif 'assign_waiter' in request.form:
            # Handle waiter assignment
            waiter_id = request.form['waiter_id']
            table_id = request.form['table_id']

            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM table_assignments WHERE waiter_id = %s", (waiter_id,))
            assigned_table = cursor.fetchone()

            if assigned_table:
                return "Waiter is already assigned to a table."
            else:
                cursor.execute("INSERT INTO table_assignments (table_id, waiter_id) VALUES (%s, %s)",
                               (table_id, waiter_id))
                db.connection.commit()
                cursor.close()

    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT
            r.reservation_id,
            r.party_size,
            r.reservation_date,
            r.table_id,
            t.waiter_id
        FROM
            reservation r
            LEFT JOIN table_assignments t ON r.table_id = t.table_id
    """)
    reservations_data = cursor.fetchall()
    cursor.close()

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM table_")
    tables_data = cursor.fetchall()

    cursor.execute("SELECT * FROM staff WHERE staff_designation = 'waiter'")
    waiters_data = cursor.fetchall()
    cursor.close()

    return render_template('tables.html', tables_data=tables_data, waiters_data=waiters_data, reservations_data=reservations_data)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        if 'add_menu' in request.form:
            # Handle adding a new menu item
            menu_name = request.form['menu_name']
            menu_price = request.form['menu_price']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO menu (menu_name, menu_price) VALUES (%s, %s)", (menu_name, menu_price))
            db.connection.commit()
            cursor.close()

        elif 'delete_menu' in request.form:
            # Handle deleting a menu item
            menu_id = request.form['menu_id']

            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM menu WHERE menu_id = %s", (menu_id,))
            db.connection.commit()
            cursor.close()

    # Fetch menu items
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_data = cursor.fetchall()
    cursor.close()

    return render_template('menu.html', menu=menu_data)
   
   
@app.route('/tables', methods=['POST'])
def add_table():
    if 'add_table' in request.form:
        employee_capacity = request.form['employee_capacity']
        employee_booking = request.form['employee_booking']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO table_ (employee_capacity, employee_booking) VALUES (%s, %s)", (employee_capacity, employee_booking))
        db.connection.commit()
        cursor.close()

    # Rest of your code for fetching and displaying table reservations

    return redirect('/tables')  # Redirect to the same page after handling the form

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if 'add_order' in request.form:
            menu_id = request.form['menu_id']
            special_request = request.form['special_request']
            order_quantity = request.form['order_quantity']
            customer_id = request.form['customer_id']

            # Retrieve additional information about the menu item
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM menu WHERE menu_id = %s", (menu_id,))
            menu_info = cursor.fetchone()

            # Add the order to the database
            cursor.execute("""
    INSERT INTO order_ (menu_id, special_request, order_quantity, customer_id, table_assignment_id, chef_id)
    VALUES (
        %s,
        %s,
        %s,
        %s,
        (SELECT assignment_id FROM table_assignments WHERE waiter_id IS NOT NULL LIMIT 1),
        (SELECT staff_id FROM staff WHERE staff_designation = 'chef' LIMIT 1)
    )
""", (
    int(menu_id) if menu_id else None,
    special_request,
    int(order_quantity) if order_quantity else None,
    int(customer_id) if customer_id else None
))


            db.connection.commit()
            cursor.close()

    # Fetch order information including related data (menu, table, waiter, etc.)
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT
            o.order_id,
            o.special_request,
            o.order_quantity,
            o.customer_id,
            t.table_id,
            t.waiter_id,
            m.menu_name,
            m.menu_price
        FROM
            order_ o
            LEFT JOIN table_assignments t ON o.table_assignment_id = t.assignment_id
            LEFT JOIN menu m ON o.menu_id = m.menu_id
    """)
    orders_data = cursor.fetchall()
    cursor.close()

    # Fetch menu information
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_data = cursor.fetchall()
    cursor.close()

    return render_template('order.html', menu=menu_data, orders=orders_data)

if __name__ == "__main__":
    app.run(debug=True)
