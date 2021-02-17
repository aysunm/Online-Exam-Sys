from flask_login import UserMixin
from sqlalchemy import ForeignKey

from .__init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    role = db.Column(db.String(50))


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))


class UsersExams(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    exam_id = db.Column(db.Integer, ForeignKey('exam.id'))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.String(500))
    a = db.Column(db.String(250))
    b = db.Column(db.String(250))
    c = db.Column(db.String(250))
    d = db.Column(db.String(250))
    e = db.Column(db.String(250))
    exam_id = db.Column(db.Integer, ForeignKey('exam.id'))
    point = db.Column(db.Integer)
    true_answer = db.Column(db.String(1))


class UsersAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    question_id = db.Column(db.Integer, ForeignKey('question.id'))
    answer = db.Column(db.String(1))

