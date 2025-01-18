from re import sub

generator = lambda name: sub(r'([a-z])([A-Z])', r'\1-\2', name).lower()


print(generator('CreateUser'))