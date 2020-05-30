# 1.2
import requests, xmltodict, urllib, re

res = requests.get("http://export.arxiv.org/api/query?search_query=all:france&start=0&max_results=10")

dictt = xmltodict.parse(res.content)


# print(json.dumps(dictt, indent=4))
# 1.2 Quels sont les champs disponibles ?
# id, updated, published, title, summary, author, arxiv, link, arxiv, category,

# 1.2 Quel est le champ contenant le contenu textuel ?
# title, summary

# 1.3
def request_and_parse_from_arxiv(query='covid'):
  url = "http://export.arxiv.org/api/query?search_query=all:" + query + "&start=0&max_results=10"
  result = urllib.request.urlopen(url).read().decode()
  parsedResult = xmltodict.parse(result)
  return parsedResult['feed']['entry']


docs = request_and_parse_from_arxiv()
splitted_words = []
splitted_phrases = []
for doc in docs:
  summary_ = doc['summary']
  if len(summary_) < 100:
    continue
  splitted_words.append(re.findall(r'\w+', summary_))
  splitted_phrases.append(summary_.split('.'))

print(splitted_words)
print(splitted_phrases)

joined_phases = ' '.join([' '.join(x) for x in splitted_phrases])
print(joined_phases)
