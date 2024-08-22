from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent
from actions_logic.input_handlers import SelectIndexHandler, SingleRangedAttackHandler, AreaRangedAttackHandler
import game_map.color as color
from actions_logic import actions
import utility_files.exceptions as exceptions 

if TYPE_CHECKING:
    from entity.entity import Entity, Actor
    from game_logic.engine import Engine

class Spell(BaseComponent):
    def __init__(self, name: str, damage: int = 0, mana: int = 1, max_range: int = 0, radius: int = 0, status: str = None, type: str = None, parent: Entity = None, handler: SelectIndexHandler = None) -> None:
        self.name = name
        self.damage = damage
        self.mana = mana
        self.max_range = max_range
        self.radius = radius
        self.status = status
        self.handler = handler
        self.type = type

        self.parent = parent

    def cast(self, caster: Actor) -> Optional[SelectIndexHandler]:
        if self.handler is not None:
            self.engine.message_log.add_message("Select a target location.", color.needs_target)
            return self.handler(
                self.engine, 
                self.radius,
                callback=lambda xy: actions.SpellAction(caster, self, xy),
            )
        else:
            xy = (self.parent.x, self.parent.y)
            return actions.SpellAction(caster, self, xy)
    
    def activate_spell(self, xy) -> None:
        if self.type == "damage":
            self.damage_effect_spell(xy)
        elif self.type == "status":
            self.status_effect_spell(xy)
        elif self.type == "cure":
            self.cure_effect_spell(xy)
        else:
            pass
            
    
    def damage_effect_spell(self, xy: Optional[Tuple[int, int]]) -> None:
        caster = self.parent

        if self.handler == AreaRangedAttackHandler:
            """
            Deals damage to a radius of targets.
            """
            targets_hit = False
            for actor in self.engine.game_map.actors:
                if actor.distance(*xy) <= self.radius:
                    self.engine.message_log.add_message(
                        f"The {actor.name} is hit by {self.name}, taking {self.damage} damage!"
                    )
                    actor.fighter.take_damage(self.damage)
                    targets_hit = True

            if not targets_hit:
                raise exceptions.Impossible("There are no targets in the radius.")
            
        elif self.handler == SingleRangedAttackHandler:
            target = self.gamemap.get_actor_at_location(*xy)

            if not self.engine.game_map.visible[xy]:
                raise exceptions.Impossible("You cannot target an area that you cannot see.")
            if not target:
                raise exceptions.Impossible("You must select an enemy to target.")
            if target is caster:
                raise exceptions.Impossible("You cannot cast this spell on yourself!")
                
            self.engine.message_log.add_message(
                f"The {target.name} is hit by {self.name}, taking {self.damage} damage!",
                color.status_effect_applied,
            )
            target.fighter.take_damage(self.damage)

        else:
            target = None
            closest_distance = self.max_range + 1.0

            for actor in self.engine.game_map.actors:
                if actor is not caster and self.parent.gamemap.visible[actor.x, actor.y]:
                    distance = caster.distance(actor.x, actor.y)

                    if distance < closest_distance:
                        target = actor
                        closest_distance = distance

            if target:
                self.engine.message_log.add_message(
                    f"The {target.name} is hit by {self.name}, for {self.damage} damage!"
                )
                target.fighter.take_damage(self.damage)
            else:
                raise exceptions.Impossible("No enemy is close enough to strike.")

        caster.fighter.mana -= self.mana

    def status_effect_spell(self, xy: Optional[Tuple[int, int]]) -> None:
        caster = self.parent

        if self.handler == SingleRangedAttackHandler:
            target = self.gamemap.get_actor_at_location(*xy)

            if not self.engine.game_map.visible[xy]:
                raise exceptions.Impossible("You cannot target an area that you cannot see.")
            if not target:
                raise exceptions.Impossible("You must select an enemy to target.")
            if target is caster:
                raise exceptions.Impossible("You cannot cast this spell on yourself!")

            if self.status == "confusion":                    
                self.engine.message_log.add_message(
                f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
                    color.status_effect_applied,
                )
                target.status.dict_condition_afflicted["confusion"] = True
                target.status.dict_turns_passed["confusion"] = 0
            elif self.status == "fear":
                self.engine.message_log.add_message(
                    f"The face of the {target.name} look scared, as it starts to run away from you!",
                    color.status_effect_applied,
                )
                target.status.dict_condition_afflicted["fear"] = True
                target.status.dict_turns_passed["fear"] = 0
            elif self.status == "stun":
                self.engine.message_log.add_message(
                    f"The {target.name} is trying to focus, but it can't!",
                    color.status_effect_applied,
                )
                target.status.dict_condition_afflicted["stun"] = True
                target.status.dict_turns_passed["stun"] = 0
        elif self.handler == AreaRangedAttackHandler:
            pass
        else:
            pass
        
        caster.fighter.mana -= self.mana


    def cure_effect_spell(self, xy: Optional[Tuple[int, int]]) -> None:
        caster = self.parent

        if caster.fighter.hp >= caster.fighter.max_hp:
            raise exceptions.Impossible("Your health is full!")
        else:
            if self.status is not None:
                caster.status.dict_condition_afflicted["bleed"] = False
                caster.status.dict_condition_afflicted["poison"] = False
                caster.status.dict_condition_afflicted["condemnation"] = False
                caster.status.dict_condition_afflicted["petrification"] = False
                caster.status.dict_condition_afflicted["blindness"] = False
                self.engine.message_log.add_message(
                    f"You are healed from your affliction!",
                    color.health_recovered,
                )
        
            amount_recovered = caster.fighter.heal(self.damage)   
            self.engine.message_log.add_message(
                f"You cast the {self.name} spell, and recover {amount_recovered} HP!",
                color.health_recovered,
            )
            caster.fighter.mana -= self.mana



