from _datetime import datetime
from flask import Flask, jsonify, request, render_template
import json
from post import Post
from functions import get_all_posts,get_max_id, get_all_comments, get_max_comment_id
from comment import Comment

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    posts = get_all_posts()
    return render_template('index.html', posts = posts)

@app.route('/posts', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        new_post = Post(
            get_max_id(),
            request.form['content'],
            str(datetime.now().day) + '.' + str(datetime.now().month) + '.' + str(
                datetime.now().year) + '  ' + datetime.now().strftime("%H:%M"),
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
                datetime.now().year) + '  ' + datetime.now().strftime("%H:%M")
        )

        new_comment.safe_comment_in_Json_file("users.json",post_id)

    posts = get_all_posts()

    return render_template('index.html', posts = posts)

if __name__ == '__main__':
    app.run()
