import json

class Comment:
    def __init__(self, comment_id, comment_content, comment_created_at):
        self.comment_id = comment_id
        self.comment_content = comment_content
        self.comment_created_at = comment_created_at

    def convert_to_Json(self):
        return(
            {
                "comment_id": self.comment_id,
                "comment_content": self.comment_content,
                "comment_created_at": self.comment_created_at
            }
        )

    def safe_comment_in_Json_file(self, filepath, post_id):
        new_comment = self.convert_to_Json()
        try:
            with open(filepath, 'r') as json_file:
                all_posts = json.load(json_file)
        except FileNotFoundError:
            all_posts = []

        for post in all_posts:
            if int(post["post_id"]) == int(post_id):
                print(post)
                post["post_comments"].append(new_comment)
                break

        with open(filepath, 'w') as json_file:
            json.dump(all_posts, json_file, indent=4)
        print(all_posts)
        #send Json to other backends


