import csv
from Ballquest import *

def __add_stat(card, row, name, optional):
    stat = row[name]

    if not optional or len(stat) > 0:
        if len(stat) is 0:
            stat = '0'
        card.add_stat(name, stat)

def __main(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            color = Color.from_string(row['Color'])
            slot = Slot.from_string(row['Slot'])
            card = Card(row['Name'], color, slot)

            special_type = SpecialType.from_string(row['Type'])

            if special_type is not None:
                card.add_type(special_type)

            __add_stat(card, row, 'Price', optional = False)
            __add_stat(card, row, 'Appeal', optional = False)
            __add_stat(card, row, 'Priority', optional = False)

            # Damage type needs to be appended to the value
            dmg = row['Damage']

            if len(dmg) > 0:
                dmg_type = row['Damage Type']
                dmg += dmg_type.lower()[0]
                card.add_stat('Damage', dmg)

            __add_stat(card, row, 'HP', optional = True)
            __add_stat(card, row, 'Capacity', optional = True)

            card.create_card()

__main("BallQuest.csv")
