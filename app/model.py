#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db


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
