from datetime import datetime
from flask import Flask, jsonify, request, render_template
import json
from post import Post
from functions import get_all_posts,get_max_id, get_all_comments, get_max_comment_id
from comment import Comment
from network import *
from multicast import *


app = Flask(__name__)
global network_instance
network_instance = Network()

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
    print(posts)

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
    return render_template('index.html', posts = posts)

@app.route('/update-users', methods=['POST'])
def update_users():
    users_string = request.data
    users_json = json.loads(users_string)
    with open('users.json', 'w') as file:
        json.dump(users_json, file)
    return '', 200

def heartbeat():
    #Instanz Network + Multicast
    server = Network()
    multicastclient = multicast.MulticastClient('224.0.0.100', ('224.0.0.100', 10000))
    #Send multicast (Heartbeat)
    multicastclient.send_message(server)
    #Listen to Multicast (Heartbeat)
    multicastclient.start(server)
    #Check First Host
    server.check_first_host()
    print(str(server.leader) + " ist leader")
    #
    print(server.replication_network)


if __name__ == '__main__':
    # Start der Flask-App in einem Thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': network_instance.get_ownip(), 'port': 5000})
    flask_thread.start()

    # Ausführung des zusätzlichen Codes in einem anderen Thread
    additional_thread = threading.Thread(target=heartbeat())
    additional_thread.start()

    # Warte, bis die Flask-App beendet wird
    flask_thread.join()



