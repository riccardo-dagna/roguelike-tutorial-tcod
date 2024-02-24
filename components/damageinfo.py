from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class DamageInfo(BaseComponent):
    parent: Actor

    def __init__(self, 
                 fire_resistance: bool = False, ice_resistance: bool = False, electric_resistance: bool = False,
                 fire_immunity: bool = False, ice_immunity: bool = False, electric_immunity: bool = False,
                 fire_vulnerability: bool = False, ice_vulnerability: bool = False, electric_vulnerability: bool = False,
                 fire_attack: bool = False, ice_attack: bool = False, electric_attack: bool = False
    ):
        
        self.dict_damage_resistance = dict(fire = fire_resistance, ice = ice_resistance, electric = electric_resistance)
        self.dict_damage_immunity = dict(fire = fire_immunity, ice = ice_immunity, electric = electric_immunity)
        self.dict_damage_vulnerabiliy = dict(fire = fire_vulnerability, ice = ice_vulnerability, electric = electric_vulnerability)
        self.dict_damage_attack = dict(fire = fire_attack, ice = ice_attack, electric = electric_attack)

    def attack_type_return(self) -> str:
        if self.dict_damage_attack["fire"]:
            return "fire"
        elif self.dict_damage_attack["ice"]:
            return "ice"
        elif self.dict_damage_attack["electric"]:
            return "electric"
        else:
            return ""
    
    def calculate_damage(self, damage_type: str) -> float:
        match damage_type:
            case "fire":
                if self.dict_damage_resistance["fire"]:
                    return 0.5
                elif self.dict_damage_immunity["fire"]:
                    return 0
                elif self.dict_damage_vulnerabiliy["fire"]:
                    return 2
                return 1
            case "ice":
                if self.dict_damage_resistance["ice"]:
                    return 0.5
                elif self.dict_damage_immunity["ice"]:
                    return 0
                elif self.dict_damage_vulnerabiliy["ice"]:
                    return 2
                return 1
            case "electric":
                if self.dict_damage_resistance["electric"]:
                    return 0.5
                elif self.dict_damage_immunity["electric"]:
                    return 0
                elif self.dict_damage_vulnerabiliy["electric"]:
                    return 2
                return 1
            case _:
                return 1

