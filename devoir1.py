# 1.1
from devoir1_reddit import request_and_parse_posts_from_reddit
from devoir1_arxiv import request_and_parse_from_arxiv

reddit_posts = request_and_parse_posts_from_reddit()

arvix_posts = request_and_parse_from_arxiv()

print('reddit_posts')
print(reddit_posts)
print('_______________________________________________')
print('arvix_posts')
print(arvix_posts)