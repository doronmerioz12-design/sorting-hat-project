from abc import ABC, abstractmethod
import numpy as np
from typing import Dict


class SortingStrategy(ABC):
    """
    Abstract Base Class that defines the contract for sorting logic across different universes.

    By using the 'Strategy' design pattern, this class allows the system to switch between
    different sorting engines (such as local vector-based similarity or remote LLM/AI sorting)
    without changing the core server logic. This ensures the application is scalable
    and easy to extend with new worlds.
    """

    @abstractmethod
    def sort(self, person_vector: np.ndarray) -> str:
        """
        Calculates and returns the best fitting house or nation for a given person.

        In the vector-based implementation, this compares the person's character vector
        against the predefined house vectors using cosine similarity. In an AI-based
        implementation, this method serves as the entry point for the LLM sorting logic.

        :param person_vector: A numerical representation (embedding) of the character's summary.
        :return: The name of the house or nation the character belongs to.
        """
        pass

    @abstractmethod
    def get_house_vectors(self) -> Dict[str, np.ndarray]:
        """
        Retrieves the predefined character vectors for all houses/nations in the current universe.

        These vectors represent the 'ideal' traits of each group (e.g., bravery for Gryffindor)
        and are used as the benchmark for the sorting process.

        :return: A dictionary mapping house names to their respective trait vectors.
        """
        pass

    def calculate_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        A helper utility to compute the cosine similarity between two vectors.

        Even when using AI for the final decision, maintaining this capability allows
        for 'Graceful Degradation'—providing a local backup sorting method if the
        AI service (like Gemini) is unavailable.

        :param v1: First trait vector.
        :param v2: Second trait vector.
        :return: A similarity score between -1.0 and 1.0.
        """
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))