from datetime import datetime
from flask import Flask, jsonify, request, render_template, redirect
import json
from post import Post
from functions import get_all_posts,get_max_id, get_all_comments, get_max_comment_id
from comment import Comment
from network import *
from multicast import *


app = Flask(__name__)
server = Network()

@app.route('/', methods=['GET'])
def home():
    posts = get_all_posts()

    return render_template('index.html', posts=posts)

@app.route('/posts', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        new_post = Post(
            get_max_id(),
            request.form['content'],
            str(datetime.now().day) + '.' + str(datetime.now().month) + '.' + str(
                datetime.now().year) + '  ' + datetime.now().strftime("%H:%M:%S"),
            [],
        )
        new_post.safe_in_Jsonfile("users.json")
    posts = get_all_posts()

    server.update_Json()

    return render_template('index.html', posts = posts)

@app.route('/comments/<post_id>', methods=['GET','POST'])
def updateComments(post_id):
    if request.method == 'POST':
        new_comment = Comment(
            get_max_comment_id(post_id),
            request.form['comment_content'],
            str(datetime.now().day) + '.' + str(datetime.now().month) + '.' + str(
                datetime.now().year) + '  ' + datetime.now().strftime("%H:%M:%S")
        )
        new_comment.safe_comment_in_Json_file("users.json",post_id)
    posts = get_all_posts()

    server.update_Json()

    return render_template('index.html', posts = posts)

@app.route('/update-users', methods=['POST'])
def update_users():
    users_string = request.data
    users_json = json.loads(users_string)
    with open('users.json', 'w') as file:
        json.dump(users_json, file)
    return '', 200


@app.route('/redirect')
def redirect_to_new_ip():
    # Specify the new IP address and the endpoint to redirect to
    new_ip_address = server.leader  # Replace this with the desired IP
    new_endpoint = ':5000'  # Replace this with the desired endpoint

    # Redirect the client to the new IP address and endpoint
    return redirect(f'http://{new_ip_address}{new_endpoint}', code=302)

def heartbeat():
    multicastclient = multicast.MulticastClient('224.0.0.100', ('224.0.0.100', 10000))
    #Send multicast (Heartbeat)
    multicastclient.send_message(server)
    #Listen to Multicast (Heartbeat)
    multicastclient.start(server)
    #Check First Host
    server.check_first_host()
    #print(str(server.leader) + " ist leader")
    #print(server.replication_network)


if __name__ == '__main__':
    # Ausführung des zusätzlichen Codes in einem anderen Thread
    additional_thread = threading.Thread(target=heartbeat())
    additional_thread.start()

    # Start der Flask-App in einem Thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': server.leader, 'port': 5000})
    flask_thread.start()

    # Warte, bis die Flask-App beendet wird
    flask_thread.join()



