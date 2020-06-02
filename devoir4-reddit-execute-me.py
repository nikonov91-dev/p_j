from models.corpus import Corpus
from api_services.reddit_api import request_and_parse_docs


corpus = Corpus('reddit', request_and_parse_docs())

corpus.get_doc_by_id(0)
print('')
print('-------le statistique des mots triée par l"occurance de mot dans un doc-------')
print(corpus.get_stats())
print('')
print('-------Concordacier de mot trouvant dans le context----------')
print(corpus.get_concordancier(0))