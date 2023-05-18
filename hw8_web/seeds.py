import json

from models import Author, Quote


with open('authors.json', 'r') as file:
    authors = json.load(file)

for author in authors:
    Author(fullname=author['fullname'],
           born_date=author['born_date'],
           born_location=author['born_location'],
           description=author['description']).save()

with open('quotes.json', 'r') as file:
    quotes = json.load(file)

for quote in quotes:
    author_q = Author.objects(fullname=quote['author'])
    tags = [tag for tag in quote['tags']]
    value = quote['quote'].replace('вЂњ', '“').replace('вЂќ', '”')
    Quote(tags=tags,
          author=author_q[0].id,
          quote=value).save()


