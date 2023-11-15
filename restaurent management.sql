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

-- Create the table_assignments table
CREATE TABLE table_assignments (
  assignment_id INT AUTO_INCREMENT PRIMARY KEY,
  table_id INT,
  waiter_id INT,
  FOREIGN KEY (table_id) REFERENCES table_(table_id),
  FOREIGN KEY (waiter_id) REFERENCES staff(staff_id) -- Corrected reference to staff(staff_id)
);

-- Create the table_ table
CREATE TABLE table_ (
  table_id INT AUTO_INCREMENT PRIMARY KEY,
  employee_capacity INT,
  employee_booking VARCHAR(255),
  assignment_id INT
);

-- Create the reservation table
CREATE TABLE reservation (
  reservation_id INT AUTO_INCREMENT PRIMARY KEY,
  party_size VARCHAR(255),
  reservation_date DATE,
  table_id INT,
  FOREIGN KEY (table_id) REFERENCES table_(table_id)
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
  table_assignment_id INT,
  chef_id INT,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (table_assignment_id) REFERENCES table_assignments(assignment_id),
  FOREIGN KEY (chef_id) REFERENCES staff(staff_id),
  FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);

-- Create the total_orders_completed table
CREATE TABLE total_orders_completed (
  date DATE PRIMARY KEY,
  total_orders_completed INT,
  total_amount INT
);

CREATE TABLE login(
  username VARCHAR(20),
  password VARCHAR(20)
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


Show tables;
