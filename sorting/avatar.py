import numpy as np
from typing import Dict
from .base_strategy import SortingStrategy
from sentence_transformers import SentenceTransformer


class AvatarStrategy(SortingStrategy):
    """
    Implementation of the SortingStrategy for the Avatar: The Last Airbender universe.

    This class manages the four nations (Fire, Air, Water, Earth) and provides
    the logic to sort characters into them based on their personality traits
    and historical summaries.
    """

    def __init__(self, model: SentenceTransformer):
        """
        Initializes the Avatar universe strategy with a pre-trained NLP model.

        The constructor defines the core characteristics of each nation and
        pre-computes their trait vectors to optimize the sorting process.

        :param model: An instance of SentenceTransformer used to generate embeddings.
        """
        self.model = model
        # Predefined qualitative descriptions used as benchmarks for sorting
        self.nation_descriptions = {
            "Fire": "Fire is the element of power. The people of the Fire Nation have desire and will and the energy and drive to achieve what they want.",
            "Air": "Air is the element of freedom. The Air Nomads detached themselves from worldly concerns, and they found peace and freedom. And they apparently had great senses of humor.",
            "Water": "Water is the element of change. The people of the Water Tribes are capable of adapting to many things. They have a sense of community and love that holds them together through anything.",
            "Earth": "Earth is the element of substance. The people of the Earth Kingdom are diverse and strong. They are persistent and enduring."
        }
        self.nation_vectors = self._generate_vectors()

    def _generate_vectors(self) -> Dict[str, np.ndarray]:
        """
        An internal helper method that converts nation descriptions into numerical vectors.

        This process (embedding) happens once during initialization to ensure that
        subsequent sorting operations are fast and do not require redundant computations.

        :return: A dictionary where keys are nation names and values are their trait vectors.
        """
        vectors = {}
        for nation, desc in self.nation_descriptions.items():
            vectors[nation] = self.model.encode(desc)
        return vectors

    def get_house_vectors(self) -> Dict[str, np.ndarray]:
        """
        Public getter to retrieve the pre-computed vectors for all Avatar nations.

        :return: A dictionary mapping nation names to their respective trait vectors.
        """
        return self.nation_vectors

    def sort(self, person_vector: np.ndarray) -> str:
        """
        Performs the sorting logic by comparing a character's vector to each nation's vector.

        The method uses cosine similarity to find the nation that best matches the
        character's summary. This serves as a robust local sorting engine and can
        act as a fallback mechanism if the primary AI service is unavailable.

        :param person_vector: The embedding vector representing the character being sorted.
        :return: The name of the nation (Fire, Air, Water, or Earth) with the highest similarity.
        """
        best_nation = None
        highest_similarity = -1.0

        for nation, nation_vector in self.nation_vectors.items():
            # Calculating cosine similarity manually using numpy
            similarity = np.dot(person_vector, nation_vector) / (
                    np.linalg.norm(person_vector) * np.linalg.norm(nation_vector)
            )

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_nation = nation

        return best_nation