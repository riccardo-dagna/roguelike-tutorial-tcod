# roguelike-tutorial-tcod

This is a rougelike created with the tutorial from http://rogueliketutorials.com/tutorials/tcod/v2/, and then modified to add new mechanics, items and monsters.

To start the project, simply download the project, execute "pip install -r requirements.txt".
And then, move into "roguelike-tutorial-tcod" and then execute "python main.py".

Or, if you want a .exe file, use the command: "pyinstaller main.py --onefile --add-data "data/menu_background.png;data/" --add-data "data/dejavu10x10_gs_tc.png;data/" "

Now the value of the player HP/Defense is insanely high, to be used for testing.
If you want to change it, go in the file "entity/entity_factories/entities.py" and change the line 17(fighter=Fighter(hp=99, base_defense=10, base_power=2),) in the class player to this one:
fighter=Fighter(hp=20, base_defense=1, base_power=2),

The list of commands is below:
- "movement arrow" to move and attack
- "numpad arrow" (excluded 5) to move and attack in the direction
- "r" to attack ranged
- "5", "Period" and "Clear" to wait
- "Return" and "Enter" to confirm
- "g" to pick up intems on the floor
- "Period" with "Shift" to take the stairs
- "c" to open the Character Sheet
- "i" to open inventory to use an item: if the item is a equipment, when you use the item you equip it; if the item is a potion, it is used; if it's a scroll, it will target an enemy or an area on the floor
- "d" to open inventory to drop an item (if the item is a equipment, when you drop the item you unequip it)


## List of mechanics

(If it's "for the enemy", it's a mechanic only usable by the enemies, if it's "on the enemy", it's a mechanic only usable by the player, otherwise it's for both)

Mechanics added in the game, already tested:
- Movement and basic attacks
- Random map generation and floor difficulty
- Item spawning in the map (depending on the floor the player is)
- Inventory capability (and dropping capability)
- Targeting ability with scrolls (single-target and area)
- Equipment (weapon, armor and accessory)
- Chests containing equipment (depending on the floor the player is)
- Condition (bleeding, poison, stun and confusion, condemnation, petrification, fear (on the enemy), blindness)
- Elemental damage (fire, ice, electric, acid) - only damage

Mechanics added in the game, to test:
- Ranged combat (with bows, etc.)
- Condition (grab (for the enemy, but needs to be checked))
- Chests (to correct random item generation by floor, and to tests)

Mechanics to add in the game:
- Condition (grab (on the enemy), charm)
- Extra effect of elemental damage
- Special attacks (stats drain, percentile damage, rot, steal, engulf/digest, dispel)
- New monster and items
- Shopkeeper (with random item)
- Boss monster (with special attack)
