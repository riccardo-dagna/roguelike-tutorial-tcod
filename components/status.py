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
    turns_condemnation: int = 10
    turns_petrification: int = 20
    turns_fear: int = 10

    def __init__(self, 
                 flag_bleed: bool = False, flag_poison: bool = False, flag_stun: bool = False, flag_confusion: bool = False, flag_grab: bool = False, flag_condemnation: bool = False, flag_petrification: bool = False, flag_fear: bool = False, flag_blindness: bool = False, 
                 immunity_bleed: bool = False, immunity_poison: bool = False, immunity_stun: bool = False, immunity_confusion: bool = False, immunity_grab: bool = False, immunity_condemnation: bool = False, immunity_petrification: bool = False, immunity_fear: bool = False, immunity_blindness: bool = False, 
                 attack_bleed: bool = False, attack_poison: bool = False, attack_stun: bool = False, attack_confusion: bool = False, attack_grab: bool = False, attack_condemnation: bool = False, attack_petrification: bool = False, attack_fear: bool = False, attack_blindness: bool = False,
    ):
        self.dict_condition_afflicted = dict(bleed = flag_bleed, poison = flag_poison, stun = flag_stun, confusion = flag_confusion, grab = flag_grab, 
                                             condemnation = flag_condemnation, petrification = flag_petrification, fear = flag_fear, blindness = flag_blindness,
                                             )

        self.dict_condition_immunity = dict(bleed = immunity_bleed, poison = immunity_poison, stun = immunity_stun, confusion = immunity_confusion, 
                                            grab = immunity_grab, condemnation = immunity_condemnation, petrification = immunity_petrification, 
                                            fear = immunity_fear, blindness = immunity_blindness,
                                            )

        self.dict_condition_attack = dict(bleed = attack_bleed, poison = attack_poison, stun = attack_stun, confusion = attack_confusion, grab = attack_grab,
                                          condemnation = attack_condemnation, petrification = attack_petrification, fear = attack_fear, blindness = attack_blindness
                                          )
        
        self.dict_turns_passed = dict(poison = 0, burn = 0, stun = 0, confusion = 0, condemnation = 0, petrification = 0, fear = 0,)
    
    @property
    def check_turns_poison(self) -> bool:
        return self.dict_condition_afflicted["poison"] and self.dict_turns_passed["poison"] > self.turns_poison
        
    @property
    def check_turns_bleed(self) -> bool:
        return self.dict_condition_afflicted["bleed"] and self.dict_turns_passed["bleed"] > self.turns_bleed
    
    @property
    def check_turns_stun(self) -> bool:
        return self.dict_turns_passed["stun"] >= self.turns_stun
    
    @property
    def check_turns_confusion(self) -> bool:
        return self.dict_turns_passed["confusion"] > self.turns_confusion
    
    @property
    def check_turns_condemnation(self) -> bool:
        return self.dict_condition_afflicted["condemnation"] and self.dict_turns_passed["condemnation"] > self.turns_condemnation

    @property
    def check_turns_petrification(self) -> bool:
        return self.dict_condition_afflicted["petrification"] and self.dict_turns_passed["petrification"] > self.turns_petrification
    
    @property
    def check_turns_petrification(self) -> bool:
        return self.dict_condition_afflicted["fead"] and self.dict_turns_passed["fear"] > self.turns_fear
        
    
    @property
    def check_grabbed_condition(self) -> bool:
        return self.dict_condition_afflicted["grab"]


    @property
    def check_bleed_immunity(self) -> bool:
        return self.dict_condition_immunity["bleed"]
    
    @property
    def check_poison_immunity(self) -> bool:
        return self.dict_condition_immunity["poison"]
    
    @property
    def check_stun_immunity(self) -> bool:
        return self.dict_condition_immunity["stun"]
    
    @property
    def check_confusion_immunity(self) -> bool:
        return self.dict_condition_immunity["confusion"]
    
    @property
    def check_grab_immunity(self) -> bool:
        return self.dict_condition_immunity["grab"]
    
    @property
    def check_condemnation_immunity(self) -> bool:
        return self.dict_condition_immunity["condemnation"]
    
    @property
    def check_petrification_immunity(self) -> bool:
        return self.dict_condition_immunity["petrification"]
    
    @property
    def check_fear_immunity(self) -> bool:
        return self.dict_condition_immunity["fear"]
    
    @property
    def check_blindness_immunity(self) -> bool:
        return self.dict_condition_immunity["blindness"]
    

    def effect_hp_damage(self) -> None:
        if self.dict_condition_afflicted["poison"]:
            self.parent.fighter.hp -= self.damage_bleed
            self.engine.message_log.add_message(f"You receive {self.damage_bleed} damage from the bleeding!")
            self.dict_turns_passed["bleed"] = 0
        if self.dict_condition_afflicted["poison"]:
            self.parent.fighter.hp -= self.damage_poison
            self.engine.message_log.add_message(f"You receive {self.damage_poison} damage from the poison!")
            self.dict_turns_passed["poison"] = 0

    def affect_new_status(self, actor, target, attack_color) -> None:
        # After the damage, there is the check for the conditions effect.
        # This checks if the entity is an enemy or the player.
        # affect_new_status(self, target)
        if self.parent.equipment.weapon is None and self.parent.equipment.accessory_1 is None and self.parent.equipment.accessory_2 is None:
            """ If the enemy can affect the player with a condition from an attack, it will not check the other condition. 
               Then, it will check if the player is already afflicted by the condition or if it's immune to the condition."""
            if self.parent.status.dict_condition_attack["bleed"]:
                if not target.status.dict_condition_afflicted["bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["bleed"] = True
                        target.status.dict_turns_passed["bleed"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if self.parent.status.dict_condition_attack["poison"]:
                if not target.status.dict_condition_afflicted["poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["poison"] = True
                        target.status.dict_turns_passed["poison"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if self.parent.status.dict_condition_attack["stun"]:
                if not target.status.dict_condition_afflicted["stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["stun"] = True
                        target.status.dict_turns_passed["stun"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if self.parent.status.dict_condition_attack["confusion"]:
                if not target.status.dict_condition_afflicted["confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["confusion"] = True
                        target.status.dict_turns_passed["confusion"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is confusion!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if self.parent.status.dict_condition_attack["grab"]:
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["grab"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already grabbed by {self.entity.name}!", attack_color)
            if self.parent.status.dict_condition_attack["condemnation"]:
                if not target.status.dict_condition_afflicted["condemnation"]:
                    if not target.status.check_condemnation_immunity:
                        target.status.dict_condition_afflicted["condemnation"] = True
                        target.status.dict_turns_passed["condemnation"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is condemned to die soon!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} death is not predestined now!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already condemned to die!", attack_color)
            if self.parent.status.dict_condition_attack["petrification"]:
                if not target.status.dict_condition_afflicted["petrification"]:
                    if not target.status.check_petrification_immunity:
                        target.status.dict_condition_afflicted["petrification"] = True
                        target.status.dict_turns_passed["petrification"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is slowly turning to stone!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too strong to be affected!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already turning to stone!", attack_color)
            if self.parent.status.dict_condition_attack["fear"]:
                if not target.status.dict_condition_afflicted["fear"]:
                    if not target.status.check_fear_immunity:
                        target.status.dict_condition_afflicted["fear"] = True
                        target.status.dict_turns_passed["fear"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is afraid of his enemy!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too strong willed to be afraid!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already afraid of his enemy!", attack_color)
            if self.parent.status.dict_condition_attack["blindness"]:
                if not target.status.dict_condition_afflicted["blindness"]:
                    if not target.status.check_blindness_immunity:
                        target.status.dict_condition_afflicted["blindness"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} eyes are clouded!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} eyes are too sharp!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already blinded!", attack_color)



        else:
            """Check if the equipment of the player can create the conditions specified. 
               Then, it will check if the monster is already afflicted by the condition or if it's immune to the condition."""
            if (self.parent.equipment.weapon.equippable.status_effect == "bleed" or (self.parent.equipment.accessory_1 is not None and self.parent.equipment.accessory_1.equippable.status_effect == "bleed")):
                if not target.status.dict_condition_afflicted["bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["bleed"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "poison" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "poison")):
                if not target.status.dict_condition_afflicted["poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["poison"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "stun" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "stun")):
                if not target.status.dict_condition_afflicted["stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["stun"] = True
                        target.status.dict_turns_passed["stun"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "confusion" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "confusion")):
                if not target.status.dict_condition_afflicted["confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["confusion"] = True
                        target.status.dict_turns_passed["confusion"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is confused!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "grab" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "grab")):
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["grab"] = True
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already grabbed by the {self.entity.name}!", attack_color)
            if (self.parent.equipment.weapon.equippable.status_effect == "fear" or (self.parent.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "fear")):
                if not target.status.dict_condition_afflicted["fear"]:
                    if not target.status.check_fear_immunity:
                        target.status.dict_condition_afflicted["fear"] = True
                        target.status.dict_turns_passed["fear"] = 0
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is afraid of his enemy!", attack_color)
                    else:
                        self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is too strong willed to be afraid!", attack_color)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"The {target.name} is already afraid of his enemy!", attack_color)



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

