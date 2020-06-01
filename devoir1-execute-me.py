# 1.1
from api_services.arvix_api import request_and_parse_docs

#ici Comment ca march est claire.
reddit_posts = request_and_parse_docs()

arvix_posts = request_and_parse_docs()

print('reddit_posts')
print(reddit_posts)
print('_______________________________________________')
print('arvix_posts')
print(arvix_posts)