from components.ai import HostileMeeleeEnemy, HostileRangedEnemy, SpecialEnemy
from components.damageinfo import DamageInfo
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.special_attacks import SpecialAttacks
from components.status import Status
from entity.entity import Actor, Chest

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileMeeleeEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=99, base_defense=10, base_power=10),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    status=Status(),
    damage_info=DamageInfo(),
    special_attacks=SpecialAttacks()
)


#This sections contains the enemies
meelee_orc = Actor(char="o", color=(63, 127, 63), name="Orc",
    ai_cls=HostileMeeleeEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0), level=Level(xp_given=35), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
)
ranged_orc = Actor(char="o", color=(63, 127, 63), name="Orc",
    ai_cls=HostileRangedEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0), level=Level(xp_given=35), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
)
troll = Actor(char="T", color=(0, 127, 0), name="Troll", 
    ai_cls=HostileMeeleeEnemy, equipment=Equipment(), fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0), level=Level(xp_given=100), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(),
)

vampire = Actor(char="v", color=(63,127, 63), name="Vampire",
    ai_cls=SpecialEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0), level=Level(xp_given=200), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(flag_stats_drain=True, value_agility_drain=1),
)
gravity_orc = Actor(char="g", color=(63,127, 63), name="Gravity Orc",
    ai_cls=SpecialEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0), level=Level(xp_given=200), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(flag_percentile=True, values_percentile=10),
)
rot_orc = Actor(char="r", color=(63,127, 63), name="Rot Orc",
    ai_cls=SpecialEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0), level=Level(xp_given=200), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(flag_rot=True, damage_rot=4),
)
corrosion_orc = Actor(char="c", color=(63,127, 63), name="Corrosion Orc",
    ai_cls=SpecialEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0), level=Level(xp_given=200), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(flag_corrosion=True, damage_corrosion=4),
)
purple_worm = Actor(char="w", color=(63,127, 63), name="Purple Worm",
    ai_cls=SpecialEnemy, equipment=Equipment(), fighter=Fighter(hp=15, base_defense=3, base_power=2),
    inventory=Inventory(capacity=0), level=Level(xp_given=200), status=Status(), damage_info=DamageInfo(),
    special_attacks=SpecialAttacks(flag_ingest=True, damage_ingest=4),
)



#This sections contains the neutral entities
chest = Chest(char="(", color=(139, 69, 19), name="Chest")