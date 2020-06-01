from gensim.summarization.summarizer import summarize

class Document():
#  2.1
  def __init__(self, json):
    self.json = json
    self.type = None

# 3.4 Here is the type getter is set
  def get_type(self):
    return self.type

# cet setter permet de change le document
  def set_json(self, json):
    for key in json:
      self.json[key] = json[key] if self.json[key] is not None else None

  def __json__(self):
    return {
      'titre': self.json['titre'],
      'date': self.json['date'],
      'url': self.json['url'],
      'text': self.json['text']
    }

# 2.2
# on ecrase la method str pour fournire l'information qu'on a besoin (p.e. pour print operateur)
  def __str__(self):
    return f'Document: {self.json["title"]}'

# 2.8
# on ecrase la method repr pour fournire l'information qu'on a besoin
  def __repr__(self):
    return f'Doc title: {self.json["title"]}, release date: {self.json["date"]}'

  # 4.3
  def summarize_me(self):
    return summarize(self.json['text'])


# 3.1
class RedditDocument(Document):
# 3.1  on appelle le constructeur pour initialiser cette class
  def __init__(self, title, text, doc):
    json = {'title': title, 'date': doc['date'], 'url': doc['url'], 'text': text}
# ici nous appellons le method __init__ of parent
    super().__init__(json)
    self.ncomment = doc['num_comments']
    self.author = doc['author']
    self.type = 'reddit'

  def increment_ncomment(self):
    self.ncomment += 1

  def get_ncomment(self):
    return f'Comment quantity: {self.ncomment}'

  @staticmethod
  def get_text_key():
    return 'body'


# 3.2
class ArxivDocument(Document):
# 3.2  on appelle le constructeur pour initialiser cette class
  def __init__(self, title, text, doc):
    json = {'title': title, 'date': doc['published'], 'url': doc['link'], 'text': text}
    # ici nous appellons le method __init__ of parent
    super().__init__(json)
    authors = doc['author']
    self.authors = [a['name'] for a in authors] if len(authors) != 1 else [authors['name']]
    self.type = 'arxiv'

  def add_coauthors(self, aut):
    self.authors.append(aut)

  def get_authors(self):
    return f'Author list: {self.authors}'

  @staticmethod
  def get_text_key():
    return 'summary'
