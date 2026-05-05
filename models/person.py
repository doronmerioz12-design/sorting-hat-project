from typing import Dict, Optional
import numpy as np


class Person:
    """
    A data container class representing a character within the Sorting Hat system.

    This class stores all relevant information about a person, including their
    biographical summary, numerical vector representation for NLP tasks,
    and their assigned houses or nations across different universes.
    """

    def __init__(self, name: str):
        """
        Initializes a new Person instance.

        :param name: The full name of the character.
        """
        self.name = name
        # Biographical data fetched from Wikipedia or other sources
        self.summary = ""
        # The numerical embedding vector used for local NLP similarity logic
        self.vector: Optional[np.ndarray] = None
        # Maps universe names (e.g., 'Hogwarts') to assigned houses (e.g., 'Gryffindor')
        self.world_assignments: Dict[str, str] = {}
        # Stores similarity scores for different categories if calculated
        self.scores: Dict[str, float] = {}

    def to_dict(self) -> dict:
        """
        Converts the Person instance into a dictionary format.

        This is primarily used for serializing the object before saving it
        to a database like MongoDB.

        :return: A dictionary representation of the character's data.
        """
        return {
            "name": self.name,
            "summary": self.summary,
            "world_assignments": self.world_assignments,
            "scores": self.scores
        }

    @staticmethod
    def from_dict(data: dict) -> 'Person':
        """
        Creates a Person instance from a dictionary.

        This static method acts as a factory, allowing the system to reconstruct
        a Person object from raw data retrieved from the database.

        :param data: The dictionary containing character information.
        :return: A fully initialized Person object.
        """
        p = Person(data["name"])
        p.summary = data.get("summary", "")
        p.world_assignments = data.get("world_assignments", {})
        p.scores = data.get("scores", {})
        return p