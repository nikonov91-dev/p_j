import re, pickle


class Document():
  def __init__(self, json=None):
    if json is None:
      json = {
        'titre': '',
        'auteur': '',
        'date': '',
        'url': '',
        'text': ''
      }
    self.json = json

  def set_json(self, json):
    for key in json:
      self.json[key] = json[key] if self.json[key] is not None else None

  def __json__(self):
    return {
      'titre': self.json['titre'],
      'auteur': self.json['auteur'],
      'date': self.json['date'],
      'url': self.json['url'],
      'text': self.json['text']
    }

  def __str__(self):
    return self.json.titre

  def __repr__(self):
    return f'Doc title: {self.json["title"]}, release date: {self.json["date"]}'


class Author():
  def __init__(self, name, id):
    self.id = id
    self.name = name
    self.ndoc = 0
    self.production = {}

  def addDoc(self):
    self.ndoc += 1

  def set_production(self, doc):
    self.production[doc['title']] = doc['id']

  def get_production(self):
    return self.production


class Corpus():
  def __init__(self):
    self.authors = {}
    self.id2aut = {}
    self.collection = {}
    self.id2doc = {}
    self.naut = 0
    self.ndoc = 0

  def proceed_docs(self, parsed_docs):
    for doc in parsed_docs:
      for author in doc['author']:
        if isinstance(author, dict):
          name_ = author['name']
          if not (name_ in self.authors):
            self.authors[name_] = Author(name_, self.naut)
            self.id2aut[self.naut] = name_
            self.naut += 1

    for doc in parsed_docs:
      peeled_title = ' '.join(re.findall(r'\w+', doc['title']))
      self.collection[peeled_title] = Document({'title': peeled_title, 'date': doc['updated'], 'author': doc['author'], 'url': doc['link'], 'text': doc['summary']})
      self.id2doc[self.ndoc] = peeled_title
      for author in doc['author']:
        if isinstance(author, dict):
          name_ = author['name']
          self.authors[name_].addDoc()
          self.authors[name_].set_production({'id': self.ndoc, 'title': doc['title']})
      self.ndoc += 1

  def get_doc_list_of_number(self, n=10):
    docs = []
    for i in range(n):
      title = self.id2doc[i]
      doc = self.collection[title]
      docs.append(doc.__repr__())
    return docs

  def save(self):
    with open('corpus.pickle', 'wb') as f:
      pickle.dump(self, f)

  def load(self):
    with open('corpus.pickle', 'rb') as f:
      self = pickle.load(f)


class RedditDocument(Document):
  def __init__(self):
    super().__init__()

  def dosmth(self):
    pass


class ArxivDocument(Document):
  def dosmth(self):
    pass