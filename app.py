from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Full-Stack-dev97@127.0.0.1/fitness_center_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta: 
        fields = ('id', 'name', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    session_id = fields.Integer()
    member_id = fields.Integer(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'session_time', 'activity')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

class Member(db.Model):
    __tablename__ = 'Members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    workout_session = db.relationship('WorkoutSessions', backref='Members')

class WorkoutSessions(db.Model):
    __tablename__ = 'WorkoutSessions'

    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(255), nullable=False)

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Member(name=member_data['name'], age=member_data['age'])
    db.session.add(new_member)
    db.session.commit()

    return jsonify({'message': 'New member added successfully'})

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)

    try:
        member_data = member_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.name = member_data['name']
    member.age = member_data['age']

    db.session.commit()

    return jsonify({'message': 'Member details updated successfully'})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)

    db.session.delete(member)
    db.session.commit()

    return jsonify({'message': 'Member deleted successfully'})

@app.route('/workout_sessions', methods=['GET'])
def get_workout_sessions():
    workout_sessions = WorkoutSessions.query.all()
    return workout_sessions_schema.jsonify(workout_sessions)

@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    try:
        workout_session_data = workout_session_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_workout_session = WorkoutSessions(member_id=workout_session_data['member_id'], session_date=workout_session_data['session_date'], session_time=workout_session_data['session_time'], activity=workout_session_data['activity'])
    db.session.add(new_workout_session)
    db.session.commit()

    return jsonify({'message': 'New workout session added successfully'}), 201

@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    workout_session = WorkoutSessions.query.get_or_404(id)

    try:
        workout_session_data = workout_session_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    workout_session.member_id = workout_session_data['member_id']
    workout_session.session_date = workout_session_data['session_date']
    workout_session.session_time = workout_session_data['session_time']
    workout_session.activity = workout_session_data['activity']

    db.session.commit()

    return jsonify({'message': 'Workout session details updated successfully'}), 200

@app.route('/workout_sessions/member/<int:id>', methods=['GET'])
def get_workout_session_by_member(id):
    workout_sessions = WorkoutSessions.query.filter_by(member_id=id).all()
    return workout_sessions_schema.jsonify(workout_sessions)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)