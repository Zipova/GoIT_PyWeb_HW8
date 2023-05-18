import re
import redis
from redis_lru import RedisLRU

from models import Quote, Author


client = redis.Redis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)


def main():
    print('What do you want to find?')
    while True:
        user_input = input('>>>').strip()
        if user_input == 'exit':
            break
        command, value = user_input.split(':')
        if command == 'tag':
            print(find_tag(value))
        elif command == 'tags':
            print(find_tags(value))
        elif command == 'name':
            print(find_name(value))
        else:
            print('Unknown command')


@cache
def find_tag(value):
    regex = re.compile(f'{value}.*')
    quotes = Quote.objects(tags=regex)
    for quote in quotes:
        return f'{quote.quote}'


def find_tags(value):
    tags = value.split(',')
    for tag in tags:
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            return f'{quote.quote}'


@cache
def find_name(value):
    try:
        author = Author.objects(fullname__istartswith=value.strip())
        quotes = Quote.objects(author=author[0].id)
        for quote in quotes:
            return f'{quote.quote}'
    except IndexError:
        return 'Wrong name'


if __name__ == '__main__':
    main()
