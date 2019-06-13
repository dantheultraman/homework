from database_setup import Base, User, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import Flask, jsonify, request, abort
import re
import smtplib
import os

app = Flask(__name__)

engine = create_engine('sqlite:///event.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

smtp_sender = os.environ['smtp_sender']
smtp_receiver = os.environ['notice_email']
smtp_address = os.environ['smtp_address']


@app.route('/events', methods=['POST'])
def createEvent():
    """Create a new event"""
    try:
        start = datetime.strptime(request.json['start'], '%Y-%m-%d %H:%M')
        end = datetime.strptime(request.json['end'], '%Y-%m-%d %H:%M')
        assert end > start
    except:
        abort(400, "Incorrect data format, should be YYYY-MM-DD H:M")

    try:
        newEvent = Event(
            name=request.json['name'],
            location=request.json['location'],
            start=request.json['start'],
            end=request.json['end']
        )
        session.add(newEvent)
        session.commit()
        return jsonify(newEvent.serialize), 201
    except:
        abort(400)


@app.route('/events/<int:event_id>', methods=['DELETE'])
def deleteEvent(event_id):
    """Delete an event"""
    try:
        event = session.query(Event).filter_by(id=event_id).one()
        session.delete(event)
        session.commit()
        return jsonify({'result': True})
    except:
        return jsonify({'result': False})


@app.route('/events/<int:event_id>', methods=['GET'])
def getEvent(event_id):
    """return an event"""
    try:
        event = session.query(Event).filter_by(id=event_id).one()
        return jsonify(event.serialize)
    except:
        abort(404)


@app.route('/events/<int:event_id>/subscribe', methods=['POST'])
def subscribe(event_id):
    """subscribe a new user to an event"""
    try:
        event = session.query(Event).filter_by(id=event_id).one()
        user = session.query(User).filter_by(email=request.json['email']).one()
    except:
        abort(400, "User not found.")

    message = """From: Homework {sender}
To: Notification {receiver}
Subject: Subscription notice
User {email} subscriped to event {event}
""".format(sender=smtp_sender, receiver=smtp_receiver,
           email=user.email, event=event.name)

    try:
        smtpObj = smtplib.SMTP(smtp_address)
        smtpObj.sendmail(smtp_sender, smtp_receiver, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"

    try:
        event.subscribers.append(user)
        session.commit()
        return jsonify(event.serialize)
    except:
        return jsonify({'result': False})


@app.route('/events/<int:event_id>/unsubscribe', methods=['POST'])
def unsubscribe(event_id):
    """unsubscribe a user from an event"""
    user_email = request.json['email']
    try:
        event = session.query(Event).filter_by(id=event_id).one()
        user = session.query(User).filter_by(email=user_email).one()
    except:
        abort(404, "eventId or user email not found.")

    try:
        event.subscribers.remove(user)
        session.commit()
        return jsonify(event.serialize)
    except:
        return jsonify({'result': False})


@app.route('/')
@app.route('/events', methods=['GET'])
def listEvents():
    """list all events"""
    events = session.query(Event).all()
    return jsonify(events=[event.serialize for event in events])


@app.route('/users', methods=['GET'])
def listUsers():
    """list all users"""
    users = session.query(User).all()
    return jsonify(users=[user.serialize for user in users])


@app.route('/users', methods=['POST'])
def createUser():
    """Create a new user"""
    email = request.json['email']
    if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
        abort(400, "Invalid email address.")
    try:
        newUser = User(email=email)
        session.add(newUser)
        session.commit()
        return jsonify(newUser.serialize), 201
    except:
        abort(400)


@app.route('/users', methods=['DELETE'])
def deleteUser():
    """Delete a user"""
    try:
        user = session.query(User).filter_by(email=request.json['email']).one()
        session.delete(user)
        session.commit()
        return jsonify({'result': True})
    except:
        return jsonify({'result': False})


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
