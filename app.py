# Task 1

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

# initialize the Flask app
app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    index = fields.Integer()
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'name', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    session_id = fields.Integer()
    member_id = fields.Integer(required=True)
    activity = fields.String(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)

    class Meta:
        fields = ('session_id', 'member_id', 'activity', 'session_date', 'session_time')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

def get_db_connection():

    db_name = "fitness_center_db"
    user = "root"
    host = "127.0.0.1"
    password = "Full-Stack-dev97"

    try:
        conn = mysql.connector.connect(
            user = user, password = password, host = host, database = db_name)
        
        print("Connection to the MySQL DB successful")

        return conn
    
    except Error as e:
        print(f'Error: {e}')
        return None
    
@app.route('/')
def home():
    return 'Welcome to the Fitness Center API'

# Task 2
@app.route('/members', methods=['GET'])
def get_members():

    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/members', methods=['POST'])
def add_member():

    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'])

        query = "INSERT INTO Members (name, age) VALUES (%s, %s)"

        cursor.execute(query, new_member)

        conn.commit()

        return jsonify({'message': 'New member added successfully'}), 201
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):

    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['age'], id)

        query = "UPDATE Members SET name = %s, age = %s WHERE id = %s"

        cursor.execute(query, updated_member)

        conn.commit()

        return jsonify({'message': 'Member updated successfully'}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor()

        member_to_delete = (id,)

        query = "DELETE FROM Members WHERE id = %s"

        cursor.execute(query, member_to_delete)

        conn.commit()

        return jsonify({'message': 'Member deleted successfully'}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

# Task 3
@app.route('/workoutsessions', methods=['GET'])
def get_workout_sessions():

    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM WorkoutSessions"

        cursor.execute(query)

        workouts = cursor.fetchall()

        return workout_sessions_schema.jsonify(workouts)
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/workoutsessions', methods=['POST'])
def add_workout_session():

    try:
        workout_session_data = workout_session_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor()

        new_workout_session = (workout_session_data['member_id'], workout_session_data['activity'], workout_session_data['session_date'], workout_session_data['session_time'])

        query = "INSERT INTO WorkoutSessions (member_id, activity, session_date, session_time) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, new_workout_session)

        conn.commit()

        return jsonify({'message': 'New workout session added successfully'}), 201
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/workoutsessions/<int:id>', methods=['PUT'])
def update_workout_session(id):

    try:
        workout_session_data = workout_session_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor()

        updated_workout_session = (workout_session_data['member_id'], workout_session_data['activity'], workout_session_data['session_date'], workout_session_data['session_time'], id)

        query = "UPDATE WorkoutSessions SET member_id = %s, activity = %s, session_date = %s, session_time = %s WHERE session_id = %s"

        cursor.execute(query, updated_workout_session)

        conn.commit()

        return jsonify({'message': 'Workout session updated successfully'}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

@app.route('/workoutsessions/member/<int:id>', methods=['GET'])
def get_workout_sessions_by_member(id):

    try:
        conn = get_db_connection()

        if conn is None:
            return jsonify({'error': 'Connection to the database failed'}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"

        cursor.execute(query, (id,))

        workouts = cursor.fetchall()

        return workout_sessions_schema.jsonify(workouts)
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)