"""
This module imports the Blueprint objects used to handle JockeyAmazon-related routes 
for creating and updating data. It defines the `__all__` list to specify the public API 
of this module, which restricts the exports to the specified objects when this module 
is imported.

Modules:
    create_jockey_amazon: Contains the blueprint for creating a JockeyAmazon entity.
    update_jockey_amazon: Contains the blueprint for updating a JockeyAmazon entity.

Exports:
    create_jockey_amazon_bp (Blueprint): The Flask blueprint responsible for handling
        the creation of new JockeyAmazon records.
    update_jockey_amazon_bp (Blueprint): The Flask blueprint responsible for handling
        the update of existing JockeyAmazon records.
"""

from .create_jockey_amazon import create_jockey_amazon_bp
from .update_jockey_amazon import update_jockey_amazon_bp

__all__ = [
    "create_jockey_amazon_bp",
    "update_jockey_amazon_bp",
]