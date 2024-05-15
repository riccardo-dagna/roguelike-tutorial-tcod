from components import consumable
from entity.entity import Item

#This sections contains the scrolls
confusion_scroll = Item(char="~", color=(207, 63, 255), name="Confusion Scroll", consumable=consumable.ConfusionConsumable(number_of_turns=10),)
fireball_scroll = Item(char="~", color=(255, 0, 0), name="Fireball Scroll", consumable=consumable.FireballDamageConsumable(damage=12, radius=3),)
lightning_scroll = Item(char="~", color=(255, 255, 0), name="Lightning Scroll", consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),)
stun_scroll = Item(char="~", color=(255, 255, 0), name="Stun Scroll", consumable=consumable.StunConsumable(number_of_turns=1),)


#This sections contains the potions
health_potion = Item(char="!", color=(127, 0, 255), name="Health Potion", consumable=consumable.HealingConsumable(amount=4),)
status_potion = Item(char="!", color=(127, 0, 255), name="Status Potion", consumable=consumable.HealingStatusConsumable(amount=2),)
