from components import equippable
from entity.entity import Item


#This sections contains the weapons
dagger = Item(char="/", color=(0, 191, 255), name="Dagger", material="metal", equippable=equippable.Dagger())
sword = Item(char="/", color=(0, 191, 255), name="Sword", material="metal", equippable=equippable.Sword())
vorpal_sword = Item(char="/", color=(0, 191, 255), name="Fire Sword", material="metal", magic_item=True, equippable=equippable.VorpalSword())

bow = Item(char="/", color=(0, 191, 255), name="Bow", material="wood", equippable=equippable.Bow())
kunai = Item(char="/", color=(0, 191, 255), name="Kunai", material="metal", equippable=equippable.Kunai())


#This sections contains the armors
leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", material="leather", equippable=equippable.LeatherArmor())
chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", material="metal", equippable=equippable.ChainMail())


#This sections contains the accessories
attack_ring = Item(char="[", color=(0, 191, 255), name="Power Ring", material="metal", magic_item=True, equippable=equippable.AttackRing())
defense_ring = Item(char="[", color=(139, 69, 19), name="Armor Ring", material="metal", magic_item=True, equippable=equippable.DefenseRing())
