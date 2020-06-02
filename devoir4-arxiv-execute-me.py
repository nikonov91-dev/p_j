from models.corpus import Corpus
from api_services.arvix_api import request_and_parse_docs


corpus = Corpus('arvix', request_and_parse_docs())

corpus.get_doc_by_id(0)

print('-------le statistique des mots triée par l"occurance de mot dans un doc-------')
print(corpus.get_stats()[0])
print(corpus.get_stats()[1])

print('-------Concordacier de mot trouvant dans le context----------')
print(corpus.get_concordancier(3)[0])
print(corpus.get_concordancier(3)[1])

print('-------Le resumé de la text certain---------')
print(corpus.get_doc_by_id(4).summarize_me())