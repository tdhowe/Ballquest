from Ballquest import *

def main():
    brown_card = Card("Test Brown Card", Color.BROWN, Slot.TRINKET)
    brown_card.add_type(SpecialType.BEAST)
    red_card = Card("Test Red Card", Color.RED, Slot.CHEST)
    blue_card = Card("Test Blue Card", Color.BLUE, Slot.HEAD)
    purple_card = Card("Test Purple Card", Color.PURPLE, Slot.BACK)
    purple_card.add_type(SpecialType.INSTRUMENT)
    purple_card.add_type(SpecialType.JEWELED)

    brown_card.set_text("Destroy this: Deal 10m damage.")
    red_card.set_text("Ranged: Damage from this is dealt after the next player's turn.")
    blue_card.set_flavor_tet("This item comes from the witch of dag'raba in the fallen swamp.")
    purple_card.set_text("When destroyed: Each player must give you an item.")
    purple_card.set_flavor_tet("\"It's good to be king.\" - Tom Petty")

    brown_card.add_stat("Price", "2")
    red_card.add_stat("Price", "3")
    blue_card.add_stat("Price", "1")
    purple_card.add_stat("Price", "4")

    brown_card.add_stat("Appeal", "-4")
    red_card.add_stat("Appeal", "Red Match 3")
    blue_card.add_stat("Appeal", "2/Beast")
    purple_card.add_stat("Appeal", "Purple Match 4")

    brown_card.add_stat("Priority", "0")
    red_card.add_stat("Priority", "2")
    purple_card.add_stat("Priority", "-3")

    brown_card.add_stat("HP", "8")
    red_card.add_stat("HP", "6")
    blue_card.add_stat("HP", "6")
    
    red_card.add_stat("Damage", "6b")
    purple_card.add_stat("Damage", "4m")

    brown_card.add_stat("Capacity", "1")
    blue_card.add_stat("Capacity", "3")
    purple_card.add_stat("Capacity", "4")

    purple_card.create_card()
    brown_card.create_card()
    red_card.create_card()
    blue_card.create_card()

main()
