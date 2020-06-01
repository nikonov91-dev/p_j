import re, pickle
import pandas as pd
from collections import defaultdict
from models.documents import RedditDocument, ArxivDocument
from models.author import Author


# 3.5 Factory
# on utilise defaultdict comme un switheur en depandant de valeur passé
# il y a besoin de lambda: 'undefined' parce que le defaultdict attandant une fonction comme le premier argument
# s'il mode fourne une autre cle (non 'reddit', non 'arvix') le defaultdict levera l'exception
class DocFactory():
  @staticmethod
  def generate_goc(mode):
    return defaultdict(lambda: 'undefined', {
      'reddit': RedditDocument,
      'arvix': ArxivDocument
    })[mode]


# 2.7
class Corpus():
  def __init__(self, mode, parsed_docs):
    # 2.3
    self.collection = {}
    self.id2doc = {}
    # 2.6
    self.authors = {}
    self.id2aut = {}
    self.naut = 0
    self.ndoc = 0
    # ici on courons l'usine et
    self.doc_instance = DocFactory.generate_goc(mode)
    # on prepare tout les variable qu'on a besoin
    # 4.5 on utilise Set pour facilement eviter les doublons
    self.dictionary = set()
    # 4.4
    self.concordancier = pd.DataFrame(columns=['word', 'contexte gauche', 'motif trouve', 'contexte droit'])
    # 4.3-4.6-4.7 on enregistre les mots occurance et le numbre d'occurrences
    self.stats = pd.DataFrame(columns=['word', 'frequance_de_mot_par_tout', 'frequance_de_mot_par_docs'])
    self.proceed_docs(parsed_docs)

  # Cette fonction est basique de Corpus pour initiate lui-meme
  def proceed_docs(self, parsed_docs):
    for doc in parsed_docs:
      # 1.3
      raw_text = doc[self.doc_instance.get_text_key()]
      text, text_as_separate_words = self.nettoyer_texte(raw_text)
      # on affiche la taille de la document
      print(len(text))
      # voici on verifie si la document et long de 100 mots, si pas - on le saute
      if len(text) < 100:
        continue

      self._concorde(text_as_separate_words, text)

      peeled_title = ' '.join(re.findall(r'\w+', doc['title']))
      self.collection[peeled_title] = self.doc_instance(peeled_title, text, doc)
      self.id2doc[self.ndoc] = peeled_title

      for author in doc['author']:
        if isinstance(author, dict):
          name_ = author['name']
          self.add_author(name_)
          self.authors[name_].increment_ndoc()
          self.authors[name_].set_production({'id': self.ndoc, 'title': peeled_title})
      # ici on ajoute le quantité des doc qu'on a processés
      self.ndoc += 1

  def add_author(self, name_):
    # on controle l'author s'il deja exist à dictionnaires
    if not (name_ in self.authors):
      self.authors[name_] = Author(name_)
      self.id2aut[self.naut] = name_
      self.naut += 1
    # si Oui on eleve un Exception personnalisee
    else:
      raise AuthorError(name_)

# 4.4
  def nettoyer_texte(self, raw_text):
    # tout les lines nouvelles sont remplacées
    raw_text = raw_text.lower().replace('\n', ' ')
    # et le text est separé aux sentences
    split_sentences = re.split(r' *[\.\?!][\'"\)\]]* *', raw_text)
    text_as_separate_words = []
    for s in split_sentences:
      # on trouve tout les mots et chiffres par \w+ parceque la date est un chiffre et il peut etre une cle (p.e. 1789)
      text_as_separate_words.append(re.findall(r'\w+', s))
    # les mots separe se reunissent dans sentence et en fin au text
    text = '. '.join([' '.join(x) for x in text_as_separate_words])
    return text, text_as_separate_words

  # 4.1
  def _search(self, word, text):
    # on trouve le mot et son location dans le text
    result = re.search(word, text, re.IGNORECASE)
    return word, text[0: result.start()], text, text[result.end(): len(text)]

  # 4.2
  def _concorde(self, text_as_separate_words, genuine_text):
    j = -1
    for i, sentence_as_separate_words in enumerate(text_as_separate_words):
      self.dictionary.update(sentence_as_separate_words)
      for w in sentence_as_separate_words:
        words_csv = self._search(w, genuine_text)
        self.concordancier.loc[len(self.concordancier)] = words_csv

        # Pour conter le nombre de documents contenant chacun des mots et mot meme frequance
        # on fait:
        # - inspect si le mot est deja au tableau
        # - et si on passe le meme sentance une fois plus
        is_not_exist = w not in self.stats['word'].values
        is_one_and_the_same_sentence = j == i
        if is_not_exist:
          self.add_word_to_stats(w)
        else:
          if is_one_and_the_same_sentence:
            self.update_word_frequency_stats(w)
          else:
            self.update_docs_frequency_stats(w)
        j = i

  def add_word_to_stats(self, word):
    self.stats.loc[len(self.concordancier)] = [word, 1, 1]

# 4.3
  def update_word_frequency_stats(self, word):
    frequance_par_tout = 'frequance_de_mot_par_tout'
    self.stats.loc[(self.stats.word == word), frequance_par_tout] = self.stats.loc[(self.stats.word == word), frequance_par_tout].values[0] + 1

# 4.7
  def update_docs_frequency_stats(self, word):
    self.update_word_frequency_stats(word)
    frequance_par_docs = 'frequance_de_mot_par_docs'
    self.stats.loc[(self.stats.word == word), frequance_par_docs] = self.stats.loc[(self.stats.word == word), frequance_par_docs].values[0] + 1

  # 4.3
  def get_stats(self, n=10):
    count = len(self.stats)
    # sorted = self.stats.sort_values(by=['frequance_de_mot_par_tout'])[:n]
    sorted = self.stats.sort_values(by=['frequance_de_mot_par_tout'], ascending=False)[:n]
    return count, sorted

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
    self.add_author(name)
    title = self.id2doc[doc_id]
    self.collection[title].add_coauthors(name)

  def get_doc_by_id(self, id):
    title = self.id2doc[id]
    return self.collection[title]


class AuthorError(Exception):
  def __init__(self, author):
    super().__init__(f'Author "{author}" already exists in the author list of this document.')
