from components import consumable
from entity.entity import Item

#This sections contains the scrolls
confusion_scroll = Item(char="~", color=(207, 63, 255), name="Confusion Scroll", material="paper", magic_item=True, consumable=consumable.ConfusionConsumable(),)
fear_scroll = Item(char="~", color=(207, 63, 255), name="Fear Scroll", material="paper", magic_item=True, consumable=consumable.FearConsumable(),)
fireball_scroll = Item(char="~", color=(255, 0, 0), name="Fireball Scroll", material="paper", magic_item=True, consumable=consumable.FireballDamageConsumable(damage=12, radius=3),)
lightning_scroll = Item(char="~", color=(255, 255, 0), name="Lightning Scroll", material="paper", magic_item=True, consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),)
stun_scroll = Item(char="~", color=(255, 255, 0), name="Stun Scroll", material="paper", magic_item=True, consumable=consumable.StunConsumable(),)


#This sections contains the potions
health_potion = Item(char="!", color=(127, 0, 255), name="Health Potion", material="liquid", magic_item=True, consumable=consumable.HealingConsumable(amount=4),)
status_potion = Item(char="!", color=(127, 0, 255), name="Status Potion", material="liquid", magic_item=True, consumable=consumable.HealingStatusConsumable(amount=2),)
