# app.py
from flask import Flask, jsonify, request
from models import db, Escrow
from utils import interact_with_contract

# ... rest of the file remains the same