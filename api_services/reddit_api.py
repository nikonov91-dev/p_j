# 1.1
import praw
import pandas as pd


def request_and_parse_docs(query="home"):
  posts_csv = []
  posts = []
# ici on utilise nos credentials obtenu sur reddit
  reddit = praw.Reddit(client_id="LsMk6MaIGpRvmg",
                       client_secret="iWddliZYW8mHJVEAuP4n_1R_rps",
                       user_agent="ma")

# ici on fait l'iteration sur the post recu
  for post in reddit.subreddit(query).hot(limit=10):
    # 1.1 Quels sont les champs disponibles
# Il y a beaucoup des chapms mais les plus utilisable sont ecrits cidessous
    # 1.1 Alimentez la liste docs avec ce texte uniquement.
    # Vous pouvez d ́ej`a vous d ́ebarrasser des sauts de ligne (\n) en les rempla ̧
    # cant par des espaces.

    # Voici on remplace le character avec espace
    converted = post.selftext.replace('\n', ' ')
    posts_csv.append([post.title, post.author.name, post.score, post.id, post.subreddit, post.url, post.num_comments, converted, post.created])
    posts.append({'title': converted, 'author': post.author.name, 'body': converted, 'url': post.url, 'date': post.created, 'num_comments': post.num_comments})
  # 1.1 Quel est le champ contenant le contenu textuel : tout sauf subreddit
# cree un tableau par pandas
  columns = ['title', 'author', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created']
  csv = pd.DataFrame(posts_csv, columns=columns)
  return posts