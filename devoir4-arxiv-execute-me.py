from models.corpus import Corpus
from api_services.arvix_api import request_and_parse_docs


corpus = Corpus('arvix', request_and_parse_docs())

corpus.get_doc_by_id(0)

print(corpus.get_stats())