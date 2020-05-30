import pickle

from models import Corpus
from arvix_api import request_and_parse_from_arxiv


corpus = Corpus('arvix', request_and_parse_from_arxiv())
print(corpus.get_doc_list_of_number(2))

#3.3 New functionality testing from 3th part
corpus.add_author_to_doc('AlexNikonov', 3)
print(corpus.get_doc_by_id(3).get_authors())
corpus.add_author_to_doc('AlexNikonov', 3)

#2.9
# corpus.save()
# del corpus
#
# with open('corpus.pickle', 'rb') as f:
#   corpus_revived = pickle.load(f)
# corpus_revived.get_doc_list_of_number(4)
