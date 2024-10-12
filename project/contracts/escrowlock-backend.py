# app.py
from flask import Flask, jsonify, request
from models import db, Escrow
from utils import interact_with_contract

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escrowlock.db'
db.init_app(app)

@app.route('/create_escrow', methods=['POST'])
def create_escrow():
    data = request.json
    buyer = data['buyer']
    amount = data['amount']
    
    # Interact with the smart contract
    result = interact_with_contract('create-escrow', [buyer, amount])
    
    if result['success']:
        escrow_id = result['data']
        new_escrow = Escrow(id=escrow_id, buyer=buyer, amount=amount, state='created')
        db.session.add(new_escrow)
        db.session.commit()
        return jsonify({'success': True, 'escrow_id': escrow_id}), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@app.route('/fund_escrow/<int:escrow_id>', methods=['POST'])
def fund_escrow(escrow_id):
    # Interact with the smart contract
    result = interact_with_contract('fund-escrow', [escrow_id])
    
    if result['success']:
        escrow = Escrow.query.get(escrow_id)
        escrow.state = 'funded'
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@app.route('/release_escrow/<int:escrow_id>', methods=['POST'])
def release_escrow(escrow_id):
    # Interact with the smart contract
    result = interact_with_contract('release-escrow', [escrow_id])
    
    if result['success']:
        escrow = Escrow.query.get(escrow_id)
        escrow.state = 'completed'
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@app.route('/get_escrow/<int:escrow_id>', methods=['GET'])
def get_escrow(escrow_id):
    escrow = Escrow.query.get(escrow_id)
    if escrow:
        return jsonify({
            'id': escrow.id,
            'buyer': escrow.buyer,
            'amount': escrow.amount,
            'state': escrow.state
        }), 200
    else:
        return jsonify({'error': 'Escrow not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Escrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(42), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(20), nullable=False)

# utils.py
import requests

def interact_with_contract(function, args):
    # This is a placeholder function. In a real implementation, you would
    # interact with the Stacks blockchain using the appropriate SDK or API.
    # For now, we'll just return a mock successful result.
    return {
        'success': True,
        'data': 1  # Mock escrow ID
    }