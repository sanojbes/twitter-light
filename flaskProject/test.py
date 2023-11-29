@app.route('/users', methods=['GET'])
def get_users():
    users = getJson()
    return jsonify(users)

# Endpunkt, um Daten eines bestimmten Benutzers abzurufen
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    users = getJson()
    for post in users['Posts']:
        if post['ID'] == int(user_id):
            return jsonify(post)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/posts', methods=['POST'])
def createPost():
    # Die Daten aus dem POST-Antrag abrufen
    data = request.json
    max_id = countID()
    users = getJson()


    # Überprüfen, ob erforderliche Felder vorhanden sind
    if max_id not in data:
        return jsonify({'error': 'ID and Post are required'}), 400
    # Append the new data to the existing data
    users['Posts'].append(data)
    # Neue Daten zum Speicher hinzufügen
    with open('/Users/felixschussler/PycharmProjects/flaskProject/users.json', 'w') as f:
        json.dump(users['Posts'], f)
        # Write the updated data back to the file

    return 'Data written to file'


#Liest die users.json file ein
def getJson ():
    f = open('/Users/felixschussler/PycharmProjects/flaskProject/users.json')
    users = json.load(f)
    print(users)

    f.close()
    return users

#ID hochzählen
def countID():
    users = getJson()
    max_id = max(entry['ID'] for entry in users['Posts'])
    return max_id

#

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")



if __name__ == '__main__':
    socketio.run(app)

