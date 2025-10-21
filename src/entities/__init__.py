"""
Entities module for Coffee Bros
Contains all game entity classes (Player, Platform, enemies, power-ups, etc.)
"""

from .player import Player
from .platform import Platform
from .polocho import Polocho
from .golden_arepa import GoldenArepa
from .laser import Laser
from .goal import Goal
from .corruption_boss import CorruptionBoss
from .mermelada import Mermelada

__all__ = ['Player', 'Platform', 'Polocho', 'GoldenArepa', 'Laser', 'Goal', 'CorruptionBoss', 'Mermelada']
