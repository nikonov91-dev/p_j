from models import Corpus
from devoir1_reddit import request_and_parse_posts_from_reddit


corpus = Corpus()
corpus.proceed_docs(request_and_parse_posts_from_reddit())
print(corpus.get_doc_list_of_number(2))

corpus.save();
del corpus

corpus_revived = Corpus()
corpus_revived.load()
# corpus_revived.get_doc_list_of_number(4)
