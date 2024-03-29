# roguelike-tutorial-tcod

This is a rougelike created with the tutorial from http://rogueliketutorials.com/tutorials/tcod/v2/, and then modified to add new mechanics, items and monsters.

To start the project, simply download the project, execute "pip install -r requirements.txt".
And then, move into "roguelike-tutorial-tcod" and then execute "python main.py".

The list of commands is below:
- "movement arrow" to move and attack
- "numpad arrow" (excluded 5) to move and attack in the direction
- "5", "Period" and "Clear" to wait
- "Return" and "Enter" to confirm
- "g" to pick up intems on the floor
- "Period" with "Shift" to take the stairs
- "c" to open the Character Sheet
- "i" to open inventory to use an item: if the item is a equipment, when you use the item you equip it; if the item is a potion, it is used; if it's a scroll, it will target an enemy or an area on the floor
- "d" to open inventory to drop an item (if the item is a equipment, when you drop the item you unequip it)

Mechanics added in the game, already tested:
- Movement and basic attacks
- Random map generation
- Item spawning in the map
- Inventory capability (and dropping capability)
- Targeting ability with scrolls (single-target and area)
- Equipment (weapon, armor and accessory)
- Condition (bleeding, poison, stun (for the enemy only) and confusion (for the enemy only))

Mechanics added in the game, to test:
- Condition (stun (for the player) and confusion (for the player))

Mechanics to add in the game:
- Condition (blindness, grab, petrification)
- Elemental damage and extra effect
- New monster and items
- Shopkeeper (with random item)
