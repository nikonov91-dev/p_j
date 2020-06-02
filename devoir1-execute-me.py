# 1.1
from api_services.arvix_api import request_and_parse_docs as arvix
from api_services.reddit_api import request_and_parse_docs as reddit

#ici Comment ca march est claire.
reddit_posts = reddit()

arvix_posts = arvix()

print('reddit_posts')
print(reddit_posts)
print('_______________________________________________')
print('arvix_posts')
print(arvix_posts)