from __future__ import annotations

from typing import TYPE_CHECKING, Any

from components.base_component import BaseComponent
from components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity.entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        status_effect: str = "",
        damage_type: str = "",
        projectile_name: str = "",
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.status_effect = status_effect
        self.damage_type = damage_type
        self.projectile_name = projectile_name
    


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=2)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4)

class VorpalSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4, status_effect="bleed")

class PoisonSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4, status_effect="poison")

class FireSword(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4, damage_type="fire")

class IceSword(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4, damage_type="ice")
        
class ElectricSword(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MEELEE, power_bonus=4, damage_type="electric")


class Bow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED, power_bonus=2, projectile_name="arrow")


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)


class AttackRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ACCESSORY, power_bonus=3)

class DefenseRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ACCESSORY, defense_bonus=3)

class VorpalAttackRing(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.ACCESSORY, power_bonus=2, status_effect="bleed")

class PoisonAttackRing(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.ACCESSORY, power_bonus=2, status_effect="poison")

