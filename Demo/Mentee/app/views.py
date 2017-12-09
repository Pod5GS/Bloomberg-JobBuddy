# -*- coding:utf-8 -*-
from flask import render_template, request, jsonify
from app import app
from app import socketio
from flask_socketio import emit
from services import getRecommendation


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/mentorindex')
def mentorindex():
    return render_template("mentorindex.html")


@app.route('/signup')
def gosignup():
    head1 = "Tell us a bit more about your interests"
    subhead1 = "We'll connect you to the professionals that match your need.<br/>Click the interest to choose, hold to learn more."
    head2 = "Select what you are interested to learn"
    subhead2 = "You can come back and edit any time"
    return render_template("signup.html", head1=head1, subhead1=subhead1, head2=head2, subhead2=subhead2, type="mentee")

@app.route('/mentorsignup')
def gomentorsignup():
    head1 = "Tell us a bit more about your career field"
    subhead1 = "We'll connect you to the mentees that you can help the most.<br/>Click the interest to choose, hold to learn more."
    head2 = "Select what you are interested to teach"
    subhead2 = "You can come back and edit any time"
    return render_template("signup.html", head1=head1, subhead1=subhead1, head2=head2, subhead2=subhead2, type="mentor")

@app.route('/events')
def goevents():
    return render_template("events.html")


@app.route('/events2')
def goevents2():
    return render_template("events2.html")


@app.route('/schedule')
def goschedule():
    return render_template("schedule.html")


@app.route('/videochat')
def govideochat():
    return render_template("videochat.html")


@app.route('/endchat')
def goendchat():
    return render_template("endchat.html")


@app.route('/fakechat')
def gofakechat():
    return render_template("fakechat.html")


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_profile = [data['menteeId'], data['menteeGender'], data['menteeEducation'], data['menteeLocation'],
                    data['menteeInterests']]
    mentors = getRecommendation(user_profile, 3)
    return jsonify(results=mentors)


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data'], 'type': message['type']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
