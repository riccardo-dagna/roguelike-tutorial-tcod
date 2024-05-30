from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor

class SpecialAttacks(BaseComponent):
    parent: Actor
    turns_to_recharge: int = 3

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



