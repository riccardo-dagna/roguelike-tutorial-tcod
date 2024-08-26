"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

from typing import Optional
import copy
import lzma
import pickle
import traceback

from PIL import Image  # type: ignore
import tcod
import libtcodpy

from entity.entity import Actor
from game_logic.engine import Engine
from game_map.game_map import GameWorld
import game_map.color as color
from entity.entity_factories import entities
from entity.entity_factories import equipment
import actions_logic.input_handlers as input_handlers
import components.spells.spell_list as spell_list
from utility_files.utility import resource_path

# Load the background image.  Pillow returns an object convertable into a NumPy array.
background_image = Image.open(resource_path("data/menu_background.png"))

def choose_player_character(character_choice: int) -> Engine:
    """Spawn a different player and equipment based on the character choice"""
    if character_choice == 1:
        player = copy.deepcopy(entities.player_fighter)

        sword = copy.deepcopy(equipment.sword)
        leather_armor = copy.deepcopy(equipment.leather_armor)

        sword.parent = player.inventory
        leather_armor.parent = player.inventory

        player.inventory.items.append(sword)
        player.equipment.toggle_equip(sword, add_message=False)

        player.inventory.items.append(leather_armor)
        player.equipment.toggle_equip(leather_armor, add_message=False)

    elif character_choice == 2:
        player = copy.deepcopy(entities.player_mage)

        dagger = copy.deepcopy(equipment.dagger)
        dagger.parent = player.inventory
        player.inventory.items.append(dagger)
        player.equipment.toggle_equip(dagger, add_message=False)

        fireball = spell_list.Fireball(player)
        lightning_bolt = spell_list.LightningBolt(player)
        ice_dart = spell_list.IceDart(player)
        confusion = spell_list.Confusion(player)
        fear = spell_list.Fear(player)
        stun = spell_list.Stun(player)
        heal = spell_list.Heal(player)

        player.spellbook.spells.append(fireball)
        player.spellbook.spells.append(lightning_bolt)
        player.spellbook.spells.append(ice_dart)
        player.spellbook.spells.append(confusion)
        player.spellbook.spells.append(fear)
        player.spellbook.spells.append(stun)
        player.spellbook.spells.append(heal)
    elif character_choice == 3:
        player = copy.deepcopy(entities.player_thief)

        dagger = copy.deepcopy(equipment.dagger)
        leather_armor = copy.deepcopy(equipment.leather_armor)
        bow = copy.deepcopy(equipment.bow)

        dagger.parent = player.inventory
        leather_armor.parent = player.inventory
        bow.parent = player.inventory

        player.inventory.items.append(dagger)
        player.equipment.toggle_equip(dagger, add_message=False)

        player.inventory.items.append(leather_armor)
        player.equipment.toggle_equip(leather_armor, add_message=False)

        player.inventory.items.append(bow)
        player.equipment.toggle_equip(bow, add_message=False)
    return player



def new_game(character_choice: int = 1) -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = choose_player_character(character_choice)

    #player = copy.deepcopy(entities.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov(radius=8)

    engine.message_log.add_message("Welcome to the dungeon, adventurer!", color.welcome_text)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE ANCIENT KINGS",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Just RD",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return ChoosePlayerHandler()

        return None


class ChoosePlayerHandler(input_handlers.BaseEventHandler):
    """Handle the choosing of the player character"""
    
    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "CHOOSE YOUR CLASS",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(["A) Fighter", "B) Mage", "C) ThieF"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        character_choice = 0

        if event.sym == tcod.event.KeySym.a:
            character_choice = 1            
        elif event.sym == tcod.event.KeySym.b:
            character_choice = 2
        elif event.sym == tcod.event.KeySym.c:
            character_choice = 3
        else:
            raise SystemExit()
            
        return input_handlers.MainGameEventHandler(new_game(character_choice))