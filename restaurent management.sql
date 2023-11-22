-- Create the database
CREATE DATABASE restaurant_management;

-- Use the database
USE restaurant_management;

-- Create the customer table
CREATE TABLE customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_name VARCHAR(255),
  customer_number INT,
  customer_email VARCHAR(255),
  customer_address VARCHAR(255)
);

-- Create the staff table with chef hierarchy
CREATE TABLE staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  staff_name VARCHAR(255),
  staff_number INT,
  staff_designation ENUM('waiter', 'manager', 'chef'),
  staff_salary INT,
  chef_hierarchy ENUM('sous chef', 'head chef', 'executive chef')
);

-- Create the table_ table
CREATE TABLE table_ (
  table_id INT AUTO_INCREMENT PRIMARY KEY,
  employee_capacity INT,
  employee_booking VARCHAR(255)
);

-- Create the reservation table
CREATE TABLE reservation (
  reservation_id INT AUTO_INCREMENT PRIMARY KEY,
  party_size INT,
  reservation_date DATE,
  table_id INT,
  customer_id INT,
  waiter_id INT,
  FOREIGN KEY (table_id) REFERENCES table_(table_id),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (waiter_id) REFERENCES staff(staff_id)
);

-- Create the customer_review table for staff
CREATE TABLE staff_review (
  staff_review_id INT AUTO_INCREMENT PRIMARY KEY,
  staff_id INT,
  customer_id INT,
  review_text TEXT,
  FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

-- Create the menu table
CREATE TABLE menu (
  menu_id INT AUTO_INCREMENT PRIMARY KEY,
  menu_name VARCHAR(255),
  menu_price INT
);

-- Create the order_ table
CREATE TABLE order_ (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  special_request VARCHAR(255),
  menu_id INT,
  order_date DATE,
  order_quantity INT,
  customer_id INT,
  table_id INT,
  chef_id INT,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (table_id) REFERENCES table_(table_id),
  FOREIGN KEY (chef_id) REFERENCES staff(staff_id),
  FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

-- Create the total_orders_completed table
CREATE TABLE total_orders_completed (
  date DATE PRIMARY KEY,
  total_orders_completed INT,
  total_amount INT
);

-- Create the login table
CREATE TABLE login (
  username VARCHAR(20),
  password VARCHAR(20)
);

CREATE TABLE table_assignments (
  assignment_id INT AUTO_INCREMENT PRIMARY KEY,
  table_id INT,
  waiter_id INT,
  FOREIGN KEY (table_id) REFERENCES table_(table_id)
);

-- Populate the total_orders_completed table with the daily totals
INSERT INTO total_orders_completed (date, total_orders_completed, total_amount)
SELECT
  order_date,
  COUNT(*) AS total_orders_completed,
  SUM(menu_price * order_quantity) AS total_amount
FROM
  order_
  INNER JOIN menu ON order_.menu_id = menu.menu_id
GROUP BY
  order_date;
  
-- Insert sample menu items
INSERT INTO menu (menu_name, menu_price) VALUES
('Classic Burger', 10),
('Margherita Pizza', 12),
('Caesar Salad', 8),
('Spaghetti Bolognese', 15),
('Grilled Chicken Sandwich', 9),
('BBQ Ribs', 18),
('Vegetarian Pizza', 14),
('Greek Salad', 10),
('Shrimp Alfredo Pasta', 16),
('Club Sandwich', 11),
('Steak', 22),
('Caprese Salad', 9),
('Veggie Wrap', 12),
('Fish and Chips', 14),
('Chicken Caesar Wrap', 11);

-- Dummy data for customer table
INSERT INTO customer (customer_name, customer_number, customer_email, customer_address)
VALUES
('John Doe', 123456789, 'john.doe@example.com', '123 Main St'),
('Jane Smith', 987654321, 'jane.smith@example.com', '456 Oak St');

-- Dummy data for staff table
INSERT INTO staff (staff_name, staff_number, staff_designation, staff_salary, chef_hierarchy)
VALUES
('Waiter 1', 111, 'waiter', 2500, NULL),
('Chef 1', 222, 'chef', 5000, 'head chef');

-- Dummy data for table_ table
INSERT INTO table_ (employee_capacity, employee_booking)
VALUES
(4, 'No'),
(6, 'Yes');

-- Dummy data for reservation table
INSERT INTO reservation (party_size, reservation_date, table_id, customer_id, waiter_id)
VALUES
(3, '2023-11-28', 1, 1, 1),
(5, '2023-11-29', 2, 2, 1);

-- Dummy data for staff_review table
INSERT INTO staff_review (staff_id, customer_id, review_text)
VALUES
(2, 1, 'Great service by Chef 1'),
(1, 2, 'Waiter 1 was very attentive');

-- Dummy data for menu table
INSERT INTO menu (menu_name, menu_price)
VALUES
('Burger', 10),
('Pizza', 12),
('Salad', 8);

-- Dummy data for order_ table
INSERT INTO order_ (special_request, menu_id, order_date, order_quantity, customer_id, table_id, chef_id)
VALUES
('No onions', 1, '2023-11-28', 2, 1, 1, 2),
(NULL, 2, '2023-11-29', 1, 2, 2, 2);

-- Dummy data for total_orders_completed table
INSERT INTO total_orders_completed (date, total_orders_completed, total_amount)
VALUES
('2023-11-28', 2, 30),
('2023-11-29', 1, 12);

-- Dummy data for login table
INSERT INTO login (username, password)
VALUES
('john_doe', 'password1'),
('jane_smith', 'password2');

