from components.ai import HostileMeeleeEnemy, HostileRangedEnemy, SpecialEnemy
from components.damageinfo import DamageInfo
from components.item.equipment import Equipment
from components.classes.fighter import Fighter, Thief, Mage
from components.inventory import Inventory
from components.level import Level
from components.special_attacks import SpecialAttacks
from components.statuses_buffs.status import Status
from components.statuses_buffs.buffs import Buffs
from components.spells.spellbook import Spellbook
from entity.entity import Actor, Chest

player_fighter = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player Fighter",
    ai_cls=HostileMeeleeEnemy,
    equipment=Equipment(),
    classes=Fighter(hp=99, base_defense=10, base_power=10, mana=10),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    status=Status(),
    buffs=Buffs(),
    damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
    spellbook=Spellbook(capacity=0, start_list=[])
)

player_thief = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player Thief",
    ai_cls=HostileMeeleeEnemy,
    equipment=Equipment(),
    classes=Thief(hp=99, base_defense=10, base_power=10, mana=10),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    status=Status(),
    buffs=Buffs(),
    damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
    spellbook=Spellbook(capacity=0, start_list=[])
)

player_mage = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player Mage",
    ai_cls=HostileMeeleeEnemy,
    equipment=Equipment(),
    classes=Mage(hp=99, base_defense=10, base_power=10, mana=100),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    status=Status(),
    buffs=Buffs(),
    damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
    spellbook=Spellbook(capacity=10, start_list=[])
)


#This sections contains the neutral entities
chest = Chest(char="(", color=(139, 69, 19), name="Chest")