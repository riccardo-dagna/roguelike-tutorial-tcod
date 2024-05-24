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
                 status_ingest: bool = False,
                ) -> None:
        self.dict_special_attacks_flag = dict(ingest = flag_ingest, percentile = flag_percentile, stats_drain = flag_stats_drain, rot = flag_rot, steal = flag_steal, dispel = flag_dispel,)
        self.dict_special_attack_values = dict(percentile = values_percentile, strenght_drain = value_strenght_drain, agility_drain = value_agility_drain,)
        self.dict_special_attack_status = dict(ingest = status_ingest,)
        turns_recharge: int = 0

    



