# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Escrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(42), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(20), nullable=False)