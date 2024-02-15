from __future__ import annotations

from typing import TYPE_CHECKING, Any

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        status_effect: str = "",
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.status_effect = status_effect


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2, status_effect="burn")

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class FireSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4, status_effect="burn")

class PoisonSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4, status_effect="poison")


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

class FireAttackRing(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.ACCESSORY, power_bonus=2, status_effect="burn")

class PoisonAttackRing(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.ACCESSORY, power_bonus=2, status_effect="poison")

