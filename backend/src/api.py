import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth # all routes using requires_auth decorate require a payload parameter

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        # format drinks to return in json blob
        formatted_drinks = [drink.short() for drink in drinks]
        return json.dumps({
            "success": True,
            "drinks": formatted_drinks
        })
    except Exception as err:
        print(f"error: {err}")
        abort(422)
    

'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        # format drinks to return in json blob
        formatted_drinks = [drink.long() for drink in drinks]
        return json.dumps({
            "success": True,
            "drinks": formatted_drinks
        })
    except Exception as err:
        print(f"error: {err}")
        abort(422)


'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    try:
        data = request.get_json()
        drink_title = data.get('title')
        drink_recipe = json.dumps([data.get('recipe')])
        drink = Drink(
            title=drink_title,
            recipe=drink_recipe
        )
        # Extra TODO raise integrity error if drink is already present
        Drink.insert(drink)
        return json.dumps({
            "success": True,
            "drinks": [
                {
                    "id": drink.id,
                    "title": drink.title,
                    "recipe": drink.recipe
                }
            ]
        })
    except Exception as err:
        abort(400)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, drink_id):
    try:
        data = request.get_json()
        drink_title = data.get('title')
        drink_recipe = json.dumps([data.get('recipe')])
    except Exception as err:
        print(f'error: {err}')
        abort(400)
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.title = drink_title 
        drink.recipe = drink_recipe
        Drink.update(drink)
        return json.dumps({
            "success": True,
            "drinks": [
                {
                    'id': drink.id,
                    'title': drink.title,
                    'recipe': drink.recipe
                }
            ]
        })
    except Exception as err:
        print(f'error: {err}')
        abort(422)


'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.get(drink_id)
    if not drink:
        abort(404)
    try:
        Drink.delete(drink)
        return json.dumps({
            "success": True,
            "delete": drink.id
        })
    except Exception as err:
        print(f'error: {err}')
        abort(422)
    


## Error Handling
# extra-todo more error handling
@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

# The auth error will already be defined from the auth.py module, we're just returning the json here
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code