import json

class Post:
    def __init__(self, post_id, post_content, post_created_at, post_comments):
        self.post_id = post_id
        self.post_content = post_content
        self.post_created_at = post_created_at
        self.post_comments = post_comments

    def convert_to_Json(self):
        return {
            "post_id": self.post_id,
            "post_content": self.post_content,
            "post_created_at": self.post_created_at,
            "post_comments": self.post_comments
        }

    def safe_in_Jsonfile(self, file_path):
        new_Post = self.convert_to_Json()
        #print(new_Post)

        try:
            with open(file_path, 'r') as json_file:
                existing_posts = json.load(json_file)
                #print(existing_posts)
        except FileNotFoundError:
            existing_posts = []

        existing_posts.append(new_Post)

        with open(file_path, 'w') as json_file:
            json.dump(existing_posts, json_file, indent=4)
            print(f"Data added to file: {file_path}")
        #send JSOn to other backends
