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


@app.route('/signup')
def gosignup():
    return render_template("signup.html")


@app.route('/mentormatch')
def gomatchmentor():
    return render_template("mentormatch.html")


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
