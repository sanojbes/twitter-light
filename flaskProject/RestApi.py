from flask import Flask, jsonify

app = Flask(__name__)

# Beispiel Benutzerdaten
users = {
    '1': {'post': 'Das ist ein Post'},
    '2': {'post': 'Das ist ein zweiter Posts'},
    # Weitere Benutzer ...
}

# Endpunkt, um alle Benutzerdaten abzurufen
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Endpunkt, um Daten eines bestimmten Benutzers abzurufen
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id])
    else:
        return jsonify({'error': 'User not found'}), 404

