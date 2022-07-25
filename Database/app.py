# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from werkzeug.utils import secure_filename
# from db import db_init, db
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db_init(app)
#
#
# class Img(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.Text, unique=True, nullable=False)
#     name = db.Column(db.Text, nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     pic = request.files['pic']
#
#     if not pic:
#         return 'No pic uploaded', 400
#
#     filename = secure_filename(pic.filename)
#     mimetype = pic.mimetype
#     img = Img(img=pic.read(), mimetype=mimetype, name=filename)
#     db.session.add(img)
#     db.session.commit()
#
#     return 'Img har been uploaded', 200


from flask import Flask, request, Response
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Img

app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
