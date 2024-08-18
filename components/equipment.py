from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from components.base_component import BaseComponent
from components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity.entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, meelee: Optional[Item] = None, ranged: Optional[Item] = None, armor: Optional[Item] = None, 
                 accessory_1: Optional[Item] = None, accessory_2: Optional[Item] = None):
        self.meelee = meelee
        self.ranged = ranged
        self.armor = armor
        self.accessory_1 = accessory_1
        self.accessory_2 = accessory_2

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.meelee is not None and self.meelee.equippable is not None:
            if self.meelee.damaged is False:
                bonus += self.meelee.equippable.defense_bonus
            else:
                bonus += round(self.meelee.equippable.defense_bonus/2)

        if self.ranged is not None and self.ranged.equippable is not None:
            if self.ranged.damaged is False:
                bonus += self.ranged.equippable.defense_bonus
            else:
                bonus += round(self.ranged.equippable.defense_bonus/2)
        
        if self.armor is not None and self.armor.equippable is not None:
            if self.armor.damaged is False:
                bonus += self.armor.equippable.defense_bonus
            else:
                bonus += round(self.armor.equippable.defense_bonus/2)
        
        if self.accessory_1 is not None and self.accessory_1.equippable is not None:
            if self.accessory_1.damaged is False:
                bonus += self.accessory_1.equippable.defense_bonus
            else:
                bonus += round(self.accessory_1.equippable.defense_bonus/2)
        
        if self.accessory_2 is not None and self.accessory_2.equippable is not None:
            if self.accessory_2.damaged is False:
                bonus += self.accessory_2.equippable.power_bonus
            else:
                bonus += round(self.accessory_2.equippable.defense_bonus/2)

        return bonus

    @property
    def power_meelee_bonus(self) -> int:
        bonus = 0

        if self.meelee is not None and self.meelee.equippable is not None:
            if self.meelee.damaged is False:
                bonus += self.meelee.equippable.power_bonus
            else:
                bonus += round(self.meelee.equippable.power_bonus/2)

        if self.armor is not None and self.armor.equippable is not None:
            if self.armor.damaged is False:
                bonus += self.armor.equippable.power_bonus
            else:
                bonus += round(self.armor.equippable.power_bonus/2)
        
        if self.accessory_1 is not None and self.accessory_1.equippable is not None:
            if self.accessory_1.damaged is False:
                bonus += self.accessory_1.equippable.power_bonus
            else:
                bonus += round(self.accessory_1.equippable.power_bonus/2)
        
        if self.accessory_2 is not None and self.accessory_2.equippable is not None:
            if self.accessory_2.damaged is False:
                bonus += self.accessory_2.equippable.power_bonus
            else:
                bonus += round(self.accessory_2.equippable.power_bonus/2)


        return bonus
    
    @property
    def power_ranged_bonus(self) -> int:
        bonus = 0

        if self.ranged is not None and self.ranged.equippable is not None:
            if self.ranged.damaged is False:
                bonus += self.ranged.equippable.power_bonus
            else:
                bonus += round(self.meelee.equippable.power_bonus/2)

        if self.armor is not None and self.armor.equippable is not None:
            if self.armor.damaged is False:
                bonus += self.armor.equippable.power_bonus
            else:
                bonus += round(self.armor.equippable.power_bonus/2)
        
        if self.accessory_1 is not None and self.accessory_1.equippable is not None:
            if self.accessory_1.damaged is False:
                bonus += self.accessory_1.equippable.power_bonus
            else:
                bonus += round(self.accessory_1.equippable.power_bonus/2)
        
        if self.accessory_2 is not None and self.accessory_2.equippable is not None:
            if self.accessory_2.damaged is False:
                bonus += self.accessory_2.equippable.power_bonus
            else:
                bonus += round(self.accessory_2.equippable.power_bonus/2)

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.meelee == item or self.ranged == item or self.armor == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You remove the {item_name}.")

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You equip the {item_name}.")

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if equippable_item.equippable and equippable_item.equippable.equipment_type == EquipmentType.MEELEE:
            slot = "meelee"
        elif equippable_item.equippable and equippable_item.equippable.equipment_type == EquipmentType.RANGED:
            slot = "ranged"
        elif equippable_item.equippable and equippable_item.equippable.equipment_type == EquipmentType.ARMOR:
            slot = "armor"
        else:
            slot= "accessory_1"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
