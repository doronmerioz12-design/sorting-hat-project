from typing import Optional
from core.database import collection
from models.person import Person


class HistoryManager:
    """
    history manager class is responsible for managing the history of each user
    instead of going to the long and resource-consuming process of NLP and AI for
     each input the user insert, i used MONGODB to save past running of a user
     so if the user insert the same name to the same world it show it right away
    """
    def __init__(self):
        pass


    async def get_cached_person(self, user_id: str, name: str) -> Optional[Person]:
        """
        get_cached_person is responsible for getting the person from the database
        it lunches and check if the person and the respected house\ nation
        exists in the database and if so get it in a suited format using the function
        'from_dict' of the class person
        using await is to make sure our program doesn't halt until it received the answer
        :param user_id: the id of the user, for each user have a different history database
        :param name: the name of the person the user have inserted
        :return: the person from the database, in the right format, else return None
        """

        data = await collection.find_one({
            "user_id": user_id,
            "name": name
        })

        if data: #if the person and the world exsist in the database
            return Person.from_dict(data) # see person class for elaboration
        return None

    async def save_person(self, user_id: str, person: Person):
        """
        save_person is responsible for saving the person to the database
        each time the user insert a name or world that doesn't exist in the database
        this function is responsible for saving the person to the database
        for later using a function called 'to_dict' of the class person
        and 'update_one' in the collection
        :param user_id: as mentioned in 'get_cached_person' function
        :param person: the person to save
        :return: nothing in particular just add the person to the database
        """
        person_dict = person.to_dict()

        person_dict["user_id"] = user_id

        await collection.update_one(
            {"user_id": user_id, "name": person.name},
            {"$set": person_dict},
            upsert=True
        )