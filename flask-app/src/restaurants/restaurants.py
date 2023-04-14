from flask import Blueprint, request, jsonify, make_response
import json
from src import db


restaurants = Blueprint('restaurants', __name__)

# Test the restaurants route
@restaurants.route('/', methods=['GET'])
def test_restaurants():
  return "<h1>This is a restaurants test</h1>"

# Get all the products from the database
@restaurants.route('/restaurants', methods=['GET'])
def get_restaurants():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM Restaurants')

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
