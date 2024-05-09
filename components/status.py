from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor

class Status(BaseComponent):
    parent: Actor

    damage_bleed: int = 1
    damage_poison: int = 2
    turns_poison: int = 4
    turns_bleed: int = 4
    turns_stun: int = 1
    turns_confusion: int = 5

    def __init__(self, 
                 flag_bleed: bool = False, flag_poison: bool = False, flag_stun: bool = False, flag_confusion: bool = False, flag_grab: bool = False,
                 immunity_bleed: bool = False, immunity_poison: bool = False, immunity_stun: bool = False, immunity_confusion: bool = False, immunity_grab: bool = False,
                 attack_bleed: bool = False, attack_poison: bool = False, attack_stun: bool = False, attack_confusion: bool = False, attack_grab: bool = False,
    ):
        self.dict_condition_afflicted = dict(flag_bleed = flag_bleed, flag_poison = flag_poison, flag_stun = flag_stun, flag_confusion = flag_confusion, 
                                             flag_grab = flag_grab
                                             )

        self.dict_condition_immunity = dict(immunity_bleed = immunity_bleed, immunity_poison = immunity_poison, immunity_stun = immunity_stun, immunity_confusion = immunity_confusion, 
                                            immunity_grab = immunity_grab
                                            )

        self.dict_condition_attack = dict(attack_bleed = attack_bleed, attack_poison = attack_poison, attack_stun = attack_stun, attack_confusion = attack_confusion, 
                                          attack_grab = attack_grab
                                          )

        self.turns_passed = 0
    
    @property
    def check_turns_poison(self) -> bool:
        return self.dict_condition_afflicted["flag_bleed"] and self.turns_passed > self.turns_poison
        
    @property
    def check_turns_bleed(self) -> bool:
        return self.dict_condition_afflicted["flag_poison"] and self.turns_passed > self.turns_bleed
    
    @property
    def check_turns_stun(self) -> bool:
        return self.turns_passed >= self.turns_stun
    
    @property
    def check_turns_confusion(self) -> bool:
        return self.turns_passed > self.turns_confusion
    
    @property
    def check_grabbed_condition(self) -> bool:
        return self.dict_condition_afflicted["flag_grab"]

    @property
    def check_bleed_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_bleed"]
    
    @property
    def check_poison_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_poison"]
    
    @property
    def check_stun_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_stun"]
    
    @property
    def check_confusion_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_confusion"]
    
    @property
    def check_grab_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_grab"]
        
    def effect_hp_damage(self) -> None:
        if self.dict_condition_afflicted["flag_bleed"]:
            self.parent.fighter.hp -= self.damage_bleed
            self.engine.message_log.add_message(f"You receive {self.damage_bleed} damage from the bleeding!")
            self.turns_passed = 0
        if self.dict_condition_afflicted["flag_poison"]:
            self.parent.fighter.hp -= self.damage_poison
            self.engine.message_log.add_message(f"You receive {self.damage_poison} damage from the poison!")
            self.turns_passed = 0

    def affect_new_status(self, actor, target, attack_color) -> None:
        # After the damage, there is the check for the conditions effect.
        # This checks if the entity is an enemy or the player.
        # affect_new_status(self, target)
        if self.parent.equipment.weapon is None and self.parent.equipment.accessory_1 is None and self.parent.equipment.accessory_2 is None:
            """ If the enemy can affect the player with a condition from an attack, it will not check the other condition. 
               Then, it will check if the player is already afflicted by the condition or if it's immune to the condition."""
            if self.parent.status.dict_condition_attack["attack_bleed"]:
                if not target.status.dict_condition_afflicted["flag_bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if self.parent.status.dict_condition_attack["attack_poison"]:
                if not target.status.dict_condition_afflicted["flag_poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if self.parent.status.dict_condition_attack["attack_stun"]:
                if not target.status.dict_condition_afflicted["flag_stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["flag_stun"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if self.parent.status.dict_condition_attack["attack_confusion"]:
                if not target.status.dict_condition_afflicted["flag_confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["flag_confusion"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is confusion!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if self.parent.status.dict_condition_attack["attack_grab"]:
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["flag_grab"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already grabbed by {self.entity.name}!", attack_color)


        else:
            """Check if the equipment of the player can create the conditions specified. 
               Then, it will check if the monster is already afflicted by the condition or if it's immune to the condition."""
            if (self.parent.equipment.weapon.equippable.status_effect == "bleed" or (self.parent.equipment.accessory_1 is not None and self.parent.equipment.accessory_1.equippable.status_effect == "bleed")):
                if not target.status.dict_condition_afflicted["flag_bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "poison" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "poison")):
                if not target.status.dict_condition_afflicted["flag_poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "stun" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "stun")):
                if not target.status.dict_condition_afflicted["flag_stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["flag_stun"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "confusion" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "confusion")):
                if not target.status.dict_condition_afflicted["flag_confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["flag_confusion"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is confused!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "grab" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "grab")):
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["flag_grab"] = True
                        target.status.turns_passed = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already grabbed by the {self.entity.name}!", attack_color)



def confusion_direction() -> Tuple[int, int]:
    # Return a random direction to the player.
    direction_x, direction_y = random.choice(
        [
            (-1, -1),  # Northwest
            (0, -1),  # North
            (1, -1),  # Northeast
            (-1, 0),  # West
            (1, 0),  # East
            (-1, 1),  # Southwest
            (0, 1),  # South
            (1, 1),  # Southeast
        ]
    )

    return direction_x, direction_y