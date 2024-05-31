from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor

class SpecialAttacks(BaseComponent):
    parent: Actor
    turns_to_recharge: int = 5

    def __init__(self, 
                 flag_ingest: bool = False, flag_percentile: bool = False, flag_stats_drain: bool = False, flag_rot: bool = False, flag_steal: bool = False, flag_dispel: bool = False,
                 values_percentile: int = 0, value_strenght_drain: int = 0, value_agility_drain: int = 0,
                 damage_ingest: int = 0, damage_stat_drain: int = 0, damage_rot: int = 0, damage_steal: int = 0, damage_dispel: int = 0,
                 status_ingest: bool = False, status_rot: bool = False,
                 immunity_ingest: bool = False, immunity_percentile: bool = False, immunity_stats_drain: bool = False, immunity_rot: bool = False, immunity_steal: bool = False, immunity_dispel: bool = False,
                ) -> None:
        self.dict_special_attacks_flag = dict(ingest = flag_ingest, percentile = flag_percentile, stats_drain = flag_stats_drain, rot = flag_rot, steal = flag_steal, dispel = flag_dispel,)
        self.dict_special_attack_values = dict(percentile = values_percentile, strenght_drain = value_strenght_drain, agility_drain = value_agility_drain,)
        self.dict_special_attack_damage = dict(ingest = damage_ingest, stats_drain = damage_stat_drain, rot = damage_rot, steal = damage_steal, dispel = damage_dispel,)
        self.dict_special_attack_status = dict(ingest = status_ingest, rot = status_rot,)
        self.dict_special_attack_immunity = dict(ingest = immunity_ingest, percentile = immunity_percentile, stats_drain = immunity_stats_drain, rot = immunity_rot, steal = immunity_steal, dispel = immunity_dispel,)
        self.dict_turns_recharge = dict(ingest = 0, percentile = 0, stats_drain = 0, rot = 0, steal = 0, dispel = 0,)
    
    @property
    def check_attack_ingest(self) -> bool:
        return self.dict_special_attacks_flag["ingest"]
    
    @property
    def check_attack_percentile(self) -> bool:
        return self.dict_special_attacks_flag["percentile"]
    
    @property
    def check_attack_stats(self) -> bool:
        return self.dict_special_attacks_flag["stats_drain"]
    
    @property
    def check_attack_rot(self) -> bool:
        return self.dict_special_attacks_flag["rot"]
    
    @property
    def check_attack_steal(self) -> bool:
        return self.dict_special_attacks_flag["steal"]
    
    @property
    def check_attack_dispel(self) -> bool:
        return self.dict_special_attacks_flag["dispel"]

    @property
    def check_turns_ingest(self) -> bool:
        return self.dict_turns_recharge["ingest"] >= (self.turns_to_recharge - 1)

    @property
    def check_turns_percentile(self) -> bool:
        return self.dict_turns_recharge["percentile"] >= (self.turns_to_recharge - 1) or self.dict_turns_recharge["percentile"] == 0
    
    @property
    def check_turns_stats_drain(self) -> bool:
        return self.dict_turns_recharge["stats_drain"] >= (self.turns_to_recharge - 1) or self.dict_turns_recharge["stats_drain"] == 0
    
    @property
    def check_turns_rot(self) -> bool:
        return self.dict_turns_recharge["rot"] >= (self.turns_to_recharge - 1)
    
    @property
    def check_turns_steal(self) -> bool:
        return self.dict_turns_recharge["steal"] >= (self.turns_to_recharge - 1)
    
    @property
    def check_turns_dispel(self) -> bool:
        return self.dict_turns_recharge["dispel"] >= (self.turns_to_recharge - 1)
    
    @property
    def check_for_special_attack_ready(self) -> bool:
        return (self.check_attack_ingest and self.check_turns_ingest) or (self.check_attack_percentile and self.check_turns_percentile) or (self.check_attack_stats and self.check_turns_stats_drain) or (self.check_attack_rot and self.check_turns_rot) or (self.check_attack_steal and self.check_turns_steal) or (self.check_attack_dispel and self.check_turns_dispel)
    

    def drain_stats_target(self, target: Actor) -> None:
        if self.dict_special_attack_values["strenght_drain"] > 0:
            if target.fighter.base_power <= 0:
                self.engine.message_log.add_message(f"The {self.parent.name} can't drain anymore of {target.name} strenght.")
                pass
            else:
                target.fighter.base_power -= self.dict_special_attack_values["strenght_drain"]
                if target.fighter.base_power < 0:
                    target.fighter.base_power = 0
                target.fighter.hp -= self.dict_special_attack_damage["stats_drain"]
                self.engine.message_log.add_message(f"The {target.name} feels less strong, as it's strength it's drained.")
        
        if self.dict_special_attack_values["agility_drain"] > 0:
            if target.fighter.base_defense <= 0:
                self.engine.message_log.add_message(f"The {self.parent.name} can't drain anymore of {target.name} agility.")
                pass
            else:
                target.fighter.base_defense -= self.dict_special_attack_values["agility_drain"]
                if target.fighter.base_defense < 0:
                    target.fighter.base_defense = 0
                target.fighter.hp -= self.dict_special_attack_damage["stats_drain"]
                self.engine.message_log.add_message(f"The {target.name} feels less agile, as it's agility it's drained.")

    
    def percentile_damage(self, target: Actor) -> None:
        if self.dict_special_attack_values["percentile"] > 0:
            damage = round((target.fighter.max_hp*self.dict_special_attack_values["percentile"])/100)
            target.fighter.hp -= damage
            self.engine.message_log.add_message(f"{target.name} feels a powerful force around him, dealing {damage}.")


        

        

