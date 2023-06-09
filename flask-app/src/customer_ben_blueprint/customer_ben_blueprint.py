from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# Ben Personas
# [1] As a user, Ben wants to see all restaurants available located in New York.
# [2] Since Ben has classes both in the morning and afternoon, he likes to order fast food for lunch since it usually has relatively faster delivery time, so he sometimes likes to only see the fast food restaurants located in New York.
# [3] Due to the fact that Ben currently has no income and is a student, he likes to see the foods with promotions in the restaurants that are located in New York.
# [4] Ben needs to see the menu first in order to place an order.
# [5] He also needs to be able to check the order status and see the past orders.
# [6] As a user, Ben wants to place an order from a restaurant  with the food that he wants.
# [7] Ben sometimes needs to cancel an order due to some unforeseen circumstances.
# [8] After canceling the order, Ben would like to delete the order, so he does not see it in his order history anymore.

customer_ben_blueprint = Blueprint('customer_ben_blueprint', __name__)

# Test the customer Ben route
@customer_ben_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for customer Ben</h1>"

# [Ben-1]
# Get all the New York restaurants
@customer_ben_blueprint.route('/restaurants/new_york', methods=['GET'])
def get_restaurants_newyork():
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of New York restaurants
  cursor.execute(
    '''SELECT 
    Restaurants.name as "Restaurant Name", 
    Restaurants_Locations.address as "Address", 
    Restaurants_Locations.city as "City", 
    Restaurants_Locations.state as "State", 
    Restaurants_Locations.zip as "Zip",
    Categories.name as "Category"
    FROM Restaurants 
    JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id 
    JOIN Categories ON Restaurants.category_id = Categories.category_id
    WHERE Restaurants_Locations.city = \'New York\'''')

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in 
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers. 
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)

# [Ben-2]
# Get all the New York restaurants that belongs to the given category
@customer_ben_blueprint.route('/restaurants/new_york/<int:category_id>', methods=['GET'])
def get_restaurants_newyork_categoryid(category_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of New York restaurants that belongs to the given category
  cursor.execute(
    '''SELECT 
    Restaurants.name as "Restaurant Name", 
    Restaurants_Locations.address as "Address", 
    Restaurants_Locations.city as "City", 
    Restaurants_Locations.state as "State", 
    Restaurants_Locations.zip as "Zip"
    FROM Restaurants
    JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id
    Join Categories ON Restaurants.category_id = Categories.category_id
    WHERE Restaurants_Locations.city = \'New York\' AND Categories.category_id = %s''', category_id)

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in 
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers. 
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)
  
# [Ben-3]
# Get all the New York discount food
@customer_ben_blueprint.route('/restaurants/new_york/discount_food', methods=['GET'])
def get_restaurants_newyork_discountfood():
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of New York discount food
  cursor.execute(
    '''SELECT 
    Foods.name as "Name", 
    (Foods.price - Foods.discount) as "Discounted Price", 
    Restaurants.name as "Restaurants Name" 
    FROM Restaurants
    JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id
    JOIN Menus ON Restaurants.restaurant_id = Menus.restaurant_id
    JOIN Foods ON Menus.menu_id = Foods.menu_id
    WHERE Restaurants_Locations.city = \'New York\' AND Foods.discount > 0.00
    ORDER BY Foods.price - Foods.discount ASC''')

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in 
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers. 
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)

# [Ben-4]
# Get the menu of Burger Express
@customer_ben_blueprint.route('/menus/<int:menu_id>', methods=['GET'])
def get_menus_menuid(menu_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for the menu of Burger Express
  cursor.execute(
    '''SELECT 
    Foods.name as "Name", 
    Foods.price as "Price",
    Foods.discount as "Discount",
    Foods.food_id as "ID"
    FROM Restaurants
    JOIN Menus ON Restaurants.restaurant_id = Menus.restaurant_id
    JOIN Foods ON Menus.menu_id = Foods.menu_id
    WHERE Menus.menu_id = %s''', menu_id)

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in 
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers.
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)

