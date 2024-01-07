import json

def get_all_posts():
    f = open("users.json")
    posts = json.load(f)

    f.close()
    return posts

def get_all_comments(post_id):
    with open('users.json', 'r') as json_file:
        posts = json.load(json_file)
        target_key = 'post_comments'

        for post in posts:
            if int(post["post_id"]) == int(post_id):
                if target_key in post:
                    return post[target_key]
                else:
                    print(f"The key '{target_key}' was not found.")
                    return None


def get_max_id():
    posts = get_all_posts()
    if not posts:
        return 1
    max_id = max(entry['post_id'] for entry in posts)
    #print(max_id)
    return int(max_id) + 1

def get_max_comment_id(post_id):
    comments = get_all_comments(post_id)
    if not comments:
        return 1
    max_id = max(entry['comment_id'] for entry in comments)
    return int(max_id) + 1
