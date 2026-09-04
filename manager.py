from validation.person_validator import PersonValidator
from validation.event_validator import EventValidator
from validation.registration_validator import RegistrationValidator 

from repository.person_file_repository import PersonFileRepository
from repository.event_repository import EventRepository
from repository.registration_repository import RegistrationRepository 

from services import MainController
from ui import ConsoleUI 

def start_application():
    """
    Builds all the application components and starts the UI.

    """
    person_validator = PersonValidator()
    event_validator = EventValidator()
    registration_validator = RegistrationValidator() 

    person_repo = PersonFileRepository("persons.txt")

    event_repo = EventRepository()
    registration_repo = RegistrationRepository() 

    controller = MainController(
        person_repo, 
        event_repo, 
        registration_repo,          
        person_validator, 
        event_validator,
        registration_validator      
    )

    console_ui = ConsoleUI(controller)

    console_ui.run()