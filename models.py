import re, pickle
from collections import defaultdict


class Document():
  def __init__(self, json=None):
    if json is None:
      json = {
        'titre': '',
        'date': '',
        'url': '',
        'text': ''
      }
    self.json = json
    self.type = None

#3.4 Here is the type getter is set
  def get_type(self):
    return self.type

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

  def __str__(self):
    return f'Document: {self.json["title"]}'

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
  def __init__(self, mode, parsed_docs):
    self.mode = mode
    self.authors = {}
    self.id2aut = {}
    self.collection = {}
    self.id2doc = {}
    self.naut = 0
    self.ndoc = 0
    self.proceed_docs(parsed_docs)

  def _add_author(self, name):
    if not (name in self.authors):
      self.authors[name] = Author(name, self.naut)
      self.id2aut[self.naut] = name
      self.naut += 1
    else:
      raise AuthorError(name)

  def proceed_docs(self, parsed_docs):
    for doc in parsed_docs:

      for author in doc['author']:
        if isinstance(author, dict):
          self._add_author(author['name'])

      peeled_title = ' '.join(re.findall(r'\w+', doc['title']))
      self.collection[peeled_title] = DocFactory.generate_goc(self.mode)(peeled_title, doc)
      self.id2doc[self.ndoc] = peeled_title

      for author in doc['author']:
        if isinstance(author, dict):
          name_ = author['name']
          self.authors[name_].addDoc()
          self.authors[name_].set_production({'id': self.ndoc, 'title': (peeled_title)})
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

  def add_author_to_doc(self, name, doc_id):
    self._add_author(name)
    title = self.id2doc[doc_id]
    self.collection[title].add_coauthors(name)

  def get_doc_by_id(self, id):
    title = self.id2doc[id]
    return self.collection[title]


class AuthorError(Exception):
  def __init__(self, author):
    super().__init__(f'Author "{author}" already exists in the author list of this document.')


#3.5 Factory
class DocFactory():
  @staticmethod
  def generate_goc(mode):
    return defaultdict(lambda: 'undefined', {
      'reddit': RedditDocument,
      'arvix': ArxivDocument
    })[mode]


# 3.1
class RedditDocument(Document):
  def __init__(self, title, doc):
    # ici nous appellons le method __init__ of parent
    json = {'title': title, 'date': doc['date'], 'url': doc['url'], 'text': doc['body']}
    super().__init__(json)
    self.ncomment = doc['num_comments']
    self.author = doc['author']
    self.type = 'reddit'

  def increment_ncomment(self):
    self.ncomment += 1

  def get_ncomment(self):
    return f'Comment quantity: {self.ncomment}'


# 3.2
class ArxivDocument(Document):
  def __init__(self, title, doc):
    # ici nous appellons le method __init__ of parent
    json = {'title': title, 'date': doc['published'], 'url': doc['link'], 'text': doc['summary']}
    super().__init__(json)
    authors = doc['author']
    self.authors = [a['name'] for a in authors] if len(authors) != 1 else [authors['name']]
    self.type = 'arxiv'

  def add_coauthors(self, aut):
    self.authors.append(aut)

  def get_authors(self):
    return f'Author list: {self.authors}'
