#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, session, redirect, url_for, flash
from model import Patent
from forms import NameForm


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
