import numpy as np
from typing import Dict
from .base_strategy import SortingStrategy
from sentence_transformers import SentenceTransformer


class HogwartsStrategy(SortingStrategy):
    """
    Implementation of the SortingStrategy for the Harry Potter universe.

    This class defines the characteristics of the four Hogwarts houses and
    provides the mathematical logic to map characters to them using
    vector similarity (NLP).
    """

    def __init__(self, model: SentenceTransformer):
        """
        Initializes the Hogwarts strategy by defining house traits and generating embeddings.

        The descriptions serve as semantic benchmarks. The model uses these to
        compare the character's summary against each house's core values.

        :param model: The SentenceTransformer model used for text-to-vector encoding.
        """
        self.model = model

        # Qualitative descriptions of each house used for vector comparison
        self.house_descriptions = {
            "Gryffindor": (
                "A house for the brave, courageous, and chivalrous. Heroes who stand up for what is right despite the danger. "
                "Those people rarely seek attention, glory, or dominance, but they are the bravest, determined and value honor. "
                "Those in here seek what is right, not for medals, not for an award or power, but "
                "because it is right and they won't be villains."),

            "Slytherin": ("A house for the ambitious, cunning, and those who seek power and status at any cost. "
                          "Strategic thinkers who prioritize their own goals, they seek their own benefits and value ambition and control. "
                          "It is no surprise therefore that most villains are and criminals of any kind are "
                          "immediately go to this house"
                          "most nazis or war criminals will be there immediately , the worst people in history"),

            "Ravenclaw": "A house for the intelligent, creative, and wise. Those who value learning, wit, and intellectual discovery above all.",

            "Hufflepuff": (
                "A house for the kind, patient, and inclusive. Those who value fair play, simple hard work, and genuine friendship. "
                "They value friendship, kindness and loyalty more than any other.")
        }

        # Pre-compute house vectors during initialization to optimize performance
        self.house_vectors = self._generate_vectors()

    def _generate_vectors(self) -> Dict[str, np.ndarray]:
        """
        Encodes the text descriptions of each house into numerical vector embeddings.

        This internal method ensures that heavy encoding work is done once
        at the start, rather than during every user request.

        :return: A dictionary mapping house names to their corresponding NumPy vectors.
        """
        vectors = {}
        for house, desc in self.house_descriptions.items():
            vectors[house] = self.model.encode(desc)
        return vectors

    def get_house_vectors(self) -> Dict[str, np.ndarray]:
        """
        Public getter to retrieve the pre-computed house vectors.

        :return: A dictionary of house names and their trait vectors.
        """
        return self.house_vectors

    def sort(self, person_vector: np.ndarray) -> str:
        """
        Determines the most appropriate house using cosine similarity.

        This method acts as a reliable backup sorting engine (Graceful Degradation).
        It calculates the mathematical similarity between the character's vector
        and each house's pre-computed vector.

        :param person_vector: The character's biography encoded as a vector.
        :return: The name of the house with the highest similarity score.
        """
        best_house = None
        highest_similarity = -1.0

        for house, house_vector in self.house_vectors.items():
            # Manual calculation of cosine similarity using dot product and norms
            similarity = np.dot(person_vector, house_vector) / (
                    np.linalg.norm(person_vector) * np.linalg.norm(house_vector)
            )

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_house = house

        return best_house