import pickle

from models.corpus import Corpus
from api_services.reddit_api import request_and_parse_docs


corpus = Corpus('reddit', request_and_parse_docs())
print(corpus.get_doc_list_of_number(2))

#3.3 New functionality testing from 3th part
print(corpus.get_doc_by_id(3).get_ncomment())
corpus.get_doc_by_id(3).increment_ncomment()
print(corpus.get_doc_by_id(3).get_ncomment())


# 2.9
corpus.save()
del corpus

# Pandant le cours je vous ai explique non correctement pourquoi je n'ai pas pu charger mon pickle enregistré
# mon problem etait que j'ai cree le pickle load comme une method de la class Corpus
# mais j'ai du charger le pickle enregistré à l'exterieur de la class sans creation de l'instance nouveaux

corpus_revived = None
print(' ---------------- revived corpus ------------------')
with open('corpus.pickle', 'rb') as f:
  corpus_revived = pickle.load(f)
print(corpus_revived.get_doc_list_of_number(4))