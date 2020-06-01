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
def request_and_parse_docs(query='covid'):
  url = "http://export.arxiv.org/api/query?search_query=all:" + query + "&start=0&max_results=10"
  result = urllib.request.urlopen(url).read().decode()
#le resultat est xml type ce pour ca il faul le covertir au dictionnair
  parsedResult = xmltodict.parse(result)
  return parsedResult['feed']['entry']
