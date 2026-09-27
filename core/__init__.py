"""
Core package for Android automation.
Exposes common device controls and UI interaction actions.
"""

from .device import connect_device, restart_app, back_to_app
from .actions import click_and_wait, scroll_by_ratio

__all__ = [
    "connect_device",
    "restart_app",
    "back_to_app",
    "click_and_wait",
    "scroll_by_ratio",
]
