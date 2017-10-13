# -*- coding:utf-8 -*-
from flask import render_template, request
from app import app
from services import getRecommendation


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_profile = [data['menteeId'], data['menteeGender'], data['menteeEducation'], data['menteeLocation'], data['menteeInterests']]
    results = getRecommendation(user_profile, 5)
    print results
