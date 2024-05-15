from components import equippable
from entity.entity import Item

dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", equippable=equippable.LeatherArmor())

chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail())

attack_ring = Item(char="[", color=(0, 191, 255), name="Power Ring", equippable=equippable.AttackRing())

defense_ring = Item(char="[", color=(139, 69, 19), name="Armor Ring", equippable=equippable.DefenseRing())

vorpal_sword = Item(char="/", color=(0, 191, 255), name="Fire Sword", equippable=equippable.VorpalSword())
