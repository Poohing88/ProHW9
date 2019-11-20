import csv
import re
from pymongo import MongoClient
from pprint import pprint


client = MongoClient()
concert_db = client['concert_db']
ticets_colection = concert_db['ticets']


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    data = []
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        for line in reader:
            data.append({
                'artist': line['Исполнитель'],
                'price': int(line['Цена']),
                'place': line['Место'],
                'date': line['Дата']
            })
        db.ticets.insert_many(data)


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    price_sort = list(db.ticets.find().sort('price'))
    return price_sort


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """
    regex = re.compile(f'({name}[а-яА-Я\w\-\s]*)')
    find_name = list(db.ticets.find().sort('price'))
    names = []
    for artists in find_name:
        key = artists.get('artist')
        key = str(key)
        find_artist = regex.findall(key)
        if find_artist:
            names.append(artists)
    return names


if __name__ == '__main__':
    read_data('artists.csv', concert_db)
    print("Сортированные по цене билеты:")
    pprint(find_cheapest(concert_db))
    print('Билеты на концерт того исполнителя что искали:')
    pprint(find_by_name('T', concert_db))
