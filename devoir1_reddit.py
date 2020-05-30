# 1.1
import praw
import pandas as pd

def request_and_parse_posts_from_reddit():
  posts = []
  reddit = praw.Reddit(client_id="LsMk6MaIGpRvmg",
                       client_secret="iWddliZYW8mHJVEAuP4n_1R_rps",
                       user_agent="my user agent")

  for post in reddit.subreddit("coronavirus").hot(limit=10):
    # 1.1 Quels sont les champs disponibles
    # 1.1 Alimentez la liste docs avec ce texte uniquement. Vous pouvez d ́ej`a vous d ́ebarrasser des sauts de ligne (\n) en les rempla ̧cant par des espaces.
    converted = post.selftext.replace('\n', ' ')
    posts.append([post.title, post.author.name, post.score, post.id, post.subreddit, post.url, post.num_comments, converted, post.created])
  # 1.1 Quel est le champ contenant le contenu textuel : tout sauf subreddit

  csv = pd.DataFrame(posts, columns=['title', 'author', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
  return csv