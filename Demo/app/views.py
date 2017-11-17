# -*- coding:utf-8 -*-
from flask import render_template, request, jsonify
from app import app
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

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_profile = [data['menteeId'], data['menteeGender'], data['menteeEducation'], data['menteeLocation'], data['menteeInterests']]
    mentors = getRecommendation(user_profile, 3)
    return jsonify(results=mentors)
