import pickle

from models import Corpus
from reddit_api import request_and_parse_posts_from_reddit


corpus = Corpus('reddit', request_and_parse_posts_from_reddit())
print(corpus.get_doc_list_of_number(2))

#3.3 New functionality testing from 3th part
print(corpus.get_doc_by_id(3).get_ncomment())
corpus.get_doc_by_id(3).increment_ncomment()
print(corpus.get_doc_by_id(3).get_ncomment())


# corpus.save()
# del corpus
#
# with open('corpus.pickle', 'rb') as f:
#   corpus_revived = pickle.load(f)
#   corpus_revived.get_doc_list_of_number(4)