import wikipediaapi
from models.person import Person


class WikiClient:
    """
    WikiClient manges the access to the wikipedia to receive the data for each person
    fairly technical but meant to connect the wikipedia using wikipediaapi
    and to search for a specific person
    """
    def __init__(self):
        """
        Initialize the WikiClient
        just some settings of which wikipedia, in which language and so on
        """

        self.wiki = wikipediaapi.Wikipedia(
            user_agent="SortingHatProject/1.0 (contact: your_email@mail.huji.ac.il)",
            language='en'
        )

    def fetch_person_data(self, person: Person) -> bool:

        """
        'fetch_person_data' fetches the data for a given person
        it received a name of a person, and check if there is a wikipedia page for that person
        and if so summerize it based on mainly 'biography' and 'personality'
        and if not or if there is an error throw it
        :param person: the person to fetch the data for
        :return: true if everything is ok, false otherwise with error message
        """
        try:

            page = self.wiki.page(person.name)

            if not page.exists():
                print(f"DEBUG: Wikipedia page for '{person.name}' not found.")
                return False


            data_text = page.summary


            relevant_sections = ['biography', 'early life', 'personality']
            for section in page.sections:
                if section.title.lower() in relevant_sections:
                    data_text += "\n" + section.text

            person.summary = data_text
            return True
        except Exception as e:
            print(f"DEBUG: Error fetching data: {e}")
            return False