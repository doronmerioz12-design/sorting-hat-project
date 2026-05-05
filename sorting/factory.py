from .hogwarts import HogwartsStrategy
from sentence_transformers import SentenceTransformer
from .avatar import AvatarStrategy


class SortingFactory:
    """
    Factory class responsible for instantiating the correct sorting strategy.

    This implementation follows the 'Factory Method' design pattern, which centralizes
    the creation of universe-specific objects. This decoupling ensures that the
    main server logic does not need to know the implementation details of each
    sorting universe.
    """

    @staticmethod
    def get_strategy(school_name: str, model: SentenceTransformer):
        """
        Returns an instance of a SortingStrategy based on the provided universe name.

        This method acts as a router, mapping string identifiers (like 'hogwarts' or 'avatar')
        to their respective strategy classes. It passes the NLP model to the strategy
        to enable vector-based similarity calculations.

        :param school_name: The name of the universe (e.g., 'Hogwarts' or 'Avatar').
        :param model: The pre-trained SentenceTransformer model for text embedding.
        :return: An initialized instance of a class inheriting from SortingStrategy.
        :raises ValueError: If the requested universe name is not supported.
        """
        # Normalize the name to lowercase to ensure the factory is case-insensitive
        name = school_name.lower()

        if name == "hogwarts":
            return HogwartsStrategy(model)
        elif name == "avatar":
            return AvatarStrategy(model)
        else:
            # Raise an error if the user requests a universe that hasn't been implemented
            raise ValueError(f"Universe '{school_name}' is not recognized")