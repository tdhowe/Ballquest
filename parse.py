import csv
from Ballquest import *

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

            


__main("BallQuest.csv")
