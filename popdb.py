import json
from home.models import Post
with open('posts.json') as f:
    posts = json.load(f)

for post in posts:
    post = Post(author=post['author'], link=post['link'], title=post['title'], content=post['content'], slug=post['slug'])
    post.save()