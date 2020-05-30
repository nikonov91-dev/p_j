from collections import defaultdict

selector = defaultdict(lambda: 'неизвестно',
                       {'a': 1,
                        'b': 'text',
                        'c': 'cc',
                        'd': 'ddd'})
print(selector['a'])
print(selector['d']('test'))