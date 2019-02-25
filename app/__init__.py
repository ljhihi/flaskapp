#coding:utf8
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ljhihi:ljhihi198992@ljhihi.mysql.pythonanywhere-services.com/ljhihi$default"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] ='de8437235dff4aef8ce4029f29325bf6'
app.config['UP_DIR'] = "/home/ljhihi/books/app/static/uploads"
# app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("home/404.html"),500