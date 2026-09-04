from repository.person_repository import PersonRepository
from domain.person import Person

class PersonFileRepository(PersonRepository):
    def __init__(self, filename):
        super().__init__()
        self.__filename = filename
        self.__load_from_file()

    def __load_from_file(self):
        try:
            with open(self.__filename, "r") as f:
                lines = f.readlines()
                
                i = 0
                while i < len(lines):
                    person_id = lines[i].strip()
                    
                    if i + 1 < len(lines):
                        name = lines[i+1].strip()
                        
                        if person_id and name:
                            person = Person(person_id, name)
                            self._persons.append(person)

                    i += 2
        except FileNotFoundError:
            pass

    def __save_to_file(self):
        with open(self.__filename, "w") as f:
            for person in self.get_all():
                f.write(f"{person.person_id}\n{person.name}\n")

    def add(self, person):
        super().add(person)
        self.__save_to_file()

    def delete(self, person_id):
        super().delete(person_id)
        self.__save_to_file()

    def update(self, person_id, new_name):
        super().update(person_id, new_name)
        self.__save_to_file()