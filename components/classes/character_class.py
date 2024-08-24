from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_logic.render_order import RenderOrder
import game_map.color as color

if TYPE_CHECKING:
    from entity.entity import Actor

class CharacterClass(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int, mana: int = 0):
        self.max_hp = hp
        self._hp = hp
        self.max_mana = mana
        self._mana = mana
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def mana(self) -> int:
        return self._mana
    
    @mana.setter
    def mana(self, value: int) -> None:
        self._mana = max(0, min(value, self.max_mana))

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power_meelee(self) -> int:
        return self.base_power + self.power_meelee_bonus
    
    @property
    def power_ranged(self) -> int:
        return self.base_power + self.power_ranged_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_meelee_bonus(self) -> int:
        if self.parent.equipment.meelee:
            return self.parent.equipment.power_meelee_bonus
        else:
            return 0
               
    @property
    def power_ranged_bonus(self) -> int:
        if self.parent.equipment.meelee:
            return self.parent.equipment.power_ranged_bonus
        else:
            return 0


    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)


    def heal_hp(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered
    

    def heal_mana(self, amount: int) -> int:
        if self.mana == self.max_mana:
            return 0

        new_mana_value = self.mana + amount

        if new_mana_value > self.max_mana:
            new_mana_value = self.max_mana

        amount_recovered = new_mana_value - self.mana

        self.mana = new_mana_value

        return amount_recovered
        

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