# [Ben-5]
# Get all orders placed by a customer
@customer_ben_blueprint.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customerid_orders(customer_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of orders placed by the customer
  cursor.execute(
      '''SELECT 
      Orders.order_id as "Order ID",
      Orders.order_time as "Order Time",
      Orders.order_status as "Order Status",
      Orders.restaurant_location_id as "Restaurant Location ID",
      Orders.restaurant_id as "Restaurant ID",
      Orders.customer_id as "Customer ID",
      Orders.customer_address_id as "Customer Address ID",
      Orders.ETA as "ETA",
      Foods.name as "Food Name",
      Order_Items.quantity as "Quantity"
      FROM Orders
      JOIN Order_Items ON Orders.order_id = Order_Items.order_id
      JOIN Foods ON Order_Items.food_id = Foods.food_id
      WHERE Orders.customer_id = %s
      ORDER BY Orders.order_time DESC''', (customer_id,))

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers.
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)

# [Ben-6]
# Place an order for a customer
@customer_ben_blueprint.route('/place_order', methods=['POST'])
def place_order():
  # Access JSON data from the request object
  req_data = request.get_json()

  rest_id = req_data['restaurant_id']
  rest_location_id = req_data['restaurant_location_id']
  fd_id = req_data['food_id']
  quan = req_data['quantity']
  spec = req_data['special_instruction']
  
  # Insert order data into the Orders table
  insert_order_stmt = 'INSERT INTO Orders (customer_id, restaurant_location_id, restaurant_id, customer_address_id) VALUES (1, ' + str(rest_location_id) + ', '+ str(rest_id) +', 1)'

  # Execute the queries
  cursor = db.get_db().cursor()
  cursor.execute(insert_order_stmt)

  db.get_db().commit()

  order_id = cursor.lastrowid

  insert_order_item_stmt = 'INSERT INTO Order_Items (order_id, food_id, quantity, special_instructions) VALUES (' + str(order_id) + ', ' + str(fd_id) + ', ' + str(quan) + ', "' + spec +'")'

  cursor = db.get_db().cursor()
  cursor.execute(insert_order_item_stmt)

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message and the order_id
  return "Success"

# [Ben-7]
# Cancel an order for a customer
@customer_ben_blueprint.route('/cancel_order', methods=['PUT'])
def cancel_order():
  # Access JSON data from the request object
  req_data = request.get_json()

  order_id = req_data['order_id']

  # Check if the order exists
  cursor = db.get_db().cursor()
  cursor.execute('SELECT * FROM Orders WHERE order_id = %s', order_id)
  order = cursor.fetchone()

  if order is None:
      return "No Order Found"

  # Update the order_status to 'Canceled'
  update_order_stmt = 'UPDATE Orders SET order_status = "Canceled" WHERE order_id = ' + str(order_id)
  cursor.execute(update_order_stmt)

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message
  return "Success"

# [Ben-8]
# Delete an order for a customer
@customer_ben_blueprint.route('/delete_order', methods=['DELETE'])
def delete_order():
  # Access JSON data from the request object
  req_data = request.get_json()

  order_id = req_data['delete_order_id']

  # Execute the queries
  cursor = db.get_db().cursor()
  # Check if the order exists
  cursor.execute('SELECT * FROM Orders WHERE order_id = %s', order_id)
  order = cursor.fetchone()

  if order is None:
      return "No Order Found"
    
  # Delete the payment records associated with the order
  delete_payment_stmt = 'DELETE FROM Payments WHERE order_id = ' + str(order_id)
  cursor.execute(delete_payment_stmt)

  # Delete the order items associated with the order
  delete_order_items_stmt = 'DELETE FROM Order_Items WHERE order_id = ' + str(order_id)
  cursor.execute(delete_order_items_stmt)

  # Delete the order from the Orders table
  delete_order_stmt = 'DELETE FROM Orders WHERE order_id = ' + str(order_id)
  cursor.execute(delete_order_stmt)

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message
  return "Success"
