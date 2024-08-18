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
- "i" to open inventory to use an item
- "d" to open inventory to drop an item


## List of mechanics

(If it's "for the enemy", it's a mechanic only usable by the enemies, if it's "on the enemy", it's a mechanic only usable by the player, otherwise it's for both)

Mechanics added in the game, already tested:
- Movement and basic attacks (meelee and ranged)
- Random map generation and floor difficulty
- Item spawning in the map (depending on the floor the player is)
- Inventory capability (and dropping capability) (only for the player)
- Targeting ability with scrolls (single-target and area) (only for the player)
- Equipment (weapon, armor and accessory) (only for the player)
- Chests containing equipment (depending on the floor the player is)
- Condition (bleeding, poison, stun, confusion, grab, condemnation, petrification, fear, blindness, charm, rage)
- Elemental damage (fire, ice, electric, acid) - only damage

Mechanics added in the game, to test:
- Chests (to correct random item generation by floor, and to tests)
- Special attacks (stats drain (for the enemy), percentile (for the enemy), rot (for the enemy), corrosion (for the enemy), dispel (for the enemy, only damage and magic items), steal (for 
  the enemy))

Mechanics added in the game, to correct:
- Special attacks (engulf/digest (to add damage every turn))

Mechanics to add in the game:
- Extra effect of elemental damage
- Special attacks (armor penetrating damage)
- Spells, spellbook and magic system
- New monster and items
- Shopkeeper (with random item)
- Boss monster (with special attack)


If in playing the game you find any bugs, feel free to let me know.