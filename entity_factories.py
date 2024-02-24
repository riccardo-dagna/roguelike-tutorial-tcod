from components import consumable, equippable
from components.ai import HostileEnemy
from components.damageinfo import DamageInfo
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.status import Status
from entity import Actor, Item, Chest

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=99, base_defense=10, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    status=Status(),
    damage_info=DamageInfo(),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    status=Status(),
    damage_info=DamageInfo(),
)
troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    status=Status(),
    damage_info=DamageInfo(),
)


confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
status_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Status Potion",
    consumable=consumable.HealingStatusConsumable(amount=2)
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
stun_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Stun Scroll",
    consumable=consumable.StunConsumable(number_of_turns=1),
)


dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", equippable=equippable.LeatherArmor())

chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail())

attack_ring = Item(char="[", color=(0, 191, 255), name="Power Ring", equippable=equippable.AttackRing())

defense_ring = Item(char="[", color=(139, 69, 19), name="Armor Ring", equippable=equippable.DefenseRing())

vorpal_sword = Item(char="/", color=(0, 191, 255), name="Fire Sword", equippable=equippable.VorpalSword())


chest = Chest(char="(", color=(139, 69, 19), name="Chest")