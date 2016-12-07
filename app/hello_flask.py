#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:hello_flask.py

import sys
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


reload(sys)
sys.setdefaultencoding('utf8')


class NameForm(FlaskForm):
    name = StringField(u'你的名字？', validators=[DataRequired()])
    submit = SubmitField(u'提交')


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'never to guess str LL'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Patent(db.Model):
    __tablename__ = 'patents'
    id = db.Column(db.Integer, primary_key=True)
    pub_id = db.Column(db.String)
    pub_date = db.Column(db.String)
    app_type = db.Column(db.String)
    app_id = db.Column(db.String)
    app_date = db.Column(db.String)
    title = db.Column(db.String)
    abstract = db.Column(db.String)

    def __repr__(self):
        return "< Patent(pub_id='%s', pub_date='%s', app_type='%s'," +\
               " app_id='%s', app_date='%s', title='%s', abstract='%s') >" % (
                        self.pub_id, self.pub_date, self.app_type, self.app_id,
                        self.app_date, self.title, self.abstract)


class Assignee(db.Model):
    __tablename__ = 'assignees'
    id = db.Column(db.Integer, primary_key=True)
    assignee = db.Column(db.String)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'))

    patent = db.relationship("Patent", back_populates="assignees")

    def __repr__(self):
        return "< Assignee(assignee='%s') >" % self.assignee

Patent.assignees = db.relationship("Assignee", order_by=Assignee.id,
                                   back_populates="patent")


class Inventor(db.Model):
    __tablename__ = 'inventors'
    id = db.Column(db.Integer, primary_key=True)
    inventor = db.Column(db.String)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'))

    patent = db.relationship("Patent", back_populates="inventors")


Patent.inventors = db.relationship("Inventor", order_by=Inventor.id,
                                   back_populates="patent")


class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    agent = db.Column(db.String)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'))

    patent = db.relationship("Patent", back_populates="agents")


Patent.agents = db.relationship("Agent", order_by=Agent.id,
                                back_populates="patent")


class Description(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'))

    patent = db.relationship("Patent", back_populates="descriptions")


Patent.descriptions = db.relationship("Description", order_by=Description.id,
                                      back_populates="patent")


class Claim(db.Model):
    __tablename__ = 'claims'
    id = db.Column(db.Integer, primary_key=True)
    claim = db.Column(db.String)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'))

    patent = db.relationship("Patent", back_populates="claims")


Patent.claims = db.relationship("Claim", order_by=Claim.id,
                                back_populates="patent")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        session['known'] = False
        patent = Patent.query.order_by(Patent.title).first()
        if old_name is not None and old_name != form.name.data:
            flash(patent.pub_id)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
