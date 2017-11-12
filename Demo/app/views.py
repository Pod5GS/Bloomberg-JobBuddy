# -*- coding:utf-8 -*-
from flask import render_template, request, jsonify
from app import app
from services import getRecommendation


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup')
def getsignup():
    return render_template("signup.html")

@app.route('/mentormatch')
def matchmentor():
    return render_template("mentormatch.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_profile = [data['menteeId'], data['menteeGender'], data['menteeEducation'], data['menteeLocation'], data['menteeInterests']]
    mentors = getRecommendation(user_profile, 3)
    return jsonify(results=mentors)
