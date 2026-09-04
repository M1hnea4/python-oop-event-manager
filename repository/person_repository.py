from domain.person import Person
from repository.exceptions import RepositoryException

class PersonRepository:
    def __init__(self):
        """
        Initializes the PersonRepository with an empty list.
        """
        self._persons = []

    def add(self, person):
        """
        Adds a new person to the list.
        """
        for p in self._persons:
            if p.person_id == person.person_id:
                raise RepositoryException(f"Person with ID {person.person_id} already exists.")
        
        self._persons.append(person)

    def delete(self, person_id):
        """
        Deletes a person by ID.
        """
        person_to_delete = None
        for p in self._persons:
            if p.person_id == person_id:
                person_to_delete = p
                break
        
        if person_to_delete is None:
            raise RepositoryException(f"Person with ID {person_id} not found.")
            
        self._persons.remove(person_to_delete)

    def update(self, person_id, new_name):
        """
        Updates a person's name.
        """
        person = self.find_by_id(person_id)
        person.name = new_name

    def find_by_id(self, person_id):
        """
        Finds a person by ID.
        """
        for p in self._persons:
            if p.person_id == person_id:
                return p
        
        raise RepositoryException(f"Person with ID {person_id} not found.")

    def get_all(self):
        """
        Returns a list of all persons.
        """
        return self._persons[:]
        
    def search_by_name(self, query):
        """
        Searches for persons whose name contains the given text.
        """
        query = query.lower()
        return [p for p in self._persons if query in p.name.lower()]