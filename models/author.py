
class Author():
# 2.4
  def __init__(self, name):
    self.name = name
    self.ndoc = 0
    self.production = {}

  def increment_ndoc(self):
    self.ndoc += 1

  def set_production(self, doc):
    self.production[doc['title']] = doc['id']

  def get_production(self):
    return self.production

# 2.5
# on ecrase la method str pour fournire l'information qu'on a besoin (p.e. pour print operateur)
  def __str__(self):
    return f'{self.name}'